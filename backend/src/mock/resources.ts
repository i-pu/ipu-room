// =========================
// resources.ts
//
// Copyright (c) 2019 i-pu
// =========================

import { Room, PluginMeta } from '@model'
import Counter from '@examples/counter'

// roomId -> room
export const roomList: Record<string, Room> = {}

// plugin-id -> pluginMeta
export const pluginMarket: Record<string, PluginMeta> = {
  [Counter.id]: Counter
}

// socketId -> roomId
export const sessions: Record<string, {
  name: string,
  id: string,
  roomId: string | null,
}> = {}