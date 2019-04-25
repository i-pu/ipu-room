## path
#### /room [GET]
##### return 
```json
{
  "rooms": [room]
}
```

#### /plugin [GET]
##### return
```json
{
  "plugins": [plugin]
}
```

# Socket.IO
## event

#### plugin/register
##### arg
```json
{
  "plugin_name": str,
  "python_file": str
}
```

#### plugin/activate
##### arg
```json
{
  "plugin_name": str,
  "room_id": str
}
```

#### visit
##### arg
```json
{
  "user_name": str
}
```

##### return
```json
user
```
  
#### lobby
##### arg
```json
{
  "user_id": str 
}
```
##### return
```json
{
  "rooms": [room],
}
```
  
#### room/create
##### arg
```json
{
  "room_name": str,
  "plugins": [plugin_id] 
}
```
##### return
```json
room
```
##### errors
unimplemented
  
#### chat 
##### arg
```json
{
  "user_id": str,
  "room_id": str,
  "content": string,
  "created_at": time, // unimplemented
}
```
##### return
```json
comment
```

##### error
unimplemented

#### room/enter
##### arg
```json
{
  "user_id": str,
  "room_id": str 
}
```
##### error
unimplemented
  
## type
#### room
```json
{
  "room": {
    "room_id": str,
    "room_name": string,
    "users": [user],
    "comments": [comment]
  }
}
```
#### user 
```json
{
  "user": {
    "id": str,
    "name": string,
    "room_id": Option<str>
  }
}
```
#### comment
```json
{
  "comment": {
    "id": str, 
    "user_id": str,
    "room_id": str,
    "content": string,
    "created_at": time // unimplemented
  }
}
```

```json
{
  "plugin": {
    "id": str,
    "name": str,
  }
}
```
