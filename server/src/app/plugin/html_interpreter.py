""" =====================
  html_interpreter.py
     by wakame_tech
======================"""

from html.parser import HTMLParser
import re
import random
import string
from uuid import uuid4
from textwrap import dedent
import importlib.machinery as imm

class Parser(HTMLParser):
  HTML_TAGS = ['html', 'head', 'title', 'base', 'link', 'style', 'meta', 'body', 'article', 'section', 'nav', 'aside','h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'footer', 'address', 'p', 'hr', 'pre', 'blockquote','ol', 'ul', 'li', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'main', 'div', 'a', 'em', 'strong','small', 's', 'cite', 'g', 'dfn', 'abbr', 'code', 'var', 'samp', 'kbd', 'data', 'sub', 'sup', 'time','i', 'b', 'u', 'mark', 'ruby', 'rb', 'rt', 'rtc', 'rp', 'bdi', 'bdo', 'span', 'br', 'wbr', 'ins','del', 'img', 'picture', 'iframe', 'embed', 'object', 'param', 'video', 'audio', 'track', 'source','map', 'area', 'table', 'caption', 'calgroup', 'col', 'tbody', 'thead', 'thoot', 'tr', 'td', 'th','form', 'fieldset', 'legend', 'label', 'input', 'select', 'option', 'optgroup', 'textarea', 'button','datalist', 'output', 'progress', 'meter', 'script', 'noscript', 'canvas', 'details', 'summary','menu', 'menuitem']

  def __init__(self):
    HTMLParser.__init__(self)
    self.in_template = False
    self.in_python = False
    # result
    self.template = ''
    self.events = []
    self.records = dict()
    self.python = ''
    self.addons = []

  def handle_starttag(self, tag, attrs):
    if tag == 'html': 
      self.in_template = True
      return
    if tag == 'python':
      self.in_python = True
      return
    # customtag
    # TODO: self-ended tag cannot handle
    if tag not in Parser.HTML_TAGS:
      custom_tag = tag.capitalize()
      custom_tag = re.sub('-(.)', lambda x:x.group(1).upper(), custom_tag)
      # print('[Plugin Compiler] detect custom tags {}'.format(custom_tag))
      self.addons.append(custom_tag)

    # analysis attrs
    for (attr, value) in attrs:
      # ':hoge="foo"', 'v-bind:hoge="foo"'
      if attr[0] == ':' or attr.split(':')[0] == 'v-bind':
        # is variable check
        if value.strip().isalnum():
          self.records[value] = None
      # '@event="foo(bar)"', 'v-on:hoge="foo"'
      if attr[0] == '@' or attr.split(':')[0] == 'v-on':
        event, args = re.match('^(.*)(?:\((.*)\)).*$', value).groups()
        print('[Plugin Compiler] detect event {}'.format(event))
        self.events.append(event)

  def handle_data(self, content):
    if self.in_python: 
      self.python = dedent(content)
      self.in_python = False
      return
    else:
      # records
      matched = re.match(r'.*\{\{(.*)\}\}.*', content)
      if matched:
        record, = matched.groups()
        record = record.strip()
        record = record.split('.')[0]
        print('[Plugin Compiler] detect variable {}'.format(record))
        self.records[record] = None

def compile(plugin):
    parser = Parser()
    parser.feed(plugin)

    # {{ hoge }} -> {{ v.hoge }}
    parser.template = re.sub(r'.*\{\{\s*(.*)\}\}.*', r'{{v.\1}}' , plugin)

    # emulate plugin to extract methods and member variables
    try:
      gbl = {}
      exec(parser.python, gbl)
      instance = gbl['Plugin']()
    except Exception as e:
      # Plugin error
      print('plugin compile error')
      return
    else:
      # check variables
      for var in dict.keys(vars(instance)):
        parser.records[var] = vars(instance)[var]

      # check methods
      methods = list(set(filter(lambda method: method[0] != '_', dir(instance))) - set(vars(instance)))
      for event in parser.events:
        if event in methods:
          None
        else:
          print('Compile error event: {} is undefined'.format(event))

      print('compiled {}'.format('Plugin'))

      # event test
      ## same as `instance.plus(1)`
      # changed = eval('instance.{}(*args)'.format('plus'), { 'instance': instance }, { 'args': [1] })

      ## sync instance's variables to records
      # for change in changed:
      #   if change in dict.keys(parser.records):
      #     parser.records[change] = instance.__dict__[change]
      # count == 1
      print(parser.records)

      return parser.template, parser.events, parser.records, parser.python, parser.addons
