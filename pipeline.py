import os
from task import Task
from taskholder import TaskHolder
from utils import create_statistics


class SimplePipeline:

    def __init__(self, data_folder):
        self.data_folder = data_folder

    def data_file(self, filename):
        return os.path.join(self.data_folder, filename)

    def run_simple_pipeline(self):

        stocks = self.data_file("stonks.tsv")
        chars_file = self.data_file("_chars.tsv")
        task_chars = Task("CharCount") \
            .with_command_list("wc", "{mode}") \
            .with_stdin(stocks) \
            .with_stdout(chars_file) \
            .with_parameter("{mode}", "-c")

        lines_file = self.data_file("_lines.tsv")
        task_lines = Task("LineCount") \
            .with_command_list("wc", "{mode}") \
            .with_stdin(stocks) \
            .with_stdout(lines_file) \
            .with_parameter("{mode}", "-l")

        quotes_file = self.data_file("quotes-day0.tsv")
        value_file = self.data_file("_value.txt")
        task_value = Task("PortfolioValue") \
            .with_command_list("python", "eval_portfolio.py", "-s", "{stocks}", "-q", "{quotes}") \
            .with_input("{stocks}", stocks) \
            .with_input("{quotes}", quotes_file) \
            .with_stdout(value_file)

        stocks_after_loss = self.data_file("_stonks.loss.tsv")
        task_stocks_after_loss = Task("GazpromLoss") \
            .with_command_list("sed", "'/GZPR/d'", "{input}") \
            .with_input("{input}", stocks) \
            .with_stdout(stocks_after_loss)

        value_loss_file = self.data_file("_value.loss.txt")
        task_value_after_loss = Task("ValueAfterLoss") \
            .with_command_list("python", "eval_portfolio.py", "-s", "{stocks}", "-q", "{quotes}") \
            .with_input("{stocks}", stocks_after_loss) \
            .with_input("{quotes}", quotes_file) \
            .with_stdout(value_loss_file)

        quotes_bigtech_file = self.data_file("quotes-bigtech.tsv")
        value_bigtech_file = self.data_file("_value.bigtech.txt")
        task_value_after_rally = Task("ValueAfterBigTechRally") \
            .with_command_list("python", "eval_portfolio.py", "-s", "{stocks}", "-q", "{quotes}") \
            .with_input("{stocks}", stocks_after_loss) \
            .with_input("{quotes}", quotes_bigtech_file) \
            .with_stdout(value_bigtech_file)

        task_holder = TaskHolder(self.data_folder)
        task_holder.add_tasks(task_chars, task_lines, task_value, task_stocks_after_loss,
                              task_value_after_loss, task_value_after_rally)
        task_holder.execute()

        stat_summary = self.data_file("_stat.summary.tsv")
        create_statistics(chars_file, lines_file, value_file, value_loss_file, value_bigtech_file,
                          stat_summary)

        last_task = Task("ListChecksums").with_command_list("cat", "{input}", "{chk}")\
            .with_input("{chk}", task_holder.checksums_file)\
            .with_input("{input}", stat_summary)
        last_task.execute()
