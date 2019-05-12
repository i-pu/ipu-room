import unittest

from src.plugin.compiler import plugin_compiler


class TestCompiler(unittest.TestCase):
    def test_compiler(self):
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
        print('plugin:-----')
        print(plugin)

        template, events, records, python, addons = plugin_compiler(plugin)

        exec(python)
        obj = eval('Plugin()')

        print('events: {}'.format(events))
        print('records: {}'.format(records))
        print('template: \n {}'.format(template))
        print('python: \n {}'.format(python))
        print('addons: \n {}'.format(addons))
