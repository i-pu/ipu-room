<template lang='pug'>
  div
    v-layout(row justify-center)
      v-dialog(v-model="dialog" max-width="600px")
        template(v-slot:activator="{ on }")
          v-btn(color="primary" v-on="on") プラグインを作成
        v-card
          v-card-title
            span.headline プラグインを作成
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

                  v-flex(xs12)
                    v-text-field(
                      v-model="pluginInfo.name"
                      :counter="12"
                      :rules="[v => !!v || '必須項目です']",
                      label="プラグイン名"
                      required
                    )

                  v-flex(xs12)
                    v-textarea(
                      v-model="pluginInfo.description"
                      label="説明"
                      :counter="200"
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
              @click="requestCreatePlugin"
            ) 作成
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { PluginConfig } from '@/model'

@Component<PluginCreateForm>({
  sockets: {
    register (data) {
      this.responseCreatePlugin(data)
    },
  },
})
export default class PluginCreateForm extends Vue {
  private dialog: boolean = false
  private valid: boolean = false
  private loader: any = null
  private fileName: string = ''
  private fileUploaded: boolean = false
  private loading: boolean = false
  private agreed: boolean = false
  private pluginInfo: {
    name: string,
    description: string,
    author: string,
    tags: string,
    content: string
  } = {
    name: '',
    description: '',
    author: '',
    tags: '',
    content: ''
  }

  public onFileSelected (event: Event) {
    this.loader = 'loading'
    this.loading = true
    if (event.target instanceof HTMLInputElement) {
      if (!event.target.files) { return }
      const file = event.target.files[0]
      const reader = new FileReader()
      reader.onload = (e: Event) => {
        this.pluginInfo.content = reader.result as string
        this.loader = null
        this.loading = false
        this.fileUploaded = true
        this.fileName = file.name

        if (this.pluginInfo.name === '') {
          this.pluginInfo.name = this.fileName.match(/(.*)(?:\.([^.]+$))/)!![1]
        }
      }
      reader.readAsText(file)
    }
  }

  public requestCreatePlugin () {
    if (this.$store.getters.localOnly) {
      this.responseCreatePlugin({ state: true })
    } else {
      this.pluginInfo.author = this.$store.getters.userName
      console.log(Object.assign({}, this.pluginInfo))
      this.$socket.emit('plugin/register', this.pluginInfo)
    }
  }

  public responseCreatePlugin (payload: { state: boolean }) {
    console.log(payload)
    this.dialog = false
  }
}
</script>
