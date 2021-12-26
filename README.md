# Simple pipeline engine 
This is a file-based pipeline engine on Python which may come in handy when 
a good old bash script processing files and outputting its result into other files 
starts producing more problems than it solves, adopts too much additional logic,
uses excessive amount of control structures or becomes unmaintainable to your taste.

### Simple example with input file
``wc -l some.txt``

can be represented as

```python
task = Task("CountLines").with_command("wc", "-l", "some.txt")
task.execute()
```

### Simple example with parameterized input file
We want to track the input file `some.txt` by pipeline engine in the previous command 

``wc -l some.txt``

so we use `with_input()` method:

```python
target_file = "some.txt"
task = Task("CountLines").with_command("wc", "-l", "{input}").with_input("{input}", target_file)
task.execute()
```

### Simple example with two types of parameters
What if we would like to parameterize what to count as well?

```python
target_file = "some.txt"

task_lines = Task("CountLines")\
    .with_command("wc", "{mode}", "{input}")\
    .with_input("{input}", target_file)\
    .with_parameter("{mode}", "-l")
task_lines.execute()

task_chars = Task("CountCharacters")\
    .with_command("wc", "{mode}", "{input}")\
    .with_input("{input}", target_file)\
    .with_parameter("{mode}", "-c")
task_chars.execute()

```
