// ========================
//  Example plugin counter
// ========================
import { BasePlugin } from '../baseplugin'
import { Plugin } from '@/logic/plugin/component'

export class CounterServer extends BasePlugin {
  public count: number

  constructor () {
    super('Counter')
    this.count = 0
  }

  public plus () {
    this.count++
  }
}

const counterTemplate: string = `<div><h3> {{ count }} </h3><v-btn @click="plus"> Add </v-btn></div>`

import { VBtn } from 'vuetify/lib'

export const counter: Plugin = {
  template: counterTemplate,
  events: { plus: {} },
  record: { count: 0 },
  addons: { VBtn }
}
