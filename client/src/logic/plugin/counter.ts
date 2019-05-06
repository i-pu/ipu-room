// ========================
//  Example plugin counter
// ========================
import { BasePlugin } from '../baseplugin'

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

const counterTemplate: string =
`
  <div>
      <h3> {{ count }} </h3>
      <v-btn @click="plus"> Add </v-btn>
  </div>
`

import { VBtn } from 'vuetify/lib'

export default {
  template: counterTemplate,
  addons: { VBtn },
}
