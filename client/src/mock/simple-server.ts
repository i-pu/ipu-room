// A Simple socket server for testing

// @ts-ignore
const Counter = require('./../plugin_examples/counter')
const Chat = require('./../plugin_examples/chat')
const Player = require('./../plugin_examples/player')
const Paint = require('./../plugin_examples/paint')
const app = require('http').createServer()
import * as SocketIO from 'socket.io'
const uuidv4 = require('uuid')
const io: SocketIO.Server = require('socket.io')(app)
const color = require('colors')

import { Room } from '@/model'

app.listen(1234, () => {
  console.log(`simple server running on ${color.green.bold('localhost:1234')}`)
})

const activatePlugin = (pluginData: any) => {
  const pluginPackage = JSON.parse(JSON.stringify(pluginData))
  pluginPackage.plugin.instanceId = uuidv4()
  return pluginPackage
}

// room_id -> room
const roomList: Record<string, Room> = {
  'xxxx-yyyy-zzzz': {
    name: '雑談部屋1',
    id: 'xxxx-yyyy-zzzz',
    // tslint:disable:max-line-length
    thumbnail_url: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
    members: [],
    pluginPackages: [
      activatePlugin(Counter), 
      activatePlugin(Counter),
      activatePlugin(Chat),
      activatePlugin(Player),
      activatePlugin(Paint)
    ],
    plugins: []
  }
}
// socket_id -> room_id
const sessions: Record<string, string> = {}

io.on('connection', socket => {
  socket.on('room/enter', ({ room_id }) => {
    console.log(`${color.black.bgWhite('room/enter')} ROOM ${color.gray(room_id)} ${color.green.bold('+')} ${socket.id}`)
    socket.join(room_id)
    sessions[socket.id] = room_id

    if (roomList[room_id] && !roomList[room_id].members.map(m => m.id).includes(socket.id)) {
      roomList[room_id].members.push({
        id: socket.id, name: '名無し', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460'
      })
    }

    const room = roomList[room_id]

    console.log(`${color.black.bgWhite('room/enter')} Total ${color.yellow(room.pluginPackages.length)} Plugins applied!!`)
    for (const { plugin, meta } of room.pluginPackages) {
      console.log(`${color.black.bgWhite('room/enter')}   - ${color.gray(meta.author + '/' + meta.name)} (${plugin.instanceId})`)
    }

    socket.emit('room/enter', { room })
    io.in(room_id).emit('room/update', { room })
  })

  socket.on('plugin/trigger', ({ room_id, instance_id, event_name, args}) => {
    console.log(`${color.black.bgWhite('[plugin/trigger]')} ROOM ${color.gray(room_id)} ${color.yellow(instance_id)} ${color.blue(event_name)}`)
    io.in(room_id).emit(`plugin/${instance_id}/trigger`, { event: event_name, args })
  })

  socket.on('plugin/sync', ({ room_id, instance_id }) => {
    const random_id = roomList[room_id].members.map(m => m.id).filter(id => id !== socket.id)[0]
    console.log(`${color.black.bgWhite('[plugin/sync]')} sync request ${color.gray(socket.id)} -> ${color.gray(random_id)}`)
    io.to(random_id).emit(`plugin/${instance_id}/clone`, { room_id, instance_id, from: socket.id })
  })

  socket.on('plugin/clone', ({ room_id, instance_id, record, from }) => {
    console.log(`${color.black.bgWhite('[plugin/clone]')} clone to ${color.gray(socket.id)} -> ${color.gray(from)}`)
    io.to(from).emit(`plugin/${instance_id}/sync`, { record })
  })

  socket.on('room/exit', ({ room_id }) => {
    leaveRoom(room_id)
    socket.emit('room/exit')
  })

  socket.on('disconnect', () => {
    if (sessions[socket.id])
      leaveRoom(sessions[socket.id])
  })

  const leaveRoom = (roomId: string) => {
    console.log(`${color.black.bgWhite('[room/exit]')} ${color.gray(roomId)} ${color.red.bold('-')} ${color.gray(socket.id)}`)
    roomList[roomId].members = roomList[roomId].members.filter(m => m.id !== socket.id)
    delete sessions[socket.id]
    io.in(roomId).emit('room/update', { room: roomList[roomId] })
  }
})

io.listen(3000)
