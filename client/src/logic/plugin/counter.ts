// ========================
//  Example plugin counter
// ========================
import { BasePlugin } from '../baseplugin'

// test in local
export class Counter extends BasePlugin {
  public count: number

  constructor () {
    super()
    this.count = 0
  }

  public plus () {
    this.count++
  }
}

export const counterTemplate: string =
`
  <div>
      <h3> {{ count }} </h3>
      <v-btn @click="plus"> Add </v-btn>
  </div>
`
