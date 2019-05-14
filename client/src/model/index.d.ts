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

// typeof plugin config
export interface PluginConfig {
  //
  room_id: string,
  // plugin id
  plugin_id: string,
  // unique id
  id: string, 
  // plugin name
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string,
  // plugin enabled
  enabled: boolean
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
  plugins: Array<{ component: Component, config: PluginConfig }>
}

export interface User {
  name: string,
  id: string,
  avatar_url: string
}

