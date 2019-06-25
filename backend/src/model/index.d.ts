// =========================
// index.d.ts
//
// Copyright (c) 2019 i-pu
// =========================

export interface Plugin {
  template: string,
  functions: string,
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
  thumbnailUrls: string[],
  name: string,
  description: string,
  author: string,
  tags: string,
  content: string
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

