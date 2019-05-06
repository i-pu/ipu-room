export class BasePlugin {
  [trigger: string]: any
  public pluginName: string
  public enabled: boolean = true

  constructor (name: string) {
    this.pluginName = name
  }
}
