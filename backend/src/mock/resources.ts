// =========================
// resources.ts
//
// Copyright (c) 2019 i-pu
// =========================

import { Room, PluginMeta } from '@client/model'
import Counter from '../examples/counter'
// import Chat from '@plugin/chat'
// import Player from '@plugin/player'
// import Paint from '@plugin/paint'

// roomId -> room
export const roomList: Record<string, Room> = {
  'xxxx-yyyy-zzzz': {
    name: '雑談部屋1',
    id: 'xxxx-yyyy-zzzz',
    // tslint:disable:max-line-length
    thumbnailUrl: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
    members: [],
    pluginPackages: [
      // activatePlugin(Chat),
      // activatePlugin(Paint),
      // activatePlugin(Player)
    ],
    plugins: [],
  },
}

// plugin-id -> pluginMeta
export const pluginMarket: Record<string, PluginMeta> = {
  'counter': Counter,
}

// socketId -> roomId
export const sessions: Record<string, {
  name: string,
  id: string,
  roomId: string | null,
}> = {}