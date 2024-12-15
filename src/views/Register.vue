<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6">
          <v-card-title class="text-h4 mb-4">
            <v-icon large color="primary" class="mr-2">mdi-account-plus</v-icon>
            ลงทะเบียนสมาชิกใหม่
          </v-card-title>

          <v-card-text>
            <!-- Terms and Conditions Section -->
            <v-sheet class="mb-6 pa-4" color="grey-lighten-4" rounded>
              <div class="text-h6 mb-4">ข้อตกลงและเงื่อนไขการขายทอดตลาด</div>
              
              <v-expansion-panels>
                <!-- Basic Registration Info -->
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    การสมัครสมาชิกและเอกสารประกอบ
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <div class="terms-content">
                      <p>1. ผู้สนใจเข้าร่วมการขายทอดตลาด ต้องสมัครสมาชิกผ่านทางเว็บไซต์ โดยกรอกข้อมูลรายละเอียดในใบสมัครให้ครบถ้วน ถูกต้องตามความเป็นจริง</p>
                      <p>2. ผู้สมัครต้องศึกษา ข้อตกลงและเงื่อนไขการขายทอดตลาด ยอมรับและยินยอมปฏิบัติตามภายใต้เงื่อนไขดังกล่าว</p>
                      
                      <div class="mt-4">
                        <strong>เอกสารประกอบการสมัครสมาชิกใหม่:</strong>
                        <div class="ml-4 mt-2">
                          <strong>บุคคลธรรมดา</strong>
                          <ul>
                            <li>สำเนาบัตรประจำตัวประชาชน</li>
                            <li>หนังสือมอบอำนาจ สำเนาบัตรประจำตัวประชาชนของผู้มอบอำนาจและผู้รับมอบอำนาจ (กรณีไม่เข้าร่วมการขายทอดตลาดด้วยตนเอง)</li>
                          </ul>
                          
                          <strong>นิติบุคคล</strong>
                          <ul>
                            <li>สำเนาหนังสือรับรองบริษัท ออกให้ไว้ไม่เกิน 3 เดือน และสำเนาภพ.20</li>
                            <li>สำเนาบัตรประจำตัวประชาชนของหุ้นส่วนผู้จัดการหรือกรรมการบริษัทผู้มีอำนาจลงนาม</li>
                            <li>กรณีมอบอำนาจ - หนังสือมอบอำนาจ พร้อมเอกสารที่เกี่ยวข้อง</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </v-expansion-panel-text>
                </v-expansion-panel>

                <!-- Auction Rules -->
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    การขายทอดตลาดออนไลน์และการวางหลักประกัน
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <div class="terms-content">
                      <strong>การวางหลักประกัน:</strong>
                      <ul>
                        <li>ผู้สมัครต้องวางหลักประกันอย่างน้อย 10% ของมูลค่าทรัพย์สินที่ต้องการประมูล</li>
                        <li>มูลค่าหลักประกันจะแตกต่างกันไปตามประเภทและมูลค่าของทรัพย์สิน</li>
                      </ul>

                      <strong>วิธีการเข้าร่วมการขายทอดตลาด:</strong>
                      <ul>
                        <li>การขายทอดตลาดออนไลน์แบบปกติ - เสนอราคาพร้อมกันในเวลาจริง</li>
                        <li>การขายทอดตลาดแบบเสนอราคาสูงสุด - เสนอราคาล่วงหน้า</li>
                      </ul>
                    </div>
                  </v-expansion-panel-text>
                </v-expansion-panel>

                <!-- Member Rights and Responsibilities -->
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    สิทธิและความรับผิดชอบของสมาชิก
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <div class="terms-content">
                      <strong>สิทธิตาม พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล:</strong>
                      <ul>
                        <li>สิทธิในการขอเข้าถึงและขอรับสำเนาข้อมูลส่วนบุคคล</li>
                        <li>สิทธิในการขอแก้ไขข้อมูล</li>
                        <li>สิทธิในการขอรับข้อมูลส่วนบุคคล</li>
                        <li>สิทธิในการขอลบหรือทำลายข้อมูล</li>
                        <li>สิทธิในการขอระงับการใช้ข้อมูล</li>
                        <li>สิทธิในการถอนความยินยอม</li>
                        <li>สิทธิในการขอคัดค้าน</li>
                      </ul>
                    </div>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-sheet>

            <!-- Agreement Checkbox -->
            <v-checkbox
              v-model="termsAccepted"
              color="primary"
              :rules="[v => !!v || 'กรุณายอมรับข้อตกลงและเงื่อนไข']"
            >
              <template v-slot:label>
                <div class="text-body-2">
                  ข้าพเจ้าได้อ่าน เข้าใจ รับทราบ และยอมรับถึงข้อปฏิบัติตามเงื่อนไข ข้อตกลงและเงื่อนไขการขายทอดตลาด 
                  ดังกล่าวข้างต้น และประกาศนโยบายความเป็นส่วนตัว (Privacy Notice)
                </div>
              </template>
            </v-checkbox>

            <!-- Register Button -->
            <v-btn
              color="primary"
              block
              size="large"
              :disabled="!termsAccepted"
              @click="proceedToRegistration"
              class="mt-6"
            >
              ดำเนินการลงทะเบียน
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const termsAccepted = ref(false)

const proceedToRegistration = () => {
  if (termsAccepted.value) {
    // Proceed to registration form
    router.push('/registration-form')
  }
}
</script>

<style scoped>
.terms-content {
  font-size: 0.9rem;
  line-height: 1.6;
}

.terms-content ul {
  padding-left: 20px;
  margin: 8px 0;
}

.terms-content li {
  margin-bottom: 4px;
}

.v-expansion-panels {
  margin-bottom: 20px;
}

:deep(.v-expansion-panel-title) {
  font-size: 1rem;
  font-weight: 500;
}
</style> 