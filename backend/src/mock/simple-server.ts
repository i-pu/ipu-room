// =========================
// simple-server.ts
//
// Copyright (c) 2019 i-pu
// =========================

import SocketIO, { Server } from 'socket.io'
import uuidv4 from 'uuid'
import color from 'colors'
import { createServer } from 'http'
import { Room, PluginPackage } from '@client/model'
import { __compilePlugin_test__ } from '../plugin-compiler/compiler'

import Counter from '../examples/counter'
// import Chat from '@plugin/chat'
// import Player from '@plugin/player'
// import Paint from '@plugin/paint'

const app = createServer()
const io: Server = SocketIO(app)

__compilePlugin_test__()

app.listen(1234, () => {
  console.log(`simple server running on ${color.green.bold('localhost:1234')}`)
})

const activatePlugin = (pluginPackage: PluginPackage): PluginPackage => {
  const newPackage: PluginPackage = JSON.parse(JSON.stringify(pluginPackage))
  newPackage.plugin.instanceId = uuidv4()
  return newPackage
}

// roomId -> room
const roomList: Record<string, Room> = {
  'xxxx-yyyy-zzzz': {
    name: '雑談部屋1',
    id: 'xxxx-yyyy-zzzz',
    // tslint:disable:max-line-length
    thumbnailUrl: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
    members: [],
    pluginPackages: [
      activatePlugin(Counter),
      // activatePlugin(Chat),
      // activatePlugin(Paint),
      // activatePlugin(Player)
    ],
    plugins: [],
  },
}

// plugin-id -> pluginPackage
const pluginMarket: Record<string, PluginPackage> = {
  'counter-0123-abcdef-4567': Counter,
 // 'paint-xxxx-12345678': Paint,
}

// socketId -> roomId
const sessions: Record<string, {
  name: string,
  id: string,
  roomId: string | null,
}> = {}

io.on('connection', (socket) => {
  socket.on('visit', ({ userName }) => {
    sessions[socket.id] = {
      name: userName,
      id: socket.id,
      roomId: '',
    }
    socket.emit('visit', { userId: socket.id })
  })

  socket.on('lobby', ({ userId }) => {
    console.log(`${color.black.bgWhite('[lobby]')} Lobby ${color.yellow(Object.keys(roomList).length.toString())} rooms`)
    socket.emit('lobby', { rooms: Object.values(roomList) })
  })

  socket.on('room/make', ({ roomName, pluginIds }: { roomName: string, pluginIds: string[]}) => {
    const roomId = uuidv4()
    console.log(`${color.black.bgWhite('[room/make]')} ${color.green.bold('+')} ${color.yellow(roomName)} (${color.gray(roomId)})`)

    const pluginPackages = pluginIds
      .filter((id: string) => Object.keys(pluginMarket).includes(id))
      .map((id) => pluginMarket[id])
      .map((pluginPackage) => activatePlugin(pluginPackage))

    roomList[roomId] = {
      name: roomName,
      id: roomId,
      thumbnailUrl: '',
      members: [],
      pluginPackages,
      plugins: [],
    }
    socket.emit('room/make', { room: roomList[roomId] })
  })

  socket.on('room/enter', ({ roomId }: { roomId: string }) => {
    console.log(`${color.black.bgWhite('[room/enter]')} ROOM ${color.gray(roomId)} ${color.green.bold('+')} ${socket.id}`)

    if (!roomList[roomId]) {
      throw new Error(`Room ${roomId} does not exist`)
    }

    const room = roomList[roomId]

    if (!sessions[socket.id] || !room) {
      return
    }

    socket.join(roomId)
    sessions[socket.id].roomId = roomId

    if (!room.members.map((m) => m.id).includes(socket.id)) {
      room.members.push({
        id: socket.id, name: sessions[socket.id].name, avatarUrl: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460',
      })
    }

    console.log(`${color.black.bgWhite('[room/enter]')} Total ${color.yellow(room.pluginPackages.length.toString())} Plugins applied!!`)
    for (const { plugin, meta } of room.pluginPackages) {
      console.log(`${color.black.bgWhite('[room/enter]')}   - ${color.gray(meta.author + '/' + meta.name)} (${plugin.instanceId})`)
    }

    socket.emit('room/enter', { room })
    socket.in(roomId).broadcast.emit('room/update', { room })
  })

  // since v2
  // socket.on('room/event/join', ({}) => {})
  // socket.on('room/event/leave', ({}) => {})

  // socket.on('plugin/event/load', ({}) => {})
  // socket.on('plugin/event/destroy', ({}) => {})

  socket.on('room/compile', ({ ipl }: { ipl: string }) => {

  })

  socket.on('plugin/trigger', ({ roomId, instanceId, data, options }: {
    roomId: string, instanceId: string, data: { event: string, args: any[] }, options: {}
  }) => {
    const { event, args } = data
    console.log(`${color.black.bgWhite('[plugin/trigger]')} ROOM ${color.gray(roomId)} ${color.yellow(instanceId)} ${color.blue(event)}`)
    io.in(roomId).emit(`plugin/${instanceId}/trigger`, { data: { event, args } })
  })

  socket.on('plugin/sync', ({ roomId, instanceId }: { roomId: string, instanceId: string }) => {
    const randomId = roomList[roomId].members.map((m) => m.id).filter((id) => id !== socket.id)[0]
    console.log(`${color.black.bgWhite('[plugin/sync]')} sync request ${color.gray(socket.id)} -> ${color.gray(randomId)}`)
    io.to(randomId).emit(`plugin/${instanceId}/clone`, { roomId, instanceId, from: socket.id })
  })

  socket.on('plugin/clone', ({ roomId, instanceId, record, from }: {
    roomId: string, instanceId: string, record: Record<string, any>, from: string
  }) => {
    console.log(`${color.black.bgWhite('[plugin/clone]')} clone to ${color.gray(socket.id)} -> ${color.gray(from)}`)
    io.to(from).emit(`plugin/${instanceId}/sync`, { record })
  })

  socket.on('room/exit', ({ roomId }: { roomId: string }) => {
    leaveRoom(roomId)
    socket.emit('room/exit')
  })

  socket.on('disconnect', () => {
    if (sessions[socket.id] && sessions[socket.id].roomId) {
      leaveRoom(sessions[socket.id].roomId!!)
    }
    delete sessions[socket.id]
  })

  const leaveRoom = (roomId: string) => {
    console.log(`${color.black.bgWhite('[room/exit]')} ${color.gray(roomId)} ${color.red.bold('-')} ${color.gray(socket.id)}`)
    roomList[roomId].members = roomList[roomId].members.filter((m) => m.id !== socket.id)

    sessions[socket.id].roomId = ''

    if (roomList[roomId].members.length === 0) {
      // remain room for sometimes
      // delete roomList[roomId]
    }

    io.in(roomId).emit('room/update', { room: roomList[roomId] })
  }
})

io.listen(3000)
