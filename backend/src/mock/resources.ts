// =========================
// resources.ts
//
// Copyright (c) 2019 i-pu
// =========================

import { Room, PluginMeta, PluginPackage } from '@client/model'
import Counter from '../examples/counter'
import { compilePlugin } from './../plugin-compiler/compiler'
// import Chat from '@plugin/chat'
// import Player from '@plugin/player'
// import Paint from '@plugin/paint'

export const activate = async (meta: PluginMeta): Promise<PluginPackage> => {
  try {
    const plugin = await compilePlugin(meta.content)
    return { plugin, meta }
  } catch (error) {
    throw error
  }
}

// roomId -> room
export const roomList: Record<string, Room> = {
  'xxxx-yyyy-zzzz': {
    name: '雑談部屋1',
    id: 'xxxx-yyyy-zzzz',
    // tslint:disable:max-line-length
    thumbnailUrl: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
    members: [],
    pluginPackages: [],
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