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
import { compilePlugin, activatePlugin } from '@plugin-compiler/compiler'
import { sessions, pluginMarket, roomList } from '@mock/resources'
import { PluginMeta, PluginPackage } from '@model'

// @ts-ignore
import fetch from 'node-fetch'

const API_ORIGIN = 'http://localhost:3000/api/v1'

import Counter from '@examples/counter'
import Chat from '@examples/chat'
import Player from '@examples/player'
import Paint from '@examples/paint'
import PlayingCard from '@examples/playingcard'
import Status from '@examples/status'

const __test__ = async () => {
  // try {
  //   // plugin upload test
  //   const { state, uploadedMeta }: { state: boolean, uploadedMeta: PluginMeta } = await fetch(`${API_ORIGIN}/market/plugins`, {
  //     method: 'POST',
  //     body: JSON.stringify(Counter)
  //   })
  //     .then((res: Response) => res.json())

  //   console.log(uploadedMeta)
  //   // plugin fetch meta test
  //   const fetchedPluginMeta: PluginMeta = await fetch(`${API_ORIGIN}/market/plugins/${uploadedMeta.id}`)
  //     .then((res: Response) => res.json())

  //   console.log(`fetched: ${fetchedPluginMeta.name}`)

  //   // plugin load test
  //   const pluginPackage: PluginPackage = await fetch(`${API_ORIGIN}/plugin/load/${uploadedMeta.id}`)
  //     .then((res: Response) => res.json())

  // //   console.log(pluginPackage)
  // } catch (error) {
  //   console.log(error)
  // }

  // make test rooms
  // roomList['xxxx-yyyy-zz'] = {
  //   name: 'トランプ',
  //   id: 'xxxx-yyyy-zz',
  //   // tslint:disable:max-line-length
  //   thumbnailUrl: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
  //   members: [],
  //   pluginPackages: [
  //     await activatePlugin(PlayingCard),
  //     await activatePlugin(Counter),
  //     await activatePlugin(Status),
  //     await activatePlugin(Player),
  //     await activatePlugin(Paint),
  //     await activatePlugin(Chat),
  //   ]
  // }
}

__test__()

const handler = router(
  // ====== Plugin Compiler API Mock ======

  /**
   *  fetch plugin metadata from the plugin market,
   *  and compile plugin.
   * 
   *  @return pluginPackage return 200 Ok and PluginPackage.
   *  @return error return 500 and error object.
   */
  get('/api/v1/plugin/load/:id', async (req, res) => {
    try {
      const pluginId = req.params.id
      // fetch package from market
      console.log(`${color.black.bgWhite('[plugin/load]')} Loading Plugin ${color.yellow(pluginId)}`)
      const meta: PluginMeta = await fetch(`${API_ORIGIN}/market/plugins/${pluginId}`)
        .then((res: any) => res.json())

      const plugin = await compilePlugin(meta)

      return send(res, 200, { plugin, meta })
    } catch (error) {
      console.log(`${color.black.bgRed('[plugin/load]')} Plugin failed to load ...`)
      console.log(error)
      send(res, 500, { error })
    }
  }),

  // ====== Api Mock =======

  /**
   *  upload plugin API as [meta: PluginMeta].
   * 
   *  @return state: boolean
   */
  post('/api/v1/market/plugins', async (req, res) => {
    try {
      const maybePluginMeta: object = await json(req)

      console.log(maybePluginMeta)

      if (!maybePluginMeta) {
        throw 'invalid meta'
      }

      const pluginMeta = maybePluginMeta as PluginMeta

      pluginMeta.id = uuidv4()
      pluginMarket[pluginMeta.id] = pluginMeta

      console.log(`${color.black.bgWhite('[market/plugins]')} Upload ${color.yellow(pluginMeta.name)} as ${color.yellow(pluginMeta.id)}`)

      return send(res, 200, JSON.stringify({ 
        state: true,
        uploadedMeta: pluginMeta
      }))
    } catch (error) {
      return send(res, 500, { error })
    }
  }),

  /**
   *  returns plugin metadata of plugins.
   */
  get('/api/v1/market/plugins', async (req, res) => {
    const metas = Object.values(pluginMarket)
    return send(res, 200, JSON.stringify(metas))
  }),

  /**
   *  returns plugin metadata which plugin id is [id].
   * 
   *  @param id plugin id
   */
  get('/api/v1/market/plugins/:id', async (req, res) => {
    const pluginId = req.params.id
    if (Object.keys(pluginId)) {
      return send(res, 200, JSON.stringify(pluginMarket[pluginId]))
    } else {
      return send(res, 403, { error: `plugin id ${pluginId} was not found.` })
    }
  }),
  (req, res) => send(res, 404, { message: 'Not Found' })
)

export const apiServer = micro(cors()(handler))
apiServer.listen(3000, () => {
  console.log(`simple api server running on ${color.green.bold('localhost:3000')}`)
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

  socket.on('room/create', async ({ roomName, plugins }: { roomName: string, plugins: string[]}) => {
    const roomId = uuidv4()
    console.log(`${color.black.bgWhite('[room/create]')} ${color.green.bold('+')} ${color.yellow(roomName)} (${color.gray(roomId)})`)

    const pluginPackages: PluginPackage[] = []

    // TODO: default plugin

    plugins.forEach(async (id: string, i: number) => {
      try {
        const pluginPackage = await fetch(`${API_ORIGIN}/plugin/load/${id}`)
          .then((res: any) => res.json()) as PluginPackage
        pluginPackages.push(pluginPackage)
        console.log(`${color.black.bgWhite('[plugin/load]')} [${i + 1}/${plugins.length}] Plugin ${color.yellow(id)} successfully loaded!!`)
      } catch (error) {
        console.log(`${color.black.bgRed('[plugin/load]')} [${i + 1}/${plugins.length}] Plugin ${color.yellow(id)} failed to load...`)
        console.log(error) 
      }
    })

    roomList[roomId] = {
      name: roomName,
      id: roomId,
      thumbnailUrl: '',
      members: [],
      pluginPackages
    }
    socket.emit('room/create', { room: roomList[roomId] })
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
