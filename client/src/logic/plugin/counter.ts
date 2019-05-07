// ========================
//  Example plugin counter
// ========================
import { Plugin } from '@/logic/plugin/component'
import { VBtn } from 'vuetify/lib'

export class CounterServer {
  public count: number = 0

  public plus () {
    this.count++
  }
}

const counter: Plugin = {
  template: `<div><h3> {{ count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
  events: ['plus'],
  record: { count: 0 },
  addons: { VBtn }
}

export default counter
