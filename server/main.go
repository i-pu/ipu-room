package main

import (
	"encoding/json"
	"log"
	"net/http"
	"reflect"

	socketio "github.com/googollee/go-socket.io"
)

type CustomServer struct {
	Server *socketio.Server
}

func (s *CustomServer) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Access-Control-Allow-Credentials", "true")
	origin := r.Header.Get("Origin")
	w.Header().Set("Access-Control-Allow-Origin", origin)
	s.Server.ServeHTTP(w, r)
}
func configureSocketIO() *socketio.Server {
	server, err := socketio.NewServer(nil)
	if err != nil {
		log.Fatal(err)
	}
	server.OnConnect("/", func(s socketio.Conn) error {
		s.SetContext("")
		log.Println("connected:", s.ID())
		return nil
	})
	server.OnEvent("/", "notice", func(s socketio.Conn, msg interface{}) {
		log.Println(reflect.TypeOf(msg))
		bytes, err := json.Marshal(msg)
		if err != nil {
			log.Println(err)
		}
		log.Println("notice msg:", string(bytes))
		s.Emit("reply", "recieve: "+string(bytes))
	})
	server.OnEvent("/", "bye", func(s socketio.Conn) string {
		last := s.Context().(string)
		log.Println("call bye by", s.ID())
		s.Emit("bye", last)
		s.Close()
		return last
	})
	server.OnError("/", func(e error) {
		log.Println("meet error:", e)
	})
	server.OnDisconnect("/", func(s socketio.Conn, msg string) {
		log.Println("closed", msg)
	})
	return server
}

func main() {
	ioServer := configureSocketIO()
	ws := new(CustomServer)
	ws.Server = ioServer
	go ws.Server.Serve()
	defer ws.Server.Close()

	http.Handle("/socket.io/", ws)
	log.Println("Serving at localhost:8000...")
	log.Fatal(http.ListenAndServe(":8000", nil))
}
