import unittest

from app.plugin.compiler import plugin_compiler


class TestCompiler(unittest.TestCase):
    def test_compiler(self):
        plugin = \
            '''
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
        expect_template = \
            '''
<html>
  <div>
{{v.count }}
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
        expect_python = \
            '''
class Plugin():
    def __init__(self):
        self.count = 0

    def plus(self, data):
        self.count += data
        return ['count']
'''

        template, events, records, python, addons = plugin_compiler(plugin)

        exec(python)
        obj = eval('Plugin()')

        self.assertEqual(['plus'], events)
        self.assertEqual({}, records)
        self.assertEqual(expect_template, template)
        self.assertEqual(expect_python, python)
        self.assertEqual(['VBtn'], addons)
