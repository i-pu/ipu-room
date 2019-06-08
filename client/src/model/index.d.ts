import { Component } from 'vue'

// typeof plugin
export interface Plugin {
  // html template
  template: string,
  // functions
  functions: Record<string, string[]>,

  instanceId: string,

  config: {
    enabled: boolean
  }
}

// static plugin info
interface PluginMeta {
  // plugin id
  id: string,
  // plugin name
  thumbnail_url: string,
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
    room: Room,
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
  pluginPackages: Array<{
    plugin: Plugin,
    meta: PluginMeta
  }>,
  plugins: Array<{
    component: Component,
    properties: PluginProperties,
  }>
}

export interface User {
  name: string,
  id: string,
  avatar_url: string
}

