# =========================
# compiler.py
#
# Copyright (c) 2019 i-pu
# =========================

import re


def compiler(ipl):
    """
    extract template and functions from the ipl file,

    Parameters
    ----------
    ipl : str
        A content of a plugin (*.ipl)

    Returns
    -------
    template : string
        A plugin template that'll be passed to a client.
    functions : string
        A JavaScript code that'll be run as a socket server.
    """

    match_result = re.match(r'.*<template>(.*)</template>.*<script>(.*)</script>.*',ipl, flags = re.DOTALL)

    if match_result is None:
        print("[Plugin Compiler] Illegal format.")
        return None

    template, raw_script = match_result.groups()

    match_result = re.findall(r"export default.*?{(.*)}", raw_script, flags = re.DOTALL)

    if len(match_result) == 0:
        print("[Plugin Compiler] Functions not found.")
        return None
        
    functions = '({' + match_result[0] + '})'
    return template, functions
