import subprocess


class ExecutionException(Exception):

    def __init__(self, task_name, exit_status):
        self.name = task_name
        self.exit_code = exit_status
        super().__init__(f"Task '{task_name}' failed with exit status: {exit_status}")


class Task:

    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.outputs = {}
        self.parameters = {}
        self.stdin = None
        self.stdout = None
        self.command = []

    def with_input(self, label, filename):
        if label not in self.inputs:
            self.inputs[label] = filename
            return self
        else:
            raise RuntimeError(f"Task '{self.name}' already contains input label '{label}'")

    def with_stdin(self, filename):
        self.stdin = filename
        return self

    def with_stdout(self, filename):
        self.stdout = filename
        return self

    def with_output(self, label, filename):
        if label not in self.outputs:
            self.outputs[label] = filename
            return self
        else:
            raise RuntimeError(f"Task '{self.name}' already contains output label '{label}'")

    def with_parameter(self, label, param):
        if label not in self.parameters:
            self.parameters[label] = param
            return self
        else:
            raise RuntimeError(f"Task '{self.name}' already contains parameter label '{label}'")

    def with_command_list(self, *command):
        self.command = list(command)
        return self

    def __str__(self):
        lines = [f"Task: {self.name}", f"Command template: {self.command}"]
        if self.stdin:
            lines.append(f"<---- Input file: {self.stdin}")
        if self.stdout:
            lines.append(f"---> Output file: {self.stdout}")

        lines.append("========= Inputs =====")
        for label, filename in self.inputs.items():
            lines.append(f"{label}: {filename}")

        lines.append("======== Outputs =====")
        for label, filename in self.outputs.items():
            lines.append(f"{label}: {filename}")

        lines.append("===== Parameters =====")
        for label, param in self.parameters.items():
            lines.append(f"{label}: {param}")
        lines.append("======================")
        return "\n".join(lines)

    def get_command(self):
        command = self.command
        for label, input in self.inputs.items():
            command = Task.__replace(command, label, input)
        for label, output in self.outputs.items():
            command = Task.__replace(command, label, output)
        for label, param in self.parameters.items():
            command = Task.__replace(command, label, param)
        return command

    def execute(self):
        command = self.get_command()
        print(f"Executing '{self.name}' command: [> {' '.join(command)} <]\n")

        process = subprocess.Popen(command,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True,
                                   bufsize=0)
        if self.stdin:
            with open(self.stdin) as f:
                process.stdin.writelines(f.readlines())
        process.stdin.close()
        self.__process_output(process)

    def __process_output(self, process):
        result_file = None if not self.stdout else open(self.stdout, "w")
        try:
            while True:
                output = process.stdout.readline()
                print(output, file=result_file, end="")
                exit_code = process.poll()
                if exit_code is not None:
                    for stdout_line in process.stdout.readlines():
                        print(stdout_line, file=result_file, end="")
                    for err_line in process.stderr.readlines():
                        print(f"{self.name}: {err_line}", end="")
                    if exit_code != 0:
                        raise ExecutionException(self.name, exit_code)
                    break
        finally:
            if result_file:
                result_file.close()

    @staticmethod
    def __replace(lst, label, value):
        return [x if x != label else value for x in lst]
