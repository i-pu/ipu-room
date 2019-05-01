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
                    v-text-field(
                      v-model="name"
                      :counter="12"
                      :rules="[v => !!v || '必須項目です']",
                      label="プラグイン名"
                      required
                    )

                  v-flex(xs12)
                    v-textarea(
                      v-model="description"
                      label="説明"
                      :counter="200"
                    )

                  v-flex(xs12)
                    v-btn(
                      :loading="loading"
                      :disabled="loading || fileUploaded"
                      color="blue-grey"
                      class="white--text"
                      @click="$refs.uploader.click()"
                    ) {{ fileUploaded ? fileName : 'pythonファイルをアップロード' }}
                      input(
                        type="file"
                        accept=".py"
                        ref="uploader"
                        @change="onFileSelected"
                        hidden
                      )
                      v-icon(right dark) cloud_upload

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

@Component({
  sockets: {
    register (data) {
      this.responseCreatePlugin(data)
    }
  }
})
export default class PluginCreateForm extends Vue {
  private dialog: boolean = false
  private valid: boolean = false
  private name: string = ''
  private description: string = ''
  private loader: any = null
  private fileName: string = ''
  private fileUploaded: boolean = false
  private fileContent: string = ''
  private loading: boolean = false
  private agreed: boolean = false

  onFileSelected (event: Event) {
    this.loader = 'loading'
    this.loading = true
    if (event.target instanceof HTMLInputElement) {
      if (!event.target.files) { return }
      const file = event.target.files[0]
      const reader = new FileReader()
      reader.onload = (e: Event) => {
        this.fileContent = reader.result as string
        this.loader = null
        this.loading = false
        this.fileUploaded = true
        this.fileName = file.name

        if (this.name === '') {
          this.name = this.fileName.match(/(.*)(?:\.([^.]+$))/)!![1]
        }
      }
      reader.readAsText(file)
    }
  }

  requestCreatePlugin () {
    if (this.$store.getters.localOnly) {
      this.responseCreatePlugin({})
    } else { 
      this.$socket.emit('register_plugin', {
        plugin_name: this.name,
        python_file: this.fileContent,
      })
    }
  }

  responseCreatePlugin (data: {}) {
    console.log(data)
    this.dialog = false
  }
}
</script>
