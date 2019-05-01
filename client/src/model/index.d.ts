export type Comment = {
  type: string,
  avatar: string,
  comment_id: string,
  user_name: string,
  user_id: string,
  text: string,
  commented_at: Date
}

export type Room = {
  room_name: string,
  room_id: string,
  thumbnail_url: string,
  members: User[],
  plugins: string[]
}

export type User = {
  name: string, avatar_url: string
}