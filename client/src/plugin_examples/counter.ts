// ==========================
//  Example plugin counter
// ========================

import { Plugin } from '@/model'

const counter: Plugin = {
  template: `<div><h3> {{ count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
  functions: {
    plus (this: { count: number }) {
      this.count++
      return [this.count]
    }
  }
}

export default counter
