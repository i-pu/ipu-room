import { Component } from 'vue'
import { compile } from '@/logic/compiler'
import { Socket } from 'socket.io'

/**
* PluginComponent
*/
// type ThenArg<T> = T extends Promise<infer U> ? U : T
// export type PluginComponent = ThenArg<ReturnType<typeof compile>> & {
//   record: Record<string, any>,
//   $send: (event: string, options?: { to: string, broadcast: boolean }, ...args: any[]) => void,
//   $socket: Socket,
//   $me: User,
//   $members: User[],
//   env: PluginProperties['env'],
// }

/**
* Expresses Data that will be send from the server.
* @param template HTML template
* @param functions functions
* @param instanceId instanceId
* @param config config
*/

// compiler internal expression
export interface PluginFunctions {
  initialize: ((...args: any) => Record<string, any>)
  [event: string]: (...args: any) => void
}

export interface Plugin {
  template: string,
  functions: string | PluginFunctions,
  instanceId: string,
  config: {
    enabled: boolean,
  }
}

/**
* Expresses Data of static infomation about a plugin.
* @param id HTML template
* @param thumbnailUrls
* @param content raw script of a plugin
*/
interface PluginMeta {
  id: string,
  version: string,
  thumbnailUrls: string[],
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string
}

/*

*/
export interface PluginEnv {
  instanceId: string,
  room: Room
}

/**
* PluginProperties
*/
export interface PluginProperties {
  record: Record<string, any>,
  env: PluginEnv,
  meta: PluginMeta
}

export interface PluginInstance {
  component: Component,
  properties: PluginProperties,
}

export interface PluginPackage {
  plugin: Plugin,
  meta: PluginMeta,
}

/**
* Room
*/
export interface Room {
  name: string,
  id: string,
  thumbnailUrl: string,
  members: User[],
  pluginPackages: PluginPackage[]
}

/**
* User
*/
export interface User {
  name: string,
  id: string,
  avatarUrl: string
}

