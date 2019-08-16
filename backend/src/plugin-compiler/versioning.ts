import color from 'colors'
import { PluginMeta } from '@model'

/**
 * semantic versioning
 * @param newPluginMeta 
 * @param oldPluginMeta
 */
export const semanticVersioning = (newPluginMeta: PluginMeta, oldPluginMeta: PluginMeta): string => {
  const [major, minor, patch] = oldPluginMeta.version.split('.')
  const newVersion = [major, minor, (parseInt(patch) + 1).toString()].join('.')
  console.log(`${color.black.bgWhite('[market/plugins]')} ${oldPluginMeta.author}/${oldPluginMeta.name} ${color.yellow(oldPluginMeta.version)} -> ${color.yellow(newVersion)}`)
  return newVersion
}