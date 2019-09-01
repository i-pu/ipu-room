import SocketIO from 'socket.io'

export default SocketIO(process.env.VUE_APP_SOCKET_ORIGIN!!, {
  path: process.env.VUE_APP_SOCKET_PATH,
})
