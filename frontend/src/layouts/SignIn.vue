<template>
  <q-layout view="lHh Lpr lFf">
    <div class="container">
      <q-card>
        <img class="avatar" src="tubarao.jpg" />
        <q-card-section>
          <q-form class="q-gutter-md q-pa-sm" @submit="login">
            <q-input
              v-model="user.username"
              label="Seu email"
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

            <div>
              <q-btn
                :loading="loading"
                label="Entrar"
                type="submit"
                color="primary"
              />
            </div>

            <div class="row justify-center">
              <span
                >Não é cadastrado?<span
                  class="signUp"
                  @click="$router.push('signUp')"
                >
                  Cadastre-se</span
                >
              </span>
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
        password: '',
        username: ''
      },
      loading: false
    }
  },
  methods: {
    async login () {
      const { username, password } = this.user
      try {
        this.loading = true
        await authService.signIn({ username, password })
        this.$router.push('home')
      } catch (err) {
        this.$q.notify({
          message: 'Email ou senha incorretos',
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
  margin-top: 100px;
  width: 350px;
  height: 420px;
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

.signUp {
  cursor: pointer;
  color: $primary;
  align-self: flex-end;
}

.q-btn {
  height: 40px;
  width: 100%;
}
</style>
