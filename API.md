## event
#### enter_room
- args
  - user_name
  - room_name
- returns
  - users:[user]
  - comments:[comment]
  - room_name
  - room_id
- errors
  - unimplemented
  
#### chat 
- args
  - user_id
  - room_id
  - content
  - created_at
- returns
  - comment
- errors
  - unimplemented

#### exit_room
- args
  - user_id
  - room_id
- errors
  - unimplemented
  
## type
#### user 
- user_id
- room_id 
- user_name

#### comment
- comment_id
- comment_user_id
- comment_room_id
- content
- created_at