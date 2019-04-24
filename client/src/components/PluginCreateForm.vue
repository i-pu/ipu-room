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
              @click="submit"
            ) 作成
</template>

<script>
export default {
  name: 'PluginCreateForm',
  data () {
    return {
      dialog: false,
      valid: false,
      name: '',
      description: '',
      loader: null,
      fileName: '',
      fileUploaded: false,
      fileContent: '',
      loading: false,
      agreed: false
    }
  },
  created () {},
  methods: {
    onFileSelected (e) {
      this.loader = 'loading'
      this.loading = true
      const files = e.target.files || e.dataTransfer.files
      let reader = new FileReader()
      reader.onload = (e) => {
        this.fileContent = e.target.result
        this.loader = null
        this.loading = false
        this.fileUploaded = true
        this.fileName = files[0].name

        if (this.name === '') {
          this.name = this.fileName.match(/(.*)(?:\.([^.]+$))/)[1]
        }
      }
      reader.readAsText(files[0])
    },
    submit () {
      this.dialog = false
      console.log('submitted')
      console.log({
        name: this.name,
        description: this.description,
        fileContent: this.fileContent
      })
    }
  }
}
</script>

<style scoped lang='stylus'>

</style>