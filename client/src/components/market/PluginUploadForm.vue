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
import Vue from 'vue'
import { Component, Prop } from 'vue-property-decorator'
import { PluginMeta } from '../../model'

@Component<PluginUploadForm>({
  sockets: {
    // 'plugin/register' (data) {
    //   this.responseCreatePlugin(data)
    // },
  },
})
export default class PluginUploadForm extends Vue {
  @Prop({ default: false }) private update!: boolean
  @Prop() private pluginMeta!: PluginMeta
  private gistUrl: string = ''
  private dialog: boolean = false
  private valid: boolean = false
  private loader: any = null
  private fileName: string = ''
  private fileUploaded: boolean = false
  private loading: boolean = false
  private agreed: boolean = false
  private meta: Partial<PluginMeta> = {
    name: '',
    description: '',
    author: '',
    tags: '',
    content: '',
    thumbnailUrls: []
  }

  private mounted() {
    if (this.update) {
      this.meta = Object.assign({}, this.pluginMeta)
    }
  }

  public onFileSelected (event: Event) {
    this.loader = 'loading'
    this.loading = true
    if (event.target instanceof HTMLInputElement) {
      if (!event.target.files) { return }
      const file = event.target.files[0]
      const reader = new FileReader()
      reader.onload = (e: Event) => {
        this.meta.content = reader.result as string
        this.loader = null
        this.loading = false
        this.fileUploaded = true
        this.fileName = file.name

        if (this.meta.name === '') {
          this.meta.name = this.fileName.match(/(.*)(?:\.([^.]+$))/)!![1]
        }
      }
      reader.readAsText(file)
    }
  }

  public async requestUploadPlugin () {
    this.meta.author = this.$store.getters.userName
    console.log(Object.assign({}, this.meta))
    if(this.update) {
      fetch(`${process.env.VUE_APP_API_ORIGIN}/market/plugins/${this.pluginMeta.id}`, {
        method: 'POST',
        body: JSON.stringify(this.meta),
      })
        .then((res) => res.json())
        .then((payload: { state: boolean }) => {
          this.responseCreatePlugin(payload)
        })
    } else {
      // from gist
      if (this.gistUrl) {
        this.meta.content = await fetch(this.gistUrl).then(res => res.text())
        console.log(this.meta.content)
      }

      fetch(`${process.env.VUE_APP_API_ORIGIN}/market/plugins`, {
        method: 'POST',
        body: JSON.stringify(this.meta),
      })
        .then((res) => res.json())
        .then((payload: { state: boolean }) => {
          this.responseCreatePlugin(payload)
        })
    }
  }

  public responseCreatePlugin (payload: { state: boolean }) {
    console.log(payload)
    this.dialog = false
    this.$emit('reload')
  }
}
</script>
