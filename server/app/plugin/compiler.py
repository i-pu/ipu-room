'''
===== plugin_compiler.py ========
  plugin -> html, events, python
=================================
'''
from html_interpreter import Parser

def plugin_compiler(plugin):
  return Parser.compile(plugin)

html, events, python = plugin_compiler(
'''
<html>
  <button event="plus(1)"> カウント </button>
  <p> {{count}} </p>
</html>
<python>
class Plugin():
  count = 0

  @classmethod
  def on_plus(cls, data):
    cls.count += data
    return { 'count': cls.count }

  @classmethod
  def all(cls) -> dict:
    return {
      'plus': cls.on_plus
    }
</python>
'''
)

print('html:\n {}'.format(html))
print('events:\n {}'.format(events))
print('python:\n {}'.format(python))