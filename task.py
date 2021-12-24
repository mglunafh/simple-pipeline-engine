import subprocess


class Task:

    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.outputs = {}
        self.parameters = {}
        self.stdin = None
        self.stdout = None
        self.command = ""

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
        print(f"Executing command: '{' '.join(command)}'")
        if self.stdin:
            process = subprocess.Popen(command,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True,
                                       bufsize=0)
            with open(self.stdin) as f:
                process.stdin.writelines(f.readlines())
                process.stdin.close()

            stdout, stderr = process.communicate()
            if self.stdout:
                with open(self.stdout, "w") as result:
                    result.write(stdout)
            else:
                print(stdout)
            print(stderr)

        else:
            process = subprocess.Popen(command,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            stdout, stderr = process.communicate()
            if self.stdout:
                with open(self.stdout, "w") as result:
                    result.write(stdout)
            else:
                print(stdout)
            print(stderr)

    @staticmethod
    def __replace(lst, label, value):
        return [x if x != label else value for x in lst]
