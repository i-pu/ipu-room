<template lang='pug'>
  div(v-if="room")
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.name }}
            v-spacer
            settings(:room="room" @add-plugin="addPlugin")
            v-btn(color="error" @click="requestExitRoom") 退出

    desk#desk(:room="room")

    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-card(white)
            status#status(:members="room.members")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

import { Room, User, Plugin, PluginProperties, PluginMeta } from '@/model'

import Desk from '@/components/room/Desk.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

import { ROOMS_MOCK } from '@/api/mock'
import { compile } from '@/logic/compiler'

// import * as Package from '@/plugin_examples/counter'
// import * as Package from '@/plugin_examples/chat'
import * as Package from '@/plugin_examples/paint'

@Component<RoomView>({
  components: { Desk, Status, Settings },
  sockets: {
    'room/enter' (data: { room: Room }) {
      // mock
      this.responseEnterRoom({ room: ROOMS_MOCK[0] })
    },
    'room/exit' (data: {}) {
      this.responseExitRoom()
    },
    'room/exit-event' ({ members }: { members: User[] }) {
      this.room!!.members = members
    },
    'plugin/info' ({ plugin, properties }: { plugin: Plugin, properties: PluginProperties }) {
      this.addPlugin(plugin, properties)
    },
  },
})
export default class RoomView extends Vue {
  private room: Room | null = null

  private get roomId (): string {
    return this.$route.params.roomId
  }

  private mounted () {
    this.requestEnterRoom({ room_id: this.roomId })
  }

  private requestEnterRoom (data: { room_id: string }) {
    console.log(`[Room] request enter`)
    this.$socket.emit('room/enter', { room_id: this.roomId })

    // if (this.$store.getters.localOnly) {
    //   this.responseEnterRoom({ room: ROOMS_MOCK[0] })
    // } else {
    //   this.$socket.emit('room/enter', { room_id: this.roomId })
    // }
  }

  private responseEnterRoom ({ room }: { room: Room }) {
    console.log(`[Room] entered`)
    this.room = {
      ...room,
      plugins: []
    }
    if (this.$store.getters.localOnly) {
      const initializeFn = new Function(...Package.plugin.functions['initialize'])
      const properties: PluginProperties = {
        record: initializeFn(),
        env: { instanceId: 'xxxx-yyyy-zzzz', room: this.room },
        meta: Package.meta,
      }
      this.addPlugin(Package.plugin, properties)
      // const properties: PluginProperties = {
      //   record: new Function(...COUNTER_PLUGIN.functions.initialize)(),
      //   env: {
      //     instanceId: 'xxxx-yyyy-zzzz',
      //     room: this.room,
      //   },
      //   meta: COUNTER_META,
      // }
      // this.addPlugin(COUNTER_PLUGIN, properties)

      // const properties: PluginProperties = {
      //   record: CHAT_RECORD,
      //   env: {
      //     instanceId: 'xxxx-yyyy-zzzz',
      //     room: this.room
      //   },
      //   meta: CHAT_META
      // }
      // this.addPlugin(CHAT_PLUGIN, properties)
    } else {
      this.$socket.emit('plugin/info', { room_id: this.room.id })
    }
  }

  private async addPlugin (plugin: Plugin, properties: PluginProperties) {
    const component = await compile(plugin, properties)
    // component.sealedOptions.methods.clone()
    this.room!!.plugins.push({ component, properties })
  }

  private requestExitRoom () {
    if (this.$store.getters.localOnly) {
      this.responseExitRoom()
    } else {
      this.$socket.emit('room/exit', {})
    }
  }

  private responseExitRoom () {
    this.$router.push('/lobby')
  }
}
</script>

<style scoped>
#desk {
  height: 100%;
}

#status {
  height: 300px;
}

v-card {
  height: 100%;
}
</style>
