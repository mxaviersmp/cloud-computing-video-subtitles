<template>
  <q-layout view="lHh Lpr lFf">
    <div class="container">
      <q-card>
        <img class="avatar" src="tubarao.jpg" />
        <q-card-section>
          <q-form @submit="cadastrar" class="q-gutter-md q-pa-sm">
            <q-input
              v-model="user.name"
              label="Seu nome"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Campo em branco']"
            />

            <q-input
              v-model="user.email"
              label="Email"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Campo em branco']"
            />

            <q-input
              type="password"
              v-model="user.password"
              label="Senha"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Campo em branco']"
            />

            <q-input
              type="password"
              v-model="confpass"
              label="Confirmar senha"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Campo em branco',
                (val) => val === user.password || 'As senhas não correspondem',
              ]"
            />

            <div>
              <q-btn
                :loading="loading"
                label="Cadastrar"
                type="submit"
                color="primary"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </div>
  </q-layout>
</template>

<script>
import authService from '../service/authService'
export default {
  data () {
    return {
      user: {
        name: '',
        password: '',
        email: ''
      },
      confpass: '',
      loading: false
    }
  },
  methods: {
    async cadastrar () {
      const { email: username, password, name } = this.user
      try {
        this.loading = true
        await authService.signUp({ username, password, name })
        this.$router.push('/')
      } catch (err) {
        this.$q.notify({
          message: 'Erro ao processar dados',
          color: 'red'
        })
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.container {
  display: flex;
  justify-content: center;
}

.q-card {
  margin-top: 60px;
  height: 580px;
  width: 400px;
  display: flex;
  flex-direction: column;
}

.q-icon {
  margin: 5px;
  margin-left: auto;
  padding: 10px;
  border-radius: 5px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2;
}

.q-icon:hover {
  background-color: #aaa;
}

.avatar {
  margin: 10px auto;
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.q-btn {
  width: 100%;
  height: 40px;
}
</style>
