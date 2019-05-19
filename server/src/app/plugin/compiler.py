# =========================
# compiler.py
#
# Copyright (c) 2019 i-pu
# =========================

from html.parser import HTMLParser
import re
from textwrap import dedent

class Parser(HTMLParser):
    HTML_TAGS = [
        'html', 'head', 'title', 'base', 'link', 'style', 'meta', 'body', 'article', 'section', 'nav', 'aside',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'footer', 'address', 'p', 'hr', 'pre', 'blockquote',
        'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'main', 'div', 'a', 'em', 'strong',
        'small', 's', 'cite', 'g', 'dfn', 'abbr', 'code', 'var', 'samp', 'kbd', 'data', 'sub', 'sup', 'time',
        'i', 'b', 'u', 'mark', 'ruby', 'rb', 'rt', 'rtc', 'rp', 'bdi', 'bdo', 'span', 'br', 'wbr', 'ins',
        'del', 'img', 'picture', 'iframe', 'embed', 'object', 'param', 'video', 'audio', 'track', 'source',
        'map', 'area', 'table', 'caption', 'calgroup', 'col', 'tbody', 'thead', 'thoot', 'tr', 'td', 'th',
        'form', 'fieldset', 'legend', 'label', 'input', 'select', 'option', 'optgroup', 'textarea', 'button',
        'datalist', 'output', 'progress', 'meter', 'script', 'noscript', 'canvas', 'details', 'summary',
        'menu', 'menuitem'
    ]

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_template = False
        self.in_python = False
        # result
        self.template = ''
        self.events = []
        self.record = dict()
        self.python = ''
        self.addons = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'html': 
            self.in_template = True
            return
        if tag == 'python':
            self.in_python = True
            return
        if tag not in Parser.HTML_TAGS:
            custom_tag = tag.capitalize()
            custom_tag = re.sub('-(.)', lambda x:x.group(1).upper(), custom_tag)
            # print('[Plugin Compiler] detect custom tags {}'.format(custom_tag))
            self.addons.add(custom_tag)

        # analysis attrs
        for (attr, value) in attrs:
            # ':hoge="foo"', 'v-bind:hoge="foo"'
            if attr[0] == ':' or attr.split(':')[0] == 'v-bind':
                # is variable check
                if value.strip().isalnum():
                    self.record[value] = None
            # '@event="foo(bar)"', 'v-on:hoge="foo"'
            if attr[0] == '@' or attr.split(':')[0] == 'v-on':
                res = re.match(r'([a-z]\w*)(?:\((.*)?\))?', value)
                if res:
                    event, args = res.groups()
                    # print('[Plugin Compiler] detect event {}'.format(event))
                    self.events.append(event)

    def handle_data(self, content):
        if self.in_python: 
            self.python = dedent(content)
            self.in_python = False
            return
        else:
            # record
            matched = re.match(r'.*\{\{(.*)\}\}.*', content)
            if matched:
                var_name, = matched.groups()
                var_name = var_name.strip()
                # only v.* regards as plugin variables
                prefix = var_name.split('.')[0]
                if prefix == 'v':
                    var_name = var_name.split('.')[1]
                    print('[Plugin Compiler] detect variable {}'.format(var_name))
                    self.record[var_name] = None

def compile(plugin):
    """
    From the html template, extract events, record, and python

    Parameters
    ----------
    plugin : string
        A content of a plugin (*.ipl)
    
    Returns
    -------
    template : string
        A plugin html that'll be passed to a client.
    events : array
        Names of event
    record : dict
        A set of variable's key and variable's value.
    python : string
        A python code that'll be run as a socket server.
    addons : array
        A set of custom tags such as Vuetify's component.
    """
    parser = Parser()
    parser.feed(plugin)

    res = re.match(r'.*<html>(.*)</html>.*', plugin, flags = re.DOTALL)
    if res:
        parser.template, = res.groups()

    # emulate plugin to extract methods and member variables
    try:
        gbl = {}
        exec(parser.python, gbl)
        instance = gbl['Plugin']()
    except Exception as e:
        # Plugin error
        print('[Plugin Compiler] An error occured while emulating plugoin instance.')
        return
    else:
        # check variables
        for var_name in dict.keys(vars(instance)):
            # reserved variable names
            if var_name not in ['events']:
                parser.record[var_name] = vars(instance)[var_name]

        # check methods
        methods = list(set(filter(lambda method: method[0] != '_', dir(instance))) - set(vars(instance)))
        for event in parser.events:
            if event in methods:
                None
            else:
                print('[Plugin Compiler] error event: {} is undefined'.format(event))

        print('compiled {}'.format('Plugin'))

        # event test
        ## same as `instance.plus(1)`
        # changed = eval('instance.{}(*args)'.format('plus'), { 'instance': instance }, { 'args': [1] })

        ## sync instance's variables to record
        # for change in changed:
        #   if change in dict.keys(parser.record):
        #     parser.record[change] = instance.__dict__[change]
        # count == 1

        print(parser.record)

        return parser.template, parser.events, parser.record, parser.python, list(parser.addons)