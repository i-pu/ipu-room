import { Component } from 'vue'

// typeof plugin
export interface Plugin {
  // html template
  template: string,
  // trigger methods' name
  events: string[],
  // variables in plugin
  record: Record<string, any>,
  // custom component that be used in
  addons: Record<string, string>
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
export interface PluginConfig {
  room_id: string,
  enabled: boolean,
  // plugin unique instance id
  id: string
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
    config: PluginConfig
  }>
}

export interface User {
  name: string,
  id: string,
  avatar_url: string
}

