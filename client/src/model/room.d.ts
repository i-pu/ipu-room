import { User } from '@/model/user'

export type Room = {
  room_name: string,
  room_id: string,
  thumbnail_url: string,
  members: User[],
  plugins: string[]
}