# Higher Order Python

Higher Order Perl, but worked through in Python, for fun.  

### Setup

I'm using python3.12 because I'm cool.  Will I later use python3.13?  Who can say.

```
$ apt-get install libsqlite3-dev libreadline6-dev
```

```
$ cd Python
$ ./configure --enable-optimizations --enable-loadable-sqlite-extensions
$ make -j8
```

I use Poetry for dependency management. Install it, create your virtual
environment, and install dependencies into it.

```
$ curl -sSL https://install.python-poetry.org | python3 -
$ echo 'export PATH="/home/ntaylor/.local/bin:$PATH"' >> ~/.zshrc
$ source ~/.zshrc
$ which poetry         
/home/ntaylor/.local/bin/poetry
$ 
```

Point Poetry to the right version of Python 3.12.

```
$ poetry env use ~/Downloads/Python-3.12.4/python
Creating virtualenv porter-WiUz2hvV-py3.12 in /home/ntaylor/.cache/pypoetry/virtualenvs
$ poetry install
Updating dependencies
[...]
Installing the current project: porter (0.1.0)
$
```

### Testing

```commandline
$ poetry run pytest
$ poetry run pyright
```
