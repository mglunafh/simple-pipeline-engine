import os
import sys
from contextlib import redirect_stderr
from io import StringIO

import pytest
from task import Task
import tempfile
from outputter import TEMPLATE, OUT, ERR


@pytest.fixture()
def capt_out():
    f = tempfile.TemporaryFile(mode="w+", encoding=sys.stdout.encoding)
    try:
        yield f
    finally:
        f.close()


@pytest.fixture()
def capt_file():
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    filename = tmpfile.name
    try:
        yield filename
    finally:
        tmpfile.close()
        os.unlink(filename)


class TestTask:

    def test_echo(self, capt_out):
        data_to_print = "Helloworld!"

        task = Task("Echo").with_command_list('echo', data_to_print)
        task.execute(use_shell=True, custom_output=capt_out)

        capt_out.seek(0)
        value = capt_out.read().strip('"\n')
        assert value == data_to_print

    def test_echo_file(self, capt_file):
        data_to_print = "Hello-world!!"
        task = Task("EchoIntoFile").with_command_list("echo", data_to_print).with_stdout(capt_file)
        task.execute(use_shell=True)
        with open(capt_file) as result:
            data = result.read().strip()
            assert data == data_to_print

    def test_outputter_stdout(self, capt_out):

        task = Task("OutputterStdout").with_command_list("python", "outputter.py", "1o")
        task.execute(custom_output=capt_out)

        capt_out.seek(0)
        value = capt_out.read().strip()
        expected = TEMPLATE.format(channel=OUT, n=1)
        assert value == expected

    def test_outputter_stderr(self):

        task = Task("OutputterStderr").with_command_list("python", "outputter.py", "1e")
        with redirect_stderr(StringIO()) as capture:
            task.execute()

        value = capture.getvalue().strip()
        expected = f"{task.name}: {TEMPLATE.format(channel=ERR, n=1)}"
        assert value == expected

    def test_outputter_both(self, capt_out):

        task = Task("OutputterStderr").with_command_list("python", "outputter.py", "1o", "1e")
        with redirect_stderr(StringIO()) as capt_err:
            task.execute(custom_output=capt_out)

        capt_out.seek(0)
        out_value = capt_out.read().strip()
        expected = TEMPLATE.format(channel=OUT, n=1)
        assert out_value == expected

        value = capt_err.getvalue().strip()
        expected = f"{task.name}: {TEMPLATE.format(channel=ERR, n=2)}"
        assert value == expected

    def test_outputter_outfile(self, capt_file):

        task = Task("OutputterStdoutFile")\
            .with_command_list("python", "outputter.py", "1o", "-o", "{out}")\
            .with_output("{out}", capt_file)
        task.execute()
        expected = TEMPLATE.format(channel=OUT, n=1)

        with open(capt_file) as result:
            data = result.read().strip()
            assert data == expected

    def test_outputter_errfile(self, capt_file):

        task = Task("OutputterStderrFile")\
            .with_command_list("python", "outputter.py", "1e", "-e", "{err}")\
            .with_output("{err}", capt_file)
        task.execute()

        expected = TEMPLATE.format(channel=ERR, n=1)
        with open(capt_file) as result:
            data = result.read().strip()
            assert data == expected
