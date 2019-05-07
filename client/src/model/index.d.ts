export interface Comment {
  type: string,
  avatar: string,
  comment_id: string,
  user_name: string,
  user_id: string,
  text: string,
  commented_at: Date
}

import { Component } from 'vue'
import { PluginConfig } from '@/logic/plugin/component'
import { BasePlugin } from '@/logic/baseplugin'

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

