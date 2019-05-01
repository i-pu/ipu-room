// test in local
export class SamplePlugin {
  private count: number

  constructor () {
    this.count = 0
  }

  public plus (data: string) {
    this.count += parseInt(data, 10)
    return { changed: 'count' }
  }
}
