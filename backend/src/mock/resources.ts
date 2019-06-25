// =========================
// resources.ts
//
// Copyright (c) 2019 i-pu
// =========================

import { Room, PluginMeta } from '@model'

import Counter from '@examples/counter'
import Chat from '@examples/chat'
import Player from '@examples/player'
import Paint from '@examples/paint'
import PlayingCard from '@examples/playingcard'
import Status from '@examples/status'

// roomId -> room
export const roomList: Record<string, Room> = {}

// plugin-id -> pluginMeta
export const pluginMarket: Record<string, PluginMeta> = {
  Counter, Chat, Player, Paint, PlayingCard, Status
}

// socketId -> roomId
export const sessions: Record<string, {
  name: string,
  id: string,
  roomId: string | null,
}> = {}