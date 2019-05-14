// =====================
//  Example plugin chat
// =====================
import { Comment } from '@/model'
import * as VuetifyComponents from 'vuetify/lib'
import { Plugin } from '../model'

const vuetifyComponents: Record<string, any> = {}
for (const [k, v] of Object.entries(VuetifyComponents)) {
  if (k[0] === 'V') {
    vuetifyComponents[k] = v
  }
}

// test in local
export class ChatServer {
  private comments: Comment[] = []

  public comment (text: string): void {
    // mock
    const comment: Comment = {
      type: 'comment',
      avatar: `https://cdn.vuetifyjs.com/images/lists/${1}.jpg`,
      comment_id: Math.random().toString(36),
      user_name: 'John',
      user_id: 'xxxx',
      text: text,
      commented_at: new Date(),
    }
    this.comments.push(comment)
  }
}

const chatTemplate = `
<div>
  <v-list id="chat" two-line="two-line" height="50%">
    <v-subheader>チャット</v-subheader>
    <template v-for="comment, i in v.comments">
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
        <v-text-field v-model="v.chatInput" label="コメント"></v-text-field>
      </v-flex>
      <v-flex d-flex="d-flex" xs4="xs4" sm4="sm4" md4="md4">
        <v-btn color="info" @click="comment(v.chatInput); v.chatInput = ''">送信</v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</div>
`

// tslint:disable-next-line
const rawPlugin = `
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
`

const chat: Plugin = {
  template: chatTemplate,
  events: ['comment'],
  record: {
    comments: [],
    chatInput: '',
  },
  addons: vuetifyComponents,
}

export default chat
