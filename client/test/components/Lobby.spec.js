import { mount } from '@vue/test-utils'
import Lobby from './../../src/components/Lobby'

describe('Component', () => {
  test('is a Vue instance', () => {
    const wrapper = mount(Lobby)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})
