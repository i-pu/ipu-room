from .html_interpreter import Parser

"""
From the html template, extract `events`, `records`, and `python`
"""


def plugin_compiler(plugin):
    """
    ===== plugin_compiler.py ======================
      plugin -> template, events, records, python
    ===============================================
    Args:
        plugin:

    Returns:

    """
    return Parser.compile(plugin)
