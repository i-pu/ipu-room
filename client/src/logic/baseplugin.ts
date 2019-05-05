export class BasePlugin {
  [trigger: string]: any
  static template: string = '<p> Hello, Plugin </p>'

  constructor () {
    
  }
}