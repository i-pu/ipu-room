import { Component } from 'vue'
import { compile } from '@/logic/compiler'
import { Socket } from 'socket.io'

/**
* PluginComponent
*/
type ThenArg<T> = T extends Promise<infer U> ? U : T
export type PluginComponent = ThenArg<ReturnType<typeof compile>> & {
  record: Record<string, any>,
  $send: (event: string, ...args: any[]) => void,
  $socket: Socket,
  env: PluginProperties['env']
}

/**
* Expresses Data that will be send from the server.
* @param template HTML template
* @param functions functions
* @param instanceId instanceId
* @param config config
*/
export interface Plugin {
  template: string,
  functions: { 
    initialize: string[] | string | ((...args: any) => Record<string, any>) } &
    (Record<string, string[] | string | ((this: PluginComponent, ...args: any) => void)>),
  instanceId: string,
  config: {
    enabled: boolean
  }
}

/**
* Expresses Data of static infomation about a plugin.
* @param id HTML template
* @param thumbnail_url
* @param content raw script of a plugin
*/
interface PluginMeta {
  id: string,
  thumbnail_url: string,
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string
}

/**
* PluginProperties
*/
export interface PluginProperties {
  record: Record<string, any>,
  env: {
    instanceId: string,
    room: Room,
  },
  meta: PluginMeta
}

export type PluginInstance = {
  component: Component,
  properties: PluginProperties,
}

export type PluginPackage = {
  plugin: Plugin,
  meta: PluginMeta,
}

/**
* Room
*/
export interface Room {
  name: string,
  id: string,
  thumbnail_url: string,
  members: User[],
  pluginPackages: Array<PluginPackage>,
  plugins: Array<PluginInstance>,
}

/**
* User
*/
export interface User {
  name: string,
  id: string,
  avatar_url: string
}

