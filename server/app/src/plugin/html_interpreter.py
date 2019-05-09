from html.parser import HTMLParser
import re
import random
import string
from uuid import uuid4
from textwrap import dedent
import importlib.machinery as imm

class Parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    # current tag's info
    self.tag = ''
    self.attrs = {}
    # flags
    self.in_template = False
    self.in_python = False
    # result
    self.template = ''
    self.events = []
    self.records = dict()
    self.python = ''

  def handle_starttag(self, tag, attrs):
    self.tag = tag
    self.attrs = dict(attrs)

  def handle_data(self, content):
    if self.tag == '':
      return
    else:
      if self.tag == 'html':
        self.in_template = True
        self.in_python = False
      if self.tag == 'python':
        self.in_template = False
        self.in_python = True
      if self.in_template:
        # records
          matched = re.match(r'.*\{\{(.*)\}\}.*', content)
          if matched:
            record, = matched.groups()
            self.records[record.strip()] = None
          # events
          if '@click' in self.attrs:
            expr = self.attrs.get('@click')
            event, args = re.match('^(.*)\(?(.*)\)?$', expr).groups()
            self.events.append(event)

    if self.in_python:
      self.python = dedent(content)

  def handle_endtag(self, tag):
    self.tag = ''
    self.attrs = {}

  @staticmethod
  def compile(plugin):
    parser = Parser()
    print(plugin)
    parser.feed(plugin)
    parser.template = re.sub(r'.*\{\{\s*(.*)\}\}.*', r'{{v.\1}}' , plugin)

    g = {}
    exec(parser.python, g)
    instance = g['Plugin']()
    methods = list(set(filter(lambda method: method[0] != '_', dir(instance))) - set(vars(instance)))
    variables = dict.keys(vars(instance))

    # check variables
    for record in parser.records:
      if record in variables:
        parser.records[record] = vars(instance)[record]
      else:
        print('Compile error record: {} is undefined'.format(record))

    # check methods
    for event in parser.events:
      if event in methods:
        None
      else:
        print('Compile error event: {} is undefined'.format(event))

    # event test
    ## same as `instance.plus(1)`
    changed = eval('instance.{}(*args)'.format('plus'), { 'instance': instance }, { 'args': [1] })

    ## sync instance's variables to records
    for change in changed:
      if change in dict.keys(parser.records):
        parser.records[change] = instance.__dict__[change]

    # count == 1
    print(parser.records)

    return parser.template, parser.events, parser.records, parser.python