<template lang="pug">
  v-layout(row wrap v-if="loaded")
    // template editor
    v-flex(d-flex xs12 sm12 md6)
      v-card(white flat)
        v-card-title.grey--text Template
        .editor.px-4(@input="syncTemplate" v-text="editableTempate" contenteditable="true")
    // functions editor
    v-flex(d-flex xs12 sm12 md6)
      v-card(white flat)
        v-card-title.grey--text Functions
        .editor.px-4(@input="syncFunctions" v-text="editableFunctions" contenteditable="true")
</template>

<script lang="ts">
import { createComponent, SetupContext, ref, reactive, onMounted, watch } from '@vue/composition-api'
import _ from 'lodash'
import { PluginPackage, Room, PluginInstance, Plugin } from '@/model'

export default createComponent({
  props: {
    pluginPackage: Object as () => PluginPackage,
  },
  setup (props: { pluginPackage: PluginPackage }, { root }: SetupContext) {
    const loaded = ref<boolean>()
    // ???
    let innerPluginPackage: any = null
    const editableFunctions = ref<string>()
    const editableTemplate = ref<string>()

    watch(() => innerPluginPackage!!.plugin.functions, async (v: PluginPackage) => {
      console.log('watch')
      await root.$emit('refresh', v)
    })

    watch(() => innerPluginPackage!!.plugin.template, async (v: PluginPackage) => {
      console.log('watch')
      await root.$emit('refresh', v)
    })

    const syncFunctions = () => _.debounce(async (e: Event) => {
      try {
        const functions = JSON.parse((e.target as HTMLInputElement).innerHTML)
        this.innerPluginPackage.plugin.functions = functions
      } catch (e) {
        root.$emit('toast', 'Syntax error')
      }
    }, 1000)

    const syncTemplate = () => _.debounce(async (e: Event) => {
      if (!innerPluginPackage) { return }
      innerPluginPackage.plugin.template = (e.target as HTMLInputElement).innerText
    }, 1000)

    onMounted(() => {
      // @ts-ignore
      Function.prototype.toJSON = Function.prototype.toString
      innerPluginPackage = reactive(_.clone(props.pluginPackage))
      editableFunctions.value = JSON.stringify(props.pluginPackage.plugin.functions, null, '\t')
      editableTemplate.value = _.clone(props.pluginPackage.plugin.template)
      loaded.value = true
    })

    return {
      loaded, innerPluginPackage, editableFunctions, editableTemplate,
      syncFunctions, syncTemplate,
    }
  },
})
</script>

<style lang="stylus" scoped>
.editor
  height 300px
  text-align left
</style>