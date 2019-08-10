// =========================
// plugin compiler service
//
// Copyright (c) 2019 i-pu
// =========================

import color from 'colors'
import micro, { send, json } from 'micro'
// @ts-ignore
import cors from 'micro-cors'
import { router, post, options } from 'microrouter'
import { compilePlugin } from '@plugin-compiler/compiler'
import { PluginMeta } from '@model'

const handler = router(
  /**
   *  fetch plugin metadata from the plugin market,
   *  and compile plugin.
   * 
   *  @return pluginPackage return 200 Ok and PluginPackage.
   *  @return error return 500 and error object.
   */
  post('/api/v1/plugin/compile', async (req, res) => {
    try {
      // fetch package from market
      const meta: PluginMeta = await json(req) as PluginMeta

      console.log('meta:')
      console.log(meta)

      const plugin = await compilePlugin(meta)

      return send(res, 200, JSON.stringify({ plugin, meta }))
    } catch (error) {
      console.log(`${color.black.bgRed('[plugin/compile]')} Occur internal error`)
      console.log(error)
      return send(res, 500, error)
    }
  }),
  options('/api/v1/plugin/compile', (_, res) => send(res, 200))
)

if (!process.env.PORT) {
  throw 'Port is not defined.'
}

export const apiServer = micro(handler) // micro(cors()(handler))
apiServer.listen(parseInt(process.env.PORT!!), () => {
  console.log(`compiler service running on port ${color.green.bold(process.env.PORT!!)}`)
})
