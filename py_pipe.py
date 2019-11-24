# Required libraries
import os
import errno
import sys

from io import StringIO
import contextlib

# Additional libraries (to pre-load)
import numpy as np
from pandas import DataFrame as df


@contextlib.contextmanager
def stdoutIo(stdout=None):
    _stdout = sys.stdout
    stdout = StringIO() if stdout is None else stdout
    sys.stdout = stdout
    yield stdout
    sys.stdout = _stdout


FIFO = '/tmp/myfifo'
MAX = 1005


def readline_from_pipe():
    pipe = os.open(FIFO, os.O_RDONLY)
    msg = str(os.read(pipe, MAX), 'utf-8')
    msg = msg.strip()[:-2]
    os.close(pipe)
    return msg


def read_stdin():
    arr = []
    while True:
        msg = readline_from_pipe()
        if msg == '~eof~':
            break
        arr.append(msg)
    return arr


__my_globals = {}
__my_locals = {}


def execute_cmd(cmd):
    try:
        with stdoutIo() as my_stdout:
            exec(cmd, __my_globals, __my_locals)
        output = my_stdout.getvalue()
    except Exception as err:
        print (err)
        raise

    return output


def write_to_pipe(msg):
    pipe = os.open(FIFO, os.O_WRONLY)
    os.write(pipe, msg.encode())
    os.close(pipe)


def main():
    while True:
        cmd = readline_from_pipe()
        # if cmd == '~~eof~~':
            # break;
        cmd_output = execute_cmd(cmd)
        write_to_pipe(cmd_output)

if __name__ == '__main__':
    main()
