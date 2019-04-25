export default {
  methods: {
    register (name, content) {
      this.$socket.emit('register_plugin', {
        plugin_name: name,
        python_file: content
      })
    },
    activate (roomId, plugins) {
      this.$socket.emit('plugin/activate', {
        plugins: plugins, // id
        room_id: roomId
      })
    }
  }
}