import csv
import os
from utils import file_checksum


class TaskHolder:

    def __init__(self, result_folder):
        self.folder = result_folder
        self.task_list = []
        self.checksums = {}
        self.checksums_file = os.path.join(result_folder, "checksums.tsv")

    def add_task_list(self, tasks):
        self.task_list.extend(tasks)

    def add_tasks(self, *tasks):
        self.task_list.extend(tasks)

    def execute(self, verbose=False):
        self._load_checksums()
        try:
            for task in self.task_list:
                if verbose:
                    print(task)
                if self.should_be_rerun(task):
                    task.execute()
                    self._calculate_checksums(task)
                else:
                    print(f"Skipping task '{task.name}'")
        finally:
            with open(self.checksums_file, 'w') as f:
                for record, checksum in self.checksums.items():
                    f.write(f"{record[0]}\t{record[1]}\t{checksum}\n")

    def should_be_rerun(self, task):
        inputs = list(task.inputs.values())
        inputs = inputs + [task.stdin] if task.stdin else inputs

        for filename in inputs:
            found_hash = self.checksums.get((task.name, filename), None)
            if found_hash is None:
                return True
            actual = file_checksum(filename)
            if found_hash != actual.hexdigest():
                return True
        return False

    def _load_checksums(self):
        if not os.path.isfile(self.checksums_file):
            return
        with open(self.checksums_file) as f:
            reader = csv.reader(f, delimiter="\t")
            for record in reader:
                if len(record) < 3:
                    raise RuntimeError(f"Malformed checksum file '{self.checksums_file}'")
                self.checksums[(record[0], record[1])] = record[2]

    def _calculate_checksums(self, task):
        inputs = list(task.inputs.values())
        inputs = inputs + [task.stdin] if task.stdin else inputs
        for filename in inputs:
            digest = file_checksum(filename)
            self.checksums[(task.name, filename)] = digest.hexdigest()

        outputs = list(task.outputs.values())
        outputs = outputs + [task.stdout] if task.stdout else outputs
        for filename in outputs:
            digest = file_checksum(filename)
            self.checksums[(task.name, filename)] = digest.hexdigest()
