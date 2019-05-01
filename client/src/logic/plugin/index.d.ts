export interface Element {
  id: string, type: string
}

export interface View extends Element {
  id: string, type: 'view', bind: string, template: string
}

export interface Event extends Element {
  id: string, type: 'event', event: string
}
