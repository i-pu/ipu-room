<template lang='pug'>
  div
    v-layout(row justify-center)
      v-dialog(v-model="dialog" max-width="600px")
        template(v-slot:activator="{ on }")
          v-btn(color="success" @click="fetchPluginData" v-on="on") 部屋を作成
        v-card
          v-card-title
            span.headline 部屋を作成
          v-card-text
            v-container(grid-list-md)
              v-layout(wrap)
                v-flex(xs12 sm12)
                  v-text-field(label="部屋名" required v-model="roomNameInput")
                v-flex(xs12 sm12)
                  v-select(
                    v-model="selectedPlugins"
                    item-text="label"
                    item-value="value"
                    :items="myPlugins"
                    label="プラグイン"
                    multiple
                  )
                    template(v-slot:selection="{ item, index }")
                      v-chip(v-if="index === 0")
                        span {{ item.label }}
          v-card-actions
            v-spacer
            v-btn(color="blue darken-1" flat @click="requestCreateRoom") 作成
</template>

<script lang="ts">
import { createComponent, SetupContext, ref } from '@vue/composition-api'
import { Room, PluginPackage, PluginMeta } from '@/model'
import socket from '@/socket'

export default createComponent({
  props: {
    userId: String,
  },
  setup (props: { userId: string }, { root }: SetupContext) {
    const dialog = ref<boolean>(false)
    const roomNameInput = ref<string>('')
    const myPlugins = ref<Array<{ label: string, value: string }>>([])
    const selectedPlugins = ref<string[]>([])

    const fetchPluginData = async () => {
      const metas: PluginMeta[] = await fetch(`${process.env.VUE_APP_API_ORIGIN}/market/plugins`)
        .then((res) => res.json())

      myPlugins.value = metas.map((meta) => ({
        label: `${meta.author}/${meta.name} v${meta.version}`,
        value: meta.id,
      }))
    }

    socket.on('room/create', (res: { room: Room }) => {
      root.$emit('add', res)
    })

    const requestCreateRoom = () => {
      socket.emit('room/create', {
        roomName: roomNameInput.value,
        plugins: selectedPlugins.value,
      })
      dialog.value = false
      roomNameInput.value = ''
    }

    const addRoom = (res: { room: Room }) => {
      root.$emit('add', res)
    }

    return {
      dialog, roomNameInput, myPlugins, selectedPlugins,
      fetchPluginData, requestCreateRoom, addRoom,
    }
  },
})
</script>