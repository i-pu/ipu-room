import { Component } from 'vue'

// typeof plugin
export interface Plugin {
  // html template
  template: string,
  // functions
  functions: Record<string, (...args: any[]) => { functionName: string, args: any[], to?: string }>
}

// static plugin info
export interface PluginMeta {
  // plugin id
  plugin_id: string,
  // plugin name
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string
}

// instance info
export interface PluginProperties {
  record: Record<string, any>,
  env: {
    instanceId: string,
    room: Room
  },
  meta: PluginMeta
}

export interface Comment {
  type: string,
  avatar: string,
  comment_id: string,
  user_name: string,
  user_id: string,
  text: string,
  commented_at: Date
}

export interface Room {
  name: string,
  id: string,
  thumbnail_url: string,
  members: User[],
  plugins: Array<{
    component: Component,
    meta: PluginMeta, 
    properties: PluginProperties
  }>
}

export interface User {
  name: string,
  id: string,
  avatar_url: string
}

