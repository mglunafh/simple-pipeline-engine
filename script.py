import os
from task import Task


stocks = os.path.join("data", "stonks.tsv")

t1 = Task("first task")\
    .with_command_list("cat", "{input}")\
    .with_input("{input}", stocks)

t2 = Task("Line count")\
    .with_command_list("wc", "{mode}", "{file}")\
    .with_input("{file}", stocks)\
    .with_parameter("{mode}", "-l")

t3 = Task("Char count")\
    .with_command_list("wc", "{mode}", "{file}")\
    .with_input("{file}", stocks)\
    .with_parameter("{mode}", "-c")

lines_file = os.path.join("data", "_lines.tsv")
t4 = Task("Line count") \
    .with_command_list("wc", "{mode}")\
    .with_stdin(stocks)\
    .with_stdout(lines_file)\
    .with_parameter("{mode}", "-l")

stocks_after_crash = os.path.join("data", "_stonks.crash.tsv")
t5 = Task("Gazprom crash")\
    .with_command_list("sed", "'/GZPR/d'", "{input}")\
    .with_input("{input}", stocks)\
    .with_stdout(stocks_after_crash)

current_task = t4
print(current_task)
current_task.execute()

# for t in [t1, t2, t3, t4]:
#     print(t)
#     t.execute()
#     print("\n+++++++++++++++++++++\n")
