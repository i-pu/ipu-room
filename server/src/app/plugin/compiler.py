from .html_interpreter import compile

"""
From the html template, extract `events`, `records`, and `python`
"""
# sample counter plugin
counter_plugin = '''
<html>
  <div>
    <h3> {{ count }} </h3>
    <v-btn @click="plus"> Add </v-btn>
  </div>
</html>
<python>
  class Plugin():
    def __init__(self):
      self.events = ['plus']
      self.count = 0

    def constructor(self):
      return { count: self.count }

    def plus(data):
      self.count += data
      return { count: self.count }
</python>
  '''

# sample chat plugin
chat_plugin = """
<html>
  <div>
    <v-list id="chat" two-line="two-line" height="50%">
      <v-subheader>チャット</v-subheader>
      <template v-for="comment, i in comments">
        <v-list-tile v-if="comment.type === 'comment'" :key="comment.comment_id" avatar="avatar">
          <v-list-tile-avatar>
            <img :src="comment.avatar"/>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{ comment.text }}</v-list-tile-title>
            <v-list-tile-sub-title>{{ comment.user_name }}</v-list-tile-sub-title>
          </v-list-tile-content>
        </v-list-tile>
      </template>
    </v-list>
    
    <v-container fluid="fluid" grid-list-md="grid-list-md" text-xs-center="text-xs-center">
      <v-layout row="row" wrap="wrap">
        <v-flex d-flex="d-flex" xs8="xs8" sm8="sm8" md8="md8">
          <v-text-field v-model="chatInput" label="コメント"></v-text-field>
        </v-flex>
        <v-flex d-flex="d-flex" xs4="xs4" sm4="sm4" md4="md4">
          <v-btn color="info" @click="comment(chatInput); chatInput = ''">送信</v-btn>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</html>
<python>
class Plugin():
  def __init__(self):
    self.comments = []
    self.chatInput = ''
  def comment(self, comment_text):
    comment = {
      type: 'comment',
      avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
      comment_id: uuidv4(),
      user_name: 'John',
      user_id: 'xxxx',
      text: comment_text
    }
    self.comments.append(comment)
    return ['comments']
</python>
"""

# youtube plugin
youtube_plugin = """
<html>
  <div>
    <v-btn> Test </v-btn>
    <player :video-id="videoid" player-width="1280" player-height="750" :player-vars="{autoplay: 1}" />
  </div>
</html>
<python>
class Plugin():
  def __init__(self):
    self.videoid = 'SX_ViT4Ra7k'
</python>
"""


def plugin_compiler(plugin_content):
    return compile(plugin_content)


# test
# template, events, records, python, addons = plugin_compiler(counter_plugin)
# print('template: \n{}'.format(template))
# print('{} {} {}'.format(events, records, addons))
