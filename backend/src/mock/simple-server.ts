// =========================
// simple-server.ts
//
// Copyright (c) 2019 i-pu
// =========================

import SocketIO, { Server } from 'socket.io'
import uuidv4 from 'uuid'
import { readFileSync } from 'fs'
import color from 'colors'
import micro, { send } from 'micro'
// @ts-ignore
import cors from 'micro-cors'
import { router, post, get } from 'microrouter'
import { compilePlugin } from '../plugin-compiler/compiler'
import { sessions, pluginMarket, roomList, activatePlugin } from './resources'

const handler = router(
  post('/api/v1/plugin/package', async (req, res) => {
    const RawCounter = readFileSync(__dirname + '/../examples/counter.ipl', { encoding: 'utf-8' })
    return await compilePlugin(RawCounter)
  }),
  get('/api/v1/market/plugins', async (req, res) => {
    const metas = Object.values(pluginMarket)
      .map(pluginPackage => pluginPackage.meta)
    send(res, 200, JSON.stringify(metas))
  }),
  get('/api/v1/market/plugins/:id', async (req, res) => {
    const pluginPackage = pluginMarket['counter-0123-abcdef-4567']
    send(res, 200, JSON.stringify(pluginPackage))
  }),
  (req, res) => send(res, 404, 'Not Found')
)

const apiServer = micro(cors()(handler))
apiServer.listen(8080, () => {
  console.log(`simple api server running on ${color.green.bold('localhost:8080')}`)
})

const socketServer = micro(
  (req, res) => send(res, 200)
)
const io: Server = SocketIO(socketServer)
socketServer.listen(1234, () => {
  console.log(`simple socket server running on ${color.green.bold('localhost:1234')}`)
})

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
