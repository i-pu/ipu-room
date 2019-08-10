import { Room, PluginProperties, PluginInstance, PluginPackage, PluginFunctions } from '@/model'
import { compile } from '@/logic/compiler'

/**
*  Initialize a plugin with record and compiles Vue Component
*/
export const boot = async ({ plugin, meta }: PluginPackage, options: { room: Room }): Promise<PluginInstance> => {
  if (plugin.instanceId === '') {
    throw new Error('Plugin instance id must be required')
  }

  console.log(plugin.functions)

  try {
    plugin.functions = typeof plugin.functions === 'string'
      ? eval(plugin.functions) as PluginFunctions
      : plugin.functions

    const initializer: () => Record<string, any> = plugin.functions.initialize

    if (!initializer) {
      throw '[Plugin Loader] Plugin initializer not found'
    }
    const properties: PluginProperties = {
      record: initializer(),
      env: { instanceId: plugin.instanceId, ...options },
      meta,
    }
    return { component: await compile(plugin, properties), properties }
  } catch (error) {
    throw error
  }
}
