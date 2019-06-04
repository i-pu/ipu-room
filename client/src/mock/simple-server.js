const app = require('http').createServer()
const io = require('socket.io')(app)

app.listen(1234, () => {
  console.log('simple server running on localhost:1234')
})

io.on('connection', socket => {
  console.log(`${socket.id} connected`)

  socket.on('room/enter', ({ room_id }) => {
    console.log(`ROOM ${room_id}: join ${socket.id}`)
    socket.join(room_id)
    socket.emit('room/enter', {})
  })

  socket.on('plugin/trigger', ({ room_id, instance_id, event_name, args}) => {
    console.log(`ROOM ${room_id} instance: ${instance_id} event: ${event_name} args: ${args}`)
    io.in(room_id).emit('plugin/trigger', { event: event_name, args })
  })
})

io.listen(3000)