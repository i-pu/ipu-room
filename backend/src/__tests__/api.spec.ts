// @ts-ignore
import fetch from 'node-fetch'
import { PluginPackage, PluginMeta } from '@model'

import Counter from '@examples/counter'

const API_ORIGIN = 'http://localhost:3000/api/v1'

describe('GET /plugin/load/:id', () => {
  it('plugin load test', async () => {
    const pluginPackage: PluginPackage = await fetch(`${API_ORIGIN}/plugin/compile`, {
      method: 'POST',
      body: JSON.stringify(Counter as PluginMeta)
    })
      .then((res: Response) => res.json())

  expect(pluginPackage)
    .toMatchObject({
      plugin: {
        functions: expect.any(String)
      }
    })
  })
})
