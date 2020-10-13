<template>
   <q-page>
       <div class="uploader-container">
            <q-uploader
            label="Adicione um arquivo .mp4"
            auto-upload
            url="http://localhost:4444/upload"
            :filter="checkFileType"
            @rejected="onRejected"
            />
       </div>

       <q-table
        hide-bottom
        class="q-mx-lg"
        title="Meus uploads"
        :data="data"
        :columns="columns"
        row-key="name"
        no-results-label="Nenhum resultado encontrado"
        no-data-label="Você ainda não enviou nenhum arquivo"
      />
   </q-page>
</template>

<script>
const ALLOWED_FILE_TIPES = ['video/mp4']

export default {
  data () {
    return {
      columns: [
        {
          name: 'name',
          required: true,
          label: 'Nome',
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'size', align: 'center', label: 'Tamanho', field: 'size', sortable: true, format: val => val && `${val} MB` },
        { name: 'duration', label: 'Duração', field: 'duration', sortable: true, format: val => val && `${val} min` },
        { name: 'words', label: 'Palavras', field: 'words', sortable: true },
        { name: 'date', label: 'Data', field: 'date', sortable: true },
        { name: 'status', label: 'Status', field: 'status', sortable: true },
        { name: 'download', label: 'Download', field: 'download' }
      ],

      data: [
        {
          name: 'Video A',
          size: 20,
          duration: 10,
          words: 240,
          date: '27/09/2020',
          status: 'Em andamento'
        },
        {
          name: 'Video B',
          size: 10,
          duration: 5,
          words: 57,
          date: '16/04/2020',
          status: 'Finalizado'
        },
        {
          name: 'Video C',
          size: 22,
          duration: 18,
          words: 432,
          date: '01/08/2020',
          status: 'Finalizado'
        }

      ]
    }
  },
  methods: {
    checkFileType (files) {
      return files.filter(file => ALLOWED_FILE_TIPES.includes(file.type))
    },
    onRejected (rejectedEntries) {
      this.$q.notify({
        type: 'negative',
        message: 'Tipo de arquivo inválido'
      })
    }
  }
}
</script>

<style lang="stylus" scoped>
    .uploader-container{
        padding 80px 0
        display flex
        align-items center
        justify-content center
    }
</style>
