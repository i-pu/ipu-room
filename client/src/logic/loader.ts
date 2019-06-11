import { Room, PluginProperties, PluginInstance, PluginPackage } from '@/model'
import { compile } from '@/logic/compiler'

export const boot = async ({ plugin, meta }: PluginPackage, options: { room: Room }): Promise<PluginInstance> => {
  try {
    const fnlike = plugin.functions.initialize

    if (!fnlike) {
      throw new Error()
    }

    const initializer = typeof(fnlike) === 'string' ? eval(`(function ${fnlike})`) : new Function(...<string[]>fnlike) as (...args: any) => Record<string, any>
    console.log(initializer())
    const properties: PluginProperties = {
      record: initializer(),
      env: { instanceId: plugin.instanceId, ...options },
      meta: meta,
    }
    return { component: await compile(plugin, properties), properties }
  } catch (e) {
    throw 'Plugin initializer not found'
  }
}