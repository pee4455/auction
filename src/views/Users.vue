<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-4">
          <v-card-title class="text-h5 mb-4">
            <v-icon start color="primary">mdi-login</v-icon>
            เข้าสู่ระบบ
          </v-card-title>

          <v-card-text>
            <v-alert
              v-if="error"
              type="error"
              variant="tonal"
              closable
              class="mb-4"
              @click:close="error = ''"
            >
              {{ error }}
            </v-alert>

            <v-form ref="form" v-model="isFormValid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="ชื่อผู้ใช้"
                :rules="[v => !!v || 'กรุณากรอกชื่อผู้ใช้']"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :disabled="loading"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="รหัสผ่าน"
                :rules="[v => !!v || 'กรุณากรอกรหัสผ่าน']"
                prepend-inner-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                :disabled="loading"
                required
              ></v-text-field>

              <v-checkbox
                v-model="rememberMe"
                label="จำการเข้าสู่ระบบ"
                :disabled="loading"
                hide-details
                class="mb-4"
              ></v-checkbox>

              <v-btn
                block
                color="primary"
                size="large"
                type="submit"
                :loading="loading"
                :disabled="!isFormValid || loading"
              >
                เข้าสู่ระบบ
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import CryptoJS from 'crypto-js'

const router = useRouter()
const form = ref(null)
const isFormValid = ref(false)
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')
const rememberMe = ref(false)

onMounted(() => {
  const savedCredentials = localStorage.getItem('credentials')
  if (savedCredentials) {
    const decrypted = CryptoJS.AES.decrypt(savedCredentials, 'secret-key').toString(CryptoJS.enc.Utf8)
    const { username: savedUsername, password: savedPassword } = JSON.parse(decrypted)
    username.value = savedUsername
    password.value = savedPassword
    rememberMe.value = true
  }
})

const handleLogin = async () => {
  if (!form.value.validate()) return

  loading.value = true
  error.value = ''
  
  try {
    const encryptedPassword = CryptoJS.SHA256(password.value).toString()
    
    const response = await fetch('http://localhost:8000/api/admin/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      const token = data.token || 'dummy-token'
      
      localStorage.setItem('token', token)
      
      if (rememberMe.value) {
        const credentials = JSON.stringify({
          username: username.value,
          password: password.value
        })
        const encrypted = CryptoJS.AES.encrypt(credentials, 'secret-key').toString()
        localStorage.setItem('credentials', encrypted)
      } else {
        localStorage.removeItem('credentials')
      }

      router.push('/admin-management')
    } else {
      error.value = data.message || 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = 'เกิดข้อผิดพลาดในการเชื่อมต่อ กรุณาลองใหม่อีกครั้ง'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style>