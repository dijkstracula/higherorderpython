# Chapter 1: Dispatch tables

import re

from typing import Any, Callable


def change_dir(arg: str):
    print(f"Changing dir to {arg}")


def open_log_file(arg: str):
    print(f"Opening {arg}")


def set_verbosity(arg: str):
    print(f"setting verbosity to {int(arg)}")


# See XXX note on function signatures.
def set_var(k: str, v: str):
    global dispatch_user_globals
    dispatch_user_globals[k] = v


def define_config_directive(arg: str):
    new_directive, def_body = re.split(r"\s+", arg, 1)
    if new_directive in dispatch_table:
        print(f"WARN: {new_directive} already defined; skipping.")
    if not def_body:
        print(f"WARN: {new_directive} has no body; skipping.")
    print(f"Directive {new_directive} will execute {def_body}")

    def doit(a: str):
        local_frame = {"arg": a} | dispatch_user_globals
        exec(def_body, None, local_frame)
        for k in local_frame:
            if k != "arg":
                dispatch_user_globals[k] = local_frame[k]

    dispatch_table[new_directive] = doit


def read_config(fn: str):
    with open(fn) as f:
        for lineno, line in enumerate(f.readlines()):
            line = line.strip()
            if line == "":
                continue
            tokens = re.split(r"\s+", line, 1)
            if len(tokens) == 2:
                (directive, rest) = tokens
            else:
                (directive, rest) = tokens[0], ""

            if directive not in dispatch_table:
                raise Exception(f"Unknown directive {directive} on line {lineno} of {fn}")
            dispatch_table[directive](rest)


dispatch_user_globals: dict[str, Any] = {"read_config": read_config}

dispatch_table: dict[str, Callable[[str], None]] = {
    "CHDIR": change_dir,
    "LOGFILE": open_log_file,
    "DEFINE": define_config_directive,

    # XXX: This is different from the HOP book in that all callbacks are implicitly variadic.  Figure out
    # how to represent that with type hints (a protocol, I think?)
    "VERBOSITY": lambda v: set_var("VERBOSITY", v),
    "TABLESIZE": lambda v: set_var("TABLESIZE", v),
    "PERLPATH":  lambda v: set_var("PERLPATH", v)
}
