// ========================
//  Example plugin counter
// ========================
import { Plugin } from '@/model'

export class CounterServer {
  public count: number = 0

  public plus () {
    this.count++
  }
}

import { VBtn } from 'vuetify/lib'

const counter: Plugin = (() => {
  return {
    template: `<div><h3> {{ v.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
    events: ['plus'],
    record: { count: 0 },
    addons: { VBtn },
  }
})()

export default counter
