# =========================
# compiler.py
#
# Copyright (c) 2019 i-pu
# =========================

import re
from textwrap import dedent


def compile(ipl):
    """
    extract template and functions from the ipl file, 

    Parameters
    ----------
    ipl : string
        A content of a plugin (*.ipl)
    
    Returns
    -------
    template : string
        A plugin html that'll be passed to a client.
    functions : dict
        A python code that'll be run as a socket server.
    """

    res = re.match(r'.*<html>(.*)</html>.*<script>(.*)</script>.*', ipl, flags=re.DOTALL)
    if res:
        functions = dict()
        template, script = res.groups()
        # [(f, args, stmt), ...]
        it = re.finditer(r"^(\w+)\s*\((.*?)\)\s*\{(.*?)^\}", script, flags=re.DOTALL | re.MULTILINE)
        for match in it:
            (f, args, stmt) = match.groups()
            args = [] if args == '' else [arg.strip() for arg in args.split(',')]
            functions[f] = [*args, stmt]

        return template, functions
