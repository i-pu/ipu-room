// test in local
export class SamplePlugin {
  public count: number

  constructor () {
    this.count = 0
  }

  public plus () {
    this.count++
    console.log(this.count)
  }
}
