export class BasePlugin {
  [trigger: string]: any
  public pluginName: string

  constructor (name: string) {
    this.pluginName = name
  }
}
