<template>
  <div>
    <v-snackbar
      v-model="show"
      :timeout="-1"
      location="bottom"
      class="cookie-consent"
    >
      <div class="d-flex align-center flex-wrap gap-4">
        <div class="text-body-1">
          เราใช้คุกกี้เพื่อเพิ่มประสิทธิภาพ และประสบการณ์ที่ดีในการใช้งานเว็บไซต์
        </div>
        <div class="d-flex gap-2">
          <v-btn
            color="primary"
            variant="tonal"
            @click="openSettings"
          >
            ตั้งค่า
          </v-btn>
          <v-btn
            color="primary"
            @click="acceptAllCookies"
          >
            ยอมรับ
          </v-btn>
        </div>
      </div>
    </v-snackbar>

    <v-dialog v-model="showSettings" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 pa-4">
          การตั้งค่าคุกกี้
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-list>
            <v-list-item>
              <template v-slot:prepend>
                <v-checkbox
                  v-model="cookieSettings.necessary"
                  disabled
                  :readonly="true"
                  color="primary"
                ></v-checkbox>
              </template>
              <v-list-item-title>คุกกี้ที่จำเป็น</v-list-item-title>
              <v-list-item-subtitle>
                จำเป็นสำหรับการทำงานของเว็บไซต์
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-checkbox
                  v-model="cookieSettings.functional"
                  color="primary"
                ></v-checkbox>
              </template>
              <v-list-item-title>คุกกี้เพื่อการใช้งาน</v-list-item-title>
              <v-list-item-subtitle>
                ช่วยจดจำการตั้งค่าและการใช้งานของคุณ
              </v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-checkbox
                  v-model="cookieSettings.analytics"
                  color="primary"
                ></v-checkbox>
              </template>
              <v-list-item-title>คุกกี้เพื่อการวิเคราะห์</v-list-item-title>
              <v-list-item-subtitle>
                ช่วยในการวิเคราะห์การใช้งานเว็บไซต์
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="grey-darken-1"
            variant="text"
            @click="showSettings = false"
          >
            ยกเลิก
          </v-btn>
          <v-btn
            color="primary"
            @click="saveCookieSettings"
          >
            บันทึกการตั้งค่า
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const show = ref(false)
const showSettings = ref(false)

const cookieSettings = reactive({
  necessary: true,
  functional: true,
  analytics: true,
  marketing: false
})

const openSettings = () => {
  showSettings.value = true
}

const acceptAllCookies = () => {
  Object.keys(cookieSettings).forEach(key => {
    cookieSettings[key] = true
  })
  saveCookieSettings()
}

const saveCookieSettings = () => {
  try {
    localStorage.setItem('cookieConsent', 'custom')
    localStorage.setItem('cookieSettings', JSON.stringify(cookieSettings))
    show.value = false
    showSettings.value = false
  } catch (error) {
    console.error('Error saving cookie settings:', error)
  }
}

onMounted(() => {
  try {
    const consent = localStorage.getItem('cookieConsent')
    if (!consent) {
      show.value = true
    } else if (consent === 'custom') {
      const savedSettings = localStorage.getItem('cookieSettings')
      if (savedSettings) {
        Object.assign(cookieSettings, JSON.parse(savedSettings))
      }
    }
  } catch (error) {
    console.error('Error loading cookie settings:', error)
    show.value = true
  }
})
</script>

<style scoped>
.cookie-consent {
  max-width: 100%;
}

.v-snackbar.cookie-consent :deep(.v-snackbar__wrapper) {
  max-width: 100%;
  width: 100%;
  background-color: rgba(35, 93, 59, 0.95);
}

@media (max-width: 600px) {
  .cookie-consent :deep(.v-snackbar__wrapper) {
    flex-direction: column;
    padding: 1rem;
  }
  
  .cookie-consent .d-flex {
    flex-direction: column;
    align-items: stretch;
  }
}
</style> 