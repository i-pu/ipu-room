<template lang='pug'>
  div
    v-container(fluid grid-list-md)
      v-layout(row wrap)
        v-flex(
          v-for="room in rooms" :key="room.room_id"
          d-flex xs12 sm6 md3
        )
          v-card
            v-img(:src="room.thumbnail_url" height="200px")
            v-card-title
              h3.headline {{ room.room_name }}
            v-card-text
              template(v-for="member, i in room.members")
                v-tooltip.mr-2(top :key="i")
                  template(v-slot:activator="{ on }")
                    v-avatar(v-on="on" size="60")
                      img(:src="member.avatar_url")
                  span {{ member.name }}
            v-card-actions
              v-btn(color="info" @click="join(room.room_id)") 入室
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

import { Room } from '@/model'

@Component<RoomList>({})
export default class RoomList extends Vue {
  @Prop() public userId!: string
  @Prop() public rooms!: Room[]

  private roomNameInput: string = ''

  public join (roomId: string) {
    this.$router.push({
      path: `/room/${roomId}`,
      params: {
        roomId,
      },
    })
    // this.$socket.emit('enter_room', { room_name: this.roomNameInput })
  }
}
</script>