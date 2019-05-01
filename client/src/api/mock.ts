import { Room, User, Comment } from '@/model'

export const ROOMS_MOCK: Room[] = [
  {
    room_name: '雑談部屋1',
    room_id: 'xxxx-yyyy-zzzz',
    thumbnail_url: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
    members: [
      { id: '123', name: 'Tom', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
      { id: '456', name: 'John', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
      { id: '789', name: 'Alice', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
    ],
    plugins: ['counter'],
  },
]

// : User
export const USER_MOCK: User = { id: '123', name: 'Tom', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' }

// : User[]
export const ROOM_MEMBER_MOCK: User[] = [
  { id: '123', name: 'Tom', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
  { id: '456', name: 'John', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
  { id: '789', name: 'Alice', avatar_url: 'https://avatars0.githubusercontent.com/u/9064066?v=4&s=460' },
]

// : Comment[]
export const COMMENTS_MOCK = []
