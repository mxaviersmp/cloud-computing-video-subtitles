<template>
  <q-page>
    <div class="uploader-container">
      <q-uploader
        ref="uploader"
        @finish="finished"
        label="Adicione um arquivo .mp4"
        auto-upload
        extensions=".mp4"
        :factory="uploadVideo"
        :filter="checkFileType"
        @rejected="onRejected"
      />
    </div>

    <q-table
      :loading="loading"
      class="q-mx-lg"
      hide-pagination
      title="Meus uploads"
      :data="uploadsData"
      :columns="columns"
      row-key="name"
      loading-label="Carregando..."
      no-results-label="Nenhum resultado encontrado"
      no-data-label="Você ainda não enviou nenhum arquivo"
    >
       <template v-slot:body-cell-download="props">
        <q-td :props="props">
          <q-btn :disable="!props.value" type="a" :href="props.value" round color="secondary" icon="cloud_download" />
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script>
import videoService from '../service/videoService'
import authService from '../service/authService'

const ALLOWED_FILE_TIPES = ['video/mp4']
export default {
  data () {
    return {
      uploadsData: [],
      loading: false,
      columns: [
        {
          label: 'Nome',
          field: 'video_name',
          required: true,
          align: 'left',
          sortable: true
        },
        {
          name: 'duration',
          label: 'Duração',
          field: 'duration',
          sortable: true,
          format: (val) => this.formatTime(val)
        },
        { label: 'Palavras transcritas', field: 'transcription_words', sortable: true },
        { label: 'Palavras traduzidas', field: 'translation_words', sortable: true },
        {
          label: 'Status',
          field: 'finished',
          sortable: true,
          format: (val) => val === 'True' ? 'Finalizado' : 'Em andamento'
        },
        { label: 'Download', field: 'video_uri', name: 'download' }
      ]
    }
  },
  methods: {
    checkFileType (files) {
      return files.filter((file) => ALLOWED_FILE_TIPES.includes(file.type))
    },
    onRejected (rejectedEntries) {
      this.$q.notify({
        type: 'negative',
        message: 'Tipo de arquivo inválido'
      })
    },
    formatTime (duration) {
      if (duration) { return duration >= 60 ? `${duration / 60} min` : `${duration} s` }
      return ''
    },
    async uploadVideo (files) {
      try {
        const file = files[0]
        const { attributes } = await authService.getCurrentUser()

        const formData = new FormData()
        formData.set('file_name', file.name)
        formData.set('user_id', attributes.sub)
        formData.set('user_email', attributes.email)
        formData.append('file', file)

        await videoService.send(formData)
        this.$q.notify({
          type: 'positive',
          message: 'Video enviado com sucesso'
        })
      } catch {
        this.$q.notify({
          type: 'negative',
          message: 'Erro ao enviar arquivo'
        })
      } finally {
        this.listUploads()
      }
    },
    async listUploads () {
      try {
        this.loading = true
        const { username } = await authService.getCurrentUser()
        this.uploadsData = await videoService.list(username)
      } catch (err) {
        this.$q.notify({
          type: 'negative',
          message: 'Erro ao carregar lista de uploads'
        })
      } finally {
        this.loading = false
      }
    },
    finished () {
      this.$refs.uploader.reset()
    }
  },
  created () {
    this.listUploads()
  }
}
</script>

<style lang="stylus" scoped>
.uploader-container {
  padding: 80px 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
