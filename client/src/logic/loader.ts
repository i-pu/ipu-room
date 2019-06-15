import { Room, PluginProperties, PluginInstance, PluginPackage } from '@/model'
import { compile } from '@/logic/compiler'

export const boot = async ({ plugin, meta }: PluginPackage, options: { room: Room }): Promise<PluginInstance> => {
  try {
    const fnlike = plugin.functions.initialize

    if (!fnlike) {
      throw new Error()
    }

    const initializer = typeof(fnlike) === 'string' ?
      eval(`(function ${fnlike})`) :
      new Function(...fnlike as string[]) as (...args: any) => Record<string, any>
    console.log(initializer())
    const properties: PluginProperties = {
      record: initializer(),
      env: { instanceId: plugin.instanceId, ...options },
      meta,
    }
    return { component: await compile(plugin, properties), properties }
  } catch (e) {
    throw new Error('Plugin initializer not found')
  }
}
