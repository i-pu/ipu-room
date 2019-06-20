// =========================
// simple-server.ts
//
// Copyright (c) 2019 i-pu
// =========================

import SocketIO, { Server } from 'socket.io'
import uuidv4 from 'uuid'
import color from 'colors'
import micro, { send, json } from 'micro'
// @ts-ignore
import cors from 'micro-cors'
import { router, post, get } from 'microrouter'
import { compilePlugin } from '../plugin-compiler/compiler'
import { sessions, pluginMarket, roomList } from './resources'
import { PluginMeta, PluginPackage } from '@client/model'
import Counter from '../examples/counter'
// @ts-ignore
import fetch from 'node-fetch'

const __test__ = async () => {
  // plugin upload test
  await fetch(`http://localhost:8080/api/v1/market/plugins/counter`)
    .then((res: any) => res.json())
    .then((json: any) => console.log)

  // plugin load test
  await fetch(`http://localhost:8080/api/v1/plugin/load/counter`)
    .then((res: any) => res.json())
    .then(console.log)
    .catch(console.log)
}

// __test__()

const handler = router(
  // ====== Plugin Compiler API Mock ======
  get('/api/v1/plugin/load/:id', async (req, res) => {
    try {
      const pluginId = 'counter'
      // fetch package from market
      const meta: PluginMeta = await fetch(`http://localhost:8080/api/v1/market/plugins/${pluginId}`)
        .then((res: any) => res.json())

      const plugin = await compilePlugin(meta.content)

      send(res, 200, { plugin, meta })
    } catch (error) {
      send(res, 500, error)
    }
  }),

  // ====== Api Mock =======
  post('/api/v1/market/plugins', async (req, res) => {
    // const pluginMeta: PluginMeta = await json(req) as PluginMeta
    const pluginMeta = Counter as PluginMeta
    pluginMeta.id = 'counter' // uuidv4()
    pluginMarket[pluginMeta.id] = pluginMeta
    return send(res, 200, JSON.stringify({ state: true }))
  }),
  get('/api/v1/market/plugins', async (req, res) => {
    const metas = Object.values(pluginMarket)
    send(res, 200, JSON.stringify(metas))
  }),
  get('/api/v1/market/plugins/:id', async (req, res) => {
    const meta = pluginMarket['counter']
    send(res, 200, JSON.stringify(meta))
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

  socket.on('lobby', ({ userId }: { userId: string }) => {
    console.log(`${color.black.bgWhite('[lobby]')} Lobby ${color.yellow(Object.keys(roomList).length.toString())} rooms`)
    socket.emit('lobby', { rooms: Object.values(roomList) })
  })

  socket.on('room/make', async ({ roomName, pluginIds }: { roomName: string, pluginIds: string[]}) => {
    const roomId = uuidv4()
    console.log(`${color.black.bgWhite('[room/make]')} ${color.green.bold('+')} ${color.yellow(roomName)} (${color.gray(roomId)})`)

    const pluginPackages: PluginPackage[] = []
    pluginIds.forEach(async (id: string, i: number) => {
      try {
        const pluginPackage = await fetch(`http://localhost:8080/api/v1/plugin/load/${id}`)
          .then((res: any) => res.json()) as PluginPackage
        pluginPackages.push(pluginPackage)
        console.log(`${color.black.bgWhite('[plugin/load]')} [${i + 1}/${pluginIds.length}] Plugin ${color.yellow(id)} successfully loaded!!`)
      } catch (error) {
        console.log(`${color.black.bgRed('[plugin/load]')} [${i + 1}/${pluginIds.length}] Plugin ${color.yellow(id)} failed to load...`)
        console.log(error) 
      }
    })

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

    if (!room) {
      console.log(`${color.black.bgRed('[room/enter]')} Error room does not exist of ROOM ${roomId}`)
      return
    }

    if (!sessions[socket.id]) {
      console.log(`${color.black.bgRed('[room/enter]')} Error invalid id ${socket.id}`)
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
    // delete sessions[socket.id]
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
