<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-4">
            <v-icon large color="primary" class="mr-2">mdi-account-plus</v-icon>
            แบบฟอร์มลงทะเบียน
          </v-card-title>

          <v-card-text>
            <v-form ref="form" v-model="isFormValid">
              <!-- Previous Participation -->
              <div class="mb-4">
                <label class="text-subtitle-1 mb-2 d-block">ท่านเคยเข้าร่วมประมูลกับ บมจ.สหการประมูลหรือไม่</label>
                <v-radio-group v-model="hasPreviousParticipation" inline>
                  <v-radio label="เคยเข้าร่วมประมูล" value="true"></v-radio>
                  <v-radio label="ไม่เคยเข้าร่วมประมูล" value="false"></v-radio>
                </v-radio-group>
              </div>

              <!-- Nationality -->
              <div class="mb-4">
                <label class="text-subtitle-1 mb-2 d-block">สัญชาติ</label>
                <v-radio-group v-model="nationality" inline>
                  <v-radio label="สัญชาติไทย" value="thai"></v-radio>
                  <v-radio label="ไม่ใช่สัญชาติไทย" value="foreign"></v-radio>
                </v-radio-group>
              </div>

              <!-- Registration Type -->
              <div class="mb-4">
                <label class="text-subtitle-1 mb-2 d-block">ลงทะเบียนในนาม</label>
                <v-radio-group v-model="registrationType" inline>
                  <v-radio label="บุคคลธรรมดา" value="personal"></v-radio>
                  <v-radio label="นิติบุคคล" value="corporate"></v-radio>
                </v-radio-group>
              </div>

              <!-- Basic Information -->
              <v-row>
                <v-col cols="12" md="4">
                  <v-select
                    v-model="title"
                    :items="titleOptions"
                    label="คำนำหน้าชื่อ"
                    variant="outlined"
                    density="comfortable"
                  ></v-select>
                </v-col>
                <v-col cols="12" md="8">
                  <v-text-field
                    v-model="fullName"
                    label="ชื่อ-นามสกุล"
                    variant="outlined"
                    density="comfortable"
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- ID/Tax Number -->
              <v-text-field
                v-model="idNumber"
                :label="registrationType === 'personal' ? 'เลขที่บัตรประชาชน' : 'เลขผู้เสียภาษี'"
                variant="outlined"
                density="comfortable"
                class="mb-4"
              ></v-text-field>

              <!-- Contact Information -->
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="phone"
                    label="โทรศัพท์"
                    variant="outlined"
                    density="comfortable"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="email"
                    label="E-mail"
                    variant="outlined"
                    density="comfortable"
                    type="email"
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- Date Fields -->
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="birthDate"
                    :label="registrationType === 'personal' ? 'วันเดือนปีเกิด' : 'วันที่จดทะเบียนนิติบุคคล'"
                    variant="outlined"
                    density="comfortable"
                    type="date"
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- Additional Corporate Fields -->
              <template v-if="registrationType === 'corporate'">
                <v-text-field
                  v-model="businessType"
                  label="อาชีพ/ประเภทธุรกิจ"
                  variant="outlined"
                  density="comfortable"
                  class="mb-4"
                ></v-text-field>

                <v-row>
                  <v-col cols="6">
                    <v-text-field
                      v-model="businessYears"
                      label="ระยะเวลาประกอบกิจการ (ปี)"
                      variant="outlined"
                      density="comfortable"
                      type="number"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      v-model="businessMonths"
                      label="เดือน"
                      variant="outlined"
                      density="comfortable"
                      type="number"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </template>

              <!-- Address Fields (Only for new registrations) -->
              <template v-if="hasPreviousParticipation === 'false'">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="address.houseNumber"
                      label="บ้านเลขที่"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="address.moo"
                      label="หมู่"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="address.soi"
                      label="ซอย"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      v-model="address.road"
                      label="ถนน"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="address.subdistrict"
                      label="แขวง/ตำบล"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="address.district"
                      label="เขต/อำเภอ"
                      variant="outlined"
                      density="comfortable"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="4">
                    <v-select
                      v-model="address.province"
                      :items="provinces"
                      label="จังหวัด"
                      variant="outlined"
                      density="comfortable"
                    ></v-select>
                  </v-col>
                </v-row>

                <v-text-field
                  v-model="address.postalCode"
                  label="รหัสไปรษณีย์"
                  variant="outlined"
                  density="comfortable"
                  class="mb-4"
                ></v-text-field>
              </template>

              <!-- Submit Button -->
              <v-btn
                color="primary"
                block
                size="large"
                :disabled="!isFormValid"
                @click="submitForm"
                class="mt-6"
              >
                ลงทะเบียน
                <v-icon end>mdi-check</v-icon>
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref(null)
const isFormValid = ref(false)

// Form Fields
const hasPreviousParticipation = ref('false')
const nationality = ref('thai')
const registrationType = ref('personal')
const title = ref('')
const fullName = ref('')
const idNumber = ref('')
const phone = ref('')
const email = ref('')
const birthDate = ref('')
const businessType = ref('')
const businessYears = ref('')
const businessMonths = ref('')

// Address Fields
const address = ref({
  houseNumber: '',
  moo: '',
  soi: '',
  road: '',
  subdistrict: '',
  district: '',
  province: '',
  postalCode: ''
})

// Options
const titleOptions = [
  'นาย',
  'นาง',
  'นางสาว',
  'ดร.',
  'MR.',
  'MRS.',
  'MS.',
  'นรจ.',
  'นมจ.',
  'บริษัท',
  'ร้าน',
  'ว่าที่ร.ต.',
  'หจก.'
]
const provinces = ['กรุงเทพมหานคร', 'นนทบุรี', 'ปทุมธานี'] // Add more provinces as needed

const submitForm = async () => {
  if (!form.value.validate()) return

  try {
    // Add your form submission logic here
    console.log('Form submitted:', {
      hasPreviousParticipation: hasPreviousParticipation.value,
      nationality: nationality.value,
      registrationType: registrationType.value,
      title: title.value,
      fullName: fullName.value,
      idNumber: idNumber.value,
      phone: phone.value,
      email: email.value,
      birthDate: birthDate.value,
      businessType: businessType.value,
      businessYears: businessYears.value,
      businessMonths: businessMonths.value,
      address: address.value
    })

    // Navigate to success page or show success message
    // router.push('/registration-success')
  } catch (error) {
    console.error('Registration failed:', error)
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