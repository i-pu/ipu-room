from html_interpreter import Parser

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

if __name__ == "__main__":
  plugin = '''
    <html>
      <div>
        <h3> {{ count }} </h3>
        <v-btn @click="plus"> Add </v-btn>
      </div>
    </html>
    <python>
    class Plugin():
      def __init__(self):
        self.count = 0

      def plus(self, data):
        self.count += data
        return ['count']
    </python>
  '''

  template, events, records, python = plugin_compiler(plugin)

  print('events: {}'.format(events))
  print('records: {}'.format(records))
  print('template: \n {}'.format(template))
  print('python: \n {}'.format(python))
