export interface Comment {
  type: string,
  avatar: string,
  comment_id: string,
  user_name: string,
  user_id: string,
  text: string,
  commented_at: Date
}

import { PluginComponent } from '@/logic/plugin/component'
import { BasePlugin } from '@/logic/baseplugin'

export interface Room {
  room_name: string,
  room_id: string,
  thumbnail_url: string,
  members: User[],
  plugins: Array<{ component: PluginComponent, config: { name: string, enabled: boolean } }>
}

export interface User {
  name: string,
  id: string,
  avatar_url: string
}
