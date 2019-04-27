"""
html_interpreter.py
"""
from html.parser import HTMLParser
import re
import random
import string

def uuidv4():
  x = lambda: string.hexdigits[random.randint(0, 15)]
  h = lambda digits: ''.join([x() for _ in range(0, digits)])
  return h(8) + '-' + h(4) + '-' + h(4) + '-' + h(4) + '-' + h(12)

class Parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    # current tag's info
    self.tag = ''
    self.attrs = {}
    # flags
    self.in_html = False
    self.in_python = False
    # result
    self.html = ''
    self.events = []
    self.python = ''

  def handle_starttag(self, tag, attrs):
    self.tag = tag
    self.attrs = dict(attrs)

  def handle_data(self, content):
    if self.tag == '':
      return
    else:
      if self.tag == 'html':
        self.in_html = True
        self.in_python = False
      if self.tag == 'python':
        self.in_html = False
        self.in_python = True

      if self.in_html:
        # template
        matched = re.match(r'.*\{\{(.*)\}\}.*', content)
        if matched:
          template, = matched.groups()
          print('template: {}'.format(template))
          # TODO replace {{ hoge }}
        # event
        if 'event' in self.attrs:
          event = self.attrs.get('event')
          name, args_str = re.match('^(.*)\((.*)\)$', event).groups()
          self.events.append(
            {
              'id': uuidv4(),
              'event': name,
              'args': args_str.split(',')
            }
          )

        self.html += '<{} id="{}"> {}'.format(self.tag, id, content.strip())

      if self.in_python:
        self.python += content.strip()

  def handle_endtag(self, tag):
    if self.in_html:
      self.html += '</{}>'.format(tag)
    self.tag = ''
    self.attrs = {}

  @staticmethod
  def compile(plugin):
    parser = Parser()
    parser.feed(plugin)
    return parser.html, parser.events, parser.python