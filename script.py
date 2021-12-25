#!/usr/bin/env python

import os
from task import Task
from utils import create_statistics

DATA_FOLDER = "data"


def data_file(filename):
    return os.path.join(DATA_FOLDER, filename)


stocks = data_file("stonks.tsv")
chars_file = data_file("_chars.tsv")
task_chars = Task("CharCount")\
    .with_command_list("wc", "{mode}")\
    .with_stdin(stocks)\
    .with_stdout(chars_file)\
    .with_parameter("{mode}", "-c")

lines_file = data_file("_lines.tsv")
task_lines = Task("LineCount") \
    .with_command_list("wc", "{mode}")\
    .with_stdin(stocks)\
    .with_stdout(lines_file)\
    .with_parameter("{mode}", "-l")

quotes_file = data_file("quotes-day0.tsv")
value_file = data_file("_value.txt")
task_value = Task("PortfolioValue")\
    .with_command_list("python", "eval_portfolio.py", "-s", "{stocks}", "-q", "{quotes}")\
    .with_input("{stocks}", stocks)\
    .with_input("{quotes}", quotes_file)\
    .with_stdout(value_file)

stocks_after_loss = data_file("_stonks.loss.tsv")
task_stocks_after_loss = Task("GazpromLoss")\
    .with_command_list("sed", "'/GZPR/d'", "{input}")\
    .with_input("{input}", stocks)\
    .with_stdout(stocks_after_loss)

value_loss_file = data_file("_value.loss.txt")
task_value_after_loss = Task("PortfolioValueAfterLoss") \
    .with_command_list("python", "eval_portfolio.py", "-s", "{stocks}", "-q", "{quotes}") \
    .with_input("{stocks}", stocks_after_loss) \
    .with_input("{quotes}", quotes_file) \
    .with_stdout(value_loss_file)

quotes_bigtech_file = data_file("quotes-bigtech.tsv")
value_bigtech_file = data_file("_value.bigtech.txt")
task_value_after_rally = Task("PortfolioValueAfterAfterBigTechRally") \
    .with_command_list("python", "eval_portfolio.py", "-s", "{stocks}", "-q", "{quotes}") \
    .with_input("{stocks}", stocks_after_loss) \
    .with_input("{quotes}", quotes_bigtech_file) \
    .with_stdout(value_bigtech_file)


task_chars.execute()
task_lines.execute()
task_value.execute()
task_stocks_after_loss.execute()
task_value_after_loss.execute()
task_value_after_rally.execute()

stat_summary = data_file("_stat.summary.tsv")
create_statistics(chars_file, lines_file, value_file, value_loss_file, value_bigtech_file,
                  stat_summary)
