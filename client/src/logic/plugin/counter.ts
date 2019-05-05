// test in local
export class Counter {
  static template: string =
  `
    <div>
        <h3> {{ count }} </h3>
        <v-btn @click="plus"> Add </v-btn>
    </div>
  `

  public count: number

  constructor () {
    this.count = 0
  }

  public plus () {
    this.count++
  }
}
