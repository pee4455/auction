<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-tabs
            v-model="activeTab"
            color="primary"
            align-tabs="center"
          >
            <v-tab value="users">
              <v-icon start>mdi-account-group</v-icon>
              จัดการผู้ใช้งาน
            </v-tab>
            <v-tab value="auctions">
              <v-icon start>mdi-gavel</v-icon>
              จัดการการประมูล
            </v-tab>
            <v-tab value="carousel">
              <v-icon start>mdi-image-multiple</v-icon>
              จัดการรูปสไลด์
            </v-tab>
            <v-tab value="documents">
              <v-icon start>mdi-file-document</v-icon>
              จัดการเอกสาร
            </v-tab>
          </v-tabs>

          <v-window v-model="activeTab">
            <!-- Users Management -->
            <v-window-item value="users">
              <v-card-text>
                <v-data-table
                  :headers="userHeaders"
                  :items="users"
                  :loading="loading"
                >
                  <template v-slot:item.actions="{ item }">
                    <v-btn
                      icon
                      variant="text"
                      color="primary"
                      @click="editUser(item)"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      variant="text"
                      color="error"
                      @click="deleteUser(item)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-window-item>

            <!-- Auctions Management -->
            <v-window-item value="auctions">
              <v-card-text>
                <v-data-table
                  :headers="auctionHeaders"
                  :items="auctions"
                  :loading="loading"
                >
                  <template v-slot:item.actions="{ item }">
                    <v-btn
                      icon
                      variant="text"
                      color="primary"
                      @click="editAuction(item)"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      variant="text"
                      color="error"
                      @click="deleteAuction(item)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-window-item>

            <!-- Carousel Management -->
            <v-window-item value="carousel">
              <v-card-text>
                <v-row>
                  <v-col
                    v-for="(item, index) in carouselItems"
                    :key="index"
                    cols="12"
                    md="4"
                  >
                    <v-card>
                      <v-img
                        :src="item.image"
                        height="200"
                        cover
                      ></v-img>
                      <v-card-title>{{ item.title }}</v-card-title>
                      <v-card-actions>
                        <v-btn
                          color="primary"
                          variant="text"
                          @click="editCarouselItem(item)"
                        >
                          แก้ไข
                        </v-btn>
                        <v-btn
                          color="error"
                          variant="text"
                          @click="deleteCarouselItem(item)"
                        >
                          ลบ
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-window-item>

            <!-- Documents Management -->
            <v-window-item value="documents">
              <v-card-text>
                <v-data-table
                  :headers="documentHeaders"
                  :items="documents"
                  :loading="loading"
                >
                  <template v-slot:item.actions="{ item }">
                    <v-btn
                      icon
                      variant="text"
                      color="primary"
                      @click="viewDocument(item)"
                    >
                      <v-icon>mdi-eye</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      variant="text"
                      color="error"
                      @click="deleteDocument(item)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('users')
const loading = ref(false)

// Table headers
const userHeaders = [
  { title: 'ชื่อผู้ใช้', key: 'username' },
  { title: 'อีเมล', key: 'email' },
  { title: 'ประเภท', key: 'user_type' },
  { title: 'สถานะ', key: 'status' },
  { title: 'จัดการ', key: 'actions', sortable: false }
]

const auctionHeaders = [
  { title: 'ชื่อการประมูล', key: 'title' },
  { title: 'วันที่', key: 'event_date' },
  { title: 'สถานที่', key: 'location' },
  { title: 'สถานะ', key: 'status' },
  { title: 'จัดการ', key: 'actions', sortable: false }
]

const documentHeaders = [
  { title: 'ชื่อเอกสาร', key: 'name' },
  { title: 'ประเภท', key: 'type' },
  { title: 'วันที่อัพโหลด', key: 'upload_date' },
  { title: 'จัดการ', key: 'actions', sortable: false }
]

// Mock data
const users = ref([])
const auctions = ref([])
const carouselItems = ref([])
const documents = ref([])

// CRUD functions
const editUser = (item) => {
  console.log('Edit user:', item)
}

const deleteUser = (item) => {
  console.log('Delete user:', item)
}

const editAuction = (item) => {
  console.log('Edit auction:', item)
}

const deleteAuction = (item) => {
  console.log('Delete auction:', item)
}

const editCarouselItem = (item) => {
  console.log('Edit carousel item:', item)
}

const deleteCarouselItem = (item) => {
  console.log('Delete carousel item:', item)
}

const viewDocument = (item) => {
  console.log('View document:', item)
}

const deleteDocument = (item) => {
  console.log('Delete document:', item)
}

// Load data
onMounted(async () => {
  loading.value = true
  try {
    // Add API calls here
    // Example:
    // const response = await fetch('/api/users')
    // users.value = await response.json()
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style> 