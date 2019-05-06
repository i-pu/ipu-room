export class BasePlugin {
  [trigger: string]: any
  public name: string
  public enabled: boolean = true

  constructor (name: string) {
    this.name = name
  }
}
