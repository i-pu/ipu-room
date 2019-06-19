import { Room, PluginProperties, PluginInstance, PluginPackage, PluginFunctions } from '@/model'
import { compile } from '@/logic/compiler'

/**
*  Initialize plugin with record and compile Vue Component
*/
export const boot = async ({ plugin, meta }: PluginPackage, options: { room: Room }): Promise<PluginInstance> => {
  if (plugin.instanceId === '') {
    throw 'Plugin instance id must be required'
  }

  try {
    // plugin.functin: string -> Function[]
    plugin.functions = typeof plugin.functions === 'string'
      ? eval(plugin.functions) as PluginFunctions
      : plugin.functions

    const initializeFn = plugin.functions.initialize

    if (!initializeFn) {
      throw 'Plugin initializer not found'
    }

    console.log(initializeFn())
    const properties: PluginProperties = {
      record: initializeFn(),
      env: { instanceId: plugin.instanceId, ...options },
      meta,
    }
    return { component: await compile(plugin, properties), properties }
  } catch (e) {
    throw e
  }
}
