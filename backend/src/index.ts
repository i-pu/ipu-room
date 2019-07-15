// =========================
// plugin compiler service
//
// Copyright (c) 2019 i-pu
// =========================

import uuidv4 from 'uuid'
import color from 'colors'
import micro, { send, json } from 'micro'
// @ts-ignore
import cors from 'micro-cors'
import { router, post } from 'microrouter'
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
      send(res, 500, JSON.stringify({ error }))
    }
  }),
)

export const apiServer = micro(cors()(handler))
apiServer.listen(3001, () => {
  console.log(`compiler service running on ${color.green.bold(process.env.API_ORIGIN!!)}`)
})
