// @ts-ignore
import fetch from 'node-fetch'
import Counter from '@/examples/counter'
import { PluginMeta } from '@model'

let pluginId: string = ''

describe('POST /market/plugins', () => {
  it('plugin upload test', async () => {
    const payload = await fetch('http://localhost:3000/api/v1/market/plugins', {
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
    const meta: PluginMeta = await fetch(`http://localhost:3000/api/v1/market/plugins/${pluginId}`)
      .then((res: Response) => res.json())

    expect(meta).toMatchObject({
      id: expect.any(String)
    })
  })
})