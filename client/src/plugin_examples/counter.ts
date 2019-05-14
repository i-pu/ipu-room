// ========================
//  Example plugin counter
// ========================

/*
  Plugin rule

  1. all plugin variables is under the v object
*/

import { Plugin } from '@/model'

export const rawPlugin = `
<html>
  <div>
    <h3> {{ v.count }} </h3>
    <v-btn @click="plus"> Add </v-btn>
  </div>
</html>
<pyhton>
  class Plugin():
    def __init__(self):
      self.count = 0
    def plus(data):
      self.count += data
      return ['count']
</pyhton>
`

export class CounterServer {
  public count: number = 0

  public plus () {
    this.count++
  }
}

import { VBtn } from 'vuetify/lib'

const counter: Plugin = {
  template: `<div><h3> {{ v.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
  events: ['plus'],
  record: { count: 0 },
  addons: { VBtn },
}

export default counter
