# CPypes

**CPypes** is an attempt to reduce the *module importing* time for Python scripts.

The idea is to open a **server** in Python that listens commands from NamedPipes, executes them, and returns to the NamedPipe. 
The client (in this case implemented in C) will read commands from *stdin*, send to python, wait for the respond, and print the output.

## Usage
Compile the client:

```
gcc c_pipe.c -o c_pipe -O0
```


## How to run
Set the server up:
``` bash
bash-3.2$ python py_pipe.py &
```

Send commands to the server:
``` bash
bash-3.2$ echo "import numpy as np" | ./c_pipe
bash-3.2$ echo "arr = np.random.rand(1000)" | ./c_pipe
bash-3.2$ echo "print(arr.mean())" | ./c_pipe
0.496063080565581
bash-3.2$
bash-3.2$ echo "from pandas import DataFrame as df;
print(df(arr).describe())" | ./c_pipe
                 0
count  1000.000000
mean      0.496063
std       0.288981
min       0.000076
25%       0.244315
50%       0.490009
75%       0.754183
max       0.998509
bash-3.2$ 
```

## Limitations
* Because the idea works with NamedPipes, a unix system is required.

## Todos
* Use a makefile to compile the client (?).
* For the client, other optimizations (e.g. `-O3`) break the code, investigate why.
* Test the input/output array size
* Redirect pipes in case of large stdin (?). Instead of reading from stdin and writing to t
he pipe, just make python read from the stdin pipe c (?). Probably need to test if that is really needed.
