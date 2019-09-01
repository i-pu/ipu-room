<template lang="pug">
  div
    v-layout(row justify-center)
      v-dialog(v-model="dialog" max-width="600px")
        template(v-slot:activator="{ on }")
          v-btn(color="green white--text" v-on="on") プラグインを{{ update ? '更新' : '作成' }}
        v-card
          v-card-title
            span.headline プラグインを{{ update ? '更新' : '作成' }}
          v-card-text
            v-form(
              v-model="valid"
            )
              v-container(grid-list-md)
                v-layout(wrap)
                  v-flex(xs12)
                    v-btn(
                      :loading="loading"
                      :disabled="loading || fileUploaded"
                      color="blue-grey"
                      class="white--text"
                      @click="$refs.uploader.click()"
                    ) {{ fileUploaded ? fileName : 'プラグインをアップロード' }}
                      input(
                        type="file"
                        accept=".ipl"
                        ref="uploader"
                        @change="onFileSelected"
                        hidden
                      )
                      v-icon(right dark) cloud_upload

                  v-flex(xs12 v-if="!update")
                    v-text-field(
                      v-model="gistUrl"
                      :counter="12"
                      label="gistから"
                    )

                  v-flex(xs12 v-if="!update")
                    v-text-field(
                      v-model="meta.name"
                      :counter="12"
                      :rules="[v => !!v || '必須項目です']",
                      label="プラグイン名"
                      required
                    )

                  v-flex(xs12)
                    v-textarea(
                      v-model="meta.description"
                      label="説明"
                      :counter="200"
                    )

                  v-flex(xs12)
                    v-text-field(
                      v-model="meta.tags"
                      label="タグ名(カンマ区切り)"
                      :counter="100"
                    )

                  v-flex(xs12)
                    v-checkbox(
                      v-model="agreed"
                      label="同意します"
                      required
                    )
          v-card-actions
            v-spacer
            v-btn(
              :disabled="!valid"
              color="success"
              @click="requestUploadPlugin"
            ) {{ update ? '更新' : '作成' }}
</template>

<script lang="ts">
import { createComponent, ref, SetupContext, onMounted } from '@vue/composition-api'
import { PluginMeta } from '@/model'
import store from '@/store'

export default createComponent({
  props: {
    update: {
      type: Boolean,
      default: () => false,
    },
    pluginMeta: Object as () => PluginMeta,
  },
  setup (props: { update: boolean, pluginMeta: PluginMeta }, { root }: SetupContext) {
    const gistUrl = ref<string>('')
    const dialog = ref<boolean>(false)
    const valid = ref<boolean>(false)
    const loader = ref<any>(null)
    const fileName = ref<string>('')
    const fileUploaded = ref<boolean>(false)
    const loading = ref<boolean>(false)
    const agreed = ref<boolean>(false)
    const meta = ref<Partial<PluginMeta>>({
      name: '',
      description: '',
      author: '',
      tags: '',
      content: '',
      thumbnailUrls: [],
    })

    const onFileSelected = (event: Event) => {
      loader.value = 'loading'
      loading.value = true
      if (event.target instanceof HTMLInputElement) {
        if (!event.target.files) { return }
        const file = event.target.files[0]
        const reader = new FileReader()
        reader.onload = (e: Event) => {
          meta.value.content = reader.result as string
          loader.value = null
          loading.value = false
          fileUploaded.value = true
          fileName.value = file.name

          if (meta.value.name === '') {
            meta.value.name = fileName.value.match(/(.*)(?:\.([^.]+$))/)!![1]
          }
        }
        reader.readAsText(file)
      }
    }

    const requestUploadPlugin = async () => {
      meta.value.author = store.getters.userName
      console.log(Object.assign({}, this.meta))
      if (props.update) {
        const response: { state: boolean } = await fetch(
          `${process.env.VUE_APP_API_ORIGIN}/market/plugins/${props.pluginMeta.id}`
        , {
          method: 'POST',
          body: JSON.stringify(meta.value),
        })
          .then((res) => res.json())
        responseCreatePlugin(response)
      } else {
        // from gist
        if (this.gistUrl) {
          this.meta.content = await fetch(this.gistUrl).then((res) => res.text())
          console.log(this.meta.content)
        }

        const response: { state: boolean } = await fetch(`${process.env.VUE_APP_API_ORIGIN}/market/plugins`, {
          method: 'POST',
          body: JSON.stringify(this.meta),
        })
          .then((res) => res.json())

        responseCreatePlugin(response)
      }
    }

    const responseCreatePlugin = (payload: { state: boolean }) => {
      console.log(payload)
      dialog.value = false
      root.$emit('reload')
    }

    onMounted(() => {
      if (props.update) {
        meta.value = Object.assign({}, props.pluginMeta)
      }
    })

    return {
      gistUrl,
      dialog,
      valid,
      loader,
      fileName,
      fileUploaded,
      loading,
      agreed,
      meta,
      onFileSelected,
      requestUploadPlugin,
      responseCreatePlugin,
    }
  },
})
</script>
