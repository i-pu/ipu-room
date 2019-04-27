from .html_interpreter import Parser


def plugin_compiler(plugin):
    """
    ===== plugin_compiler.py ========
      plugin -> html, events, python
    =================================
    Args:
        plugin: 

    Returns:

    """
    return Parser.compile(plugin)


if __name__ == "__main__":
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
