import Vue from 'vue'
import { Mixin } from 'vue-mixin-decorator'

@Mixin
export default class Plugin extends Vue {
  public register (name: string, content: string) {
    this.$socket.emit('register_plugin', {
      plugin_name: name,
      python_file: content,
    })
  }

  public activate (roomId: string, plugins: string[]) {
    this.$socket.emit('plugin/activate', {
      plugins, // id
      room_id: roomId,
    })
  }
}
