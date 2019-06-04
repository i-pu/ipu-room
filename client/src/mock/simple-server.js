const app = require('http').createServer()
const io = require('socket.io')(app)

app.listen(1234, () => {
  console.log('simple server running on localhost:1234')
})

const store = {}

io.on('connection', socket => {
  console.log(`${socket.id} connected`)

  socket.on('room/enter', ({ room_id }) => {
    console.log(`ROOM ${room_id}: join ${socket.id}`)
    socket.join(room_id)
    store[room_id] ? store[room_id].add(room_id) : store[room_id] = new Set()
    socket.emit('room/enter', {})
  })

  socket.on('plugin/trigger', ({ room_id, instance_id, event_name, args}) => {
    console.log(`ROOM ${room_id} instance: ${instance_id} event: ${event_name} args: ${args}`)
    io.in(room_id).emit('plugin/trigger', { event: event_name, args })
  })

  // another_id : workaround
  socket.on('plugin/sync', ({ room_id, instance_id, another_id }) => {
    console.log(`[Plugin] sync from ${another_id}`)
    io.to(another_id).emit('plugin/clone', { room_id, instance_id, my_id: socket.id })
  })

  // my_id : workaround
  socket.on('plugin/clone', ({ record, my_id }) => {
    console.log(`[Plugin] clone to ${my_id}`)
    io.to(my_id).emit('plugin/sync', { record })
  })

  // socket.on('disconnect', socket => {
  // })
})

io.listen(3000)