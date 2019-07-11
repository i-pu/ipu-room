// =========================
// resources.ts
//
// Copyright (c) 2019 i-pu
// =========================

import { Room, PluginMeta } from '@model'

// roomId -> room
export const roomList: Record<string, Room> = {}

// plugin-id -> pluginMeta
export const pluginMarket: Record<string, PluginMeta> = {}

// socketId -> roomId
export const sessions: Record<string, {
  name: string,
  id: string,
  roomId: string | null,
}> = {}