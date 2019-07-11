// @ts-ignore
import fetch from 'node-fetch'
import Counter from '@/examples/counter'
import { PluginMeta, PluginPackage } from '@model'

const API_ORIGIN = 'http://localhost:3000/api/v1'

let pluginId: string = ''

describe('POST /market/plugins', () => {
  it('plugin upload test', async () => {
    // why {} ???
    console.log(Counter)

    const payload = await fetch(`${API_ORIGIN}/market/plugins`, {
      method: 'POST',
      body: JSON.stringify(Counter)
    })
      .then((res: Response) => res.json())

    expect(payload.uploadedMeta)
      .toHaveProperty('id')
    
    pluginId = payload.uploadedMeta.id
  })
})

describe('GET /market/plugins/:id', () => {
  it('plugin fetch meta test', async () => {
    const meta: PluginMeta = await fetch(`${API_ORIGIN}/market/plugins/${pluginId}`)
      .then((res: Response) => res.json())

    expect(meta)
      .toMatchObject({
        id: expect.any(String)
      })
  })
})

describe('GET /plugin/load/:id', () => {
  it('plugin load test', async () => {
    const pluginPackage: PluginPackage = await fetch(`${API_ORIGIN}/plugin/load/${pluginId}`)
      .then((res: Response) => res.json())

  expect(pluginPackage)
    .toMatchObject({
      plugin: {
        functions: expect.any(String)
      }
    })
  })
})
