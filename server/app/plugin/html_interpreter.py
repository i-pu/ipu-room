"""
html_interpreter.py
"""
from html.parser import HTMLParser

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
        id = 'hoge'

        if 'event' in self.attrs:
          self.events.append(
            {
              'id': id,
              # TODO parse args
              'event': self.attrs.get('event'),
              'args': []
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