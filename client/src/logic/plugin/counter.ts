// ========================
//  Example plugin counter
// ========================
import { BasePlugin } from '../baseplugin'

// test in local
class Counter extends BasePlugin {
  public count: number

  constructor () {
    super('Counter')
    this.count = 0
  }

  public plus () {
    this.count++
  }
}

const counterTemplate: string =
`
  <div>
      <h3> {{ count }} </h3>
      <v-btn @click="plus"> Add </v-btn>
  </div>
`

import { VBtn } from 'vuetify/lib'

export default {
  instance: new Counter(),
  template: counterTemplate,
  addons: { VBtn }
}