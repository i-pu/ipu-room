// A Simple socket server for testing
const colors = require('colors')
const app = require('http').createServer()
const io = require('socket.io')(app)

app.listen(1234, () => {
  console.log(`simple server running on ${'localhost:1234'.green.bold}`)
})

const plugin = {
  template: `<div><h3> {{ record.count }} </h3><v-btn @click="plus"> Add </v-btn></div>`,
  functions: {
    initialize: ['return { count: 0 }'],
    plus: ['this.record.count++'],
  },
  instanceId: 'counter_xxx'
}
const meta = {
  id: 'counter_xxx',
  // plugin name
  name: 'counter',
  thumbnail_url: 'https://avatars3.githubusercontent.com/u/50242068?s=200&v=4',
  description: 'aaa',
  author: 'a',
  tags: 'a,b,c',
  content: '<html></html>',
}

// room_id -> room
const roomList = {
  'xxxx-yyyy-zzzz': {
    name: '雑談部屋1',
    id: 'xxxx-yyyy-zzzz',
    // tslint:disable:max-line-length
    thumbnail_url: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
    members: [],
    pluginPackages: [{ plugin, meta }]
  }
}
// socket_id -> room_id
const sessions = {}

io.on('connection', socket => {
  // console.log(`${'+'.green.bold} ${socket.id}`)

  socket.on('room/enter', ({ room_id }) => {
    console.log(`${'room/enter'.black.bgWhite} ROOM ${room_id.gray} ${'+'.green.bold} ${socket.id}`)
    socket.join(room_id)
    sessions[socket.id] = room_id

    if (roomList[room_id] && !roomList[room_id].members.map(m => m.id).includes(socket.id)) {
      roomList[room_id].members.push({
        id: socket.id, name: '名無し', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460'
      })
    }
    socket.emit('room/enter', { room: roomList[room_id] })
    io.in(room_id).emit('room/update', { room: roomList[room_id] })
  })

  socket.on('plugin/trigger', ({ room_id, instance_id, event_name, args}) => {
    console.log(`${'[plugin/trigger]'.black.bgWhite} ROOM ${room_id.gray} ${instance_id.yellow} ${event_name.blue}`)
    io.in(room_id).emit(`plugin/${instance_id}/trigger`, { event: event_name, args })
  })

  socket.on('plugin/sync', ({ room_id, instance_id }) => {
    const random_id = roomList[room_id].members.map(m => m.id).filter(id => id !== socket.id)[0]
    console.log(`${'[plugin/sync]'.black.bgWhite} sync request ${socket.id.gray} -> ${random_id.gray}`)
    io.to(random_id).emit(`plugin/${instance_id}/clone`, { room_id, instance_id, from: socket.id })
  })

  socket.on('plugin/clone', ({ room_id, instance_id, record, from }) => {
    console.log(`${'[plugin/clone]'.black.bgWhite} clone to ${socket.id.gray} -> ${from.gray}`)
    io.to(from).emit(`plugin/${instance_id}/sync`, { record })
  })

  socket.on('room/exit', ({ room_id }) => {
    leaveRoom(room_id)
    socket.emit('room/exit')
  })

  socket.on('disconnect', () => {
    // console.log(`${'-'.red.bold} ${socket.id}`)
    if (sessions[socket.id])
      leaveRoom(sessions[socket.id])
  })

  const leaveRoom = roomId => {
    console.log(`${'[room/exit]'.black.bgWhite} ${roomId.gray} ${'-'.red.bold} ${socket.id.gray}`)
    roomList[roomId].members = roomList[roomId].members.filter(m => m.id !== socket.id)
    delete sessions[socket.id]
    io.in(roomId).emit('room/update', { room: roomList[roomId] })
  }
})

io.listen(3000)