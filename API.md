## path
#### /room
- methods
  - GET
- returns
  - rooms:[room]

## event
#### visit
##### arg
```json
{
  "user_name": string
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
  "user_id": int
}
```
##### return
```json
{
  "rooms": [room]
}
```
  
#### enter_room
##### arg
```json
{
  "user_id": int,
  "room_id": int
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
  "user_id": int,
  "room_id": int,
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

#### exit_room
##### arg
```json
{
  "user_id": int,
  "room_id": int
}
```
##### error
unimplemented
  
## type
#### room
```json
{
  "room": {
    "room_id": int,
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
    "id": int,
    "name": string,
    "room_id": Option<int>
  }
}
```
#### comment
```json
{
  "comment": {
    "id": int, 
    "user_id": int,
    "room_id": int,
    "content": string,
    "created_at": time // unimplemented
  }
}
```
