<template>
  <v-container fluid>
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card elevation="2" class="rounded-lg overflow-hidden">
          <v-carousel
            cycle
            height="400"
            hide-delimiter-background
            show-arrows="hover"
          >
            <v-carousel-item
              v-for="(slide, i) in slides"
              :key="i"
            >
              <v-img
                :src="slide.src"
                height="400"
                cover
                class="align-end"
              >
                <div class="text-overlay">
                  <h2 class="text-h4 font-weight-bold text-white mb-2">
                    {{ slide.title }}
                  </h2>
                  <p class="text-subtitle-1 text-white">
                    {{ slide.description }}
                  </p>
                </div>
              </v-img>
            </v-carousel-item>
          </v-carousel>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- ส่วนปฏิทิน -->
      <v-col cols="12" md="8">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="d-flex align-center py-4 px-6">
            <v-icon color="primary" class="mr-2">mdi-calendar</v-icon>
            ปฏิทินการประมูล
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-4">
            <div class="calendar-container">
              <div class="calendar-header d-flex align-center justify-space-between mb-4">
                <v-btn icon="mdi-chevron-left" @click="previousMonth"></v-btn>
                <h3>{{ currentMonthYear }}</h3>
                <v-btn icon="mdi-chevron-right" @click="nextMonth"></v-btn>
              </div>
              <table class="calendar-table">
                <thead>
                  <tr>
                    <th v-for="day in weekDays" :key="day">{{ day }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="week in calendar" :key="week[0].date">
                    <td 
                      v-for="day in week" 
                      :key="day.date"
                      :class="{
                        'current-month': day.currentMonth,
                        'selected': isSelectedDate(day.date),
                        'has-events': getEventsForDate(day.date).length > 0
                      }"
                      @click="selectDate(day.date)"
                    >
                      <div class="date-cell">
                        <span class="date-number">{{ new Date(day.date).getDate() }}</span>
                        <div class="event-indicators" v-if="getEventsForDate(day.date).length">
                          <span class="event-count">{{ getEventsForDate(day.date).length }}</span>
                          <div class="event-dots">
                            <span 
                              v-for="event in getEventsForDate(day.date)" 
                              :key="event.id"
                              class="event-dot"
                              :style="{ backgroundColor: 'primary' }"
                            ></span>
                          </div>
                        </div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- ส่วนแสดงรายการประมูล -->
      <v-col cols="12" md="4">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="d-flex align-center py-4 px-6">
            <v-icon color="primary" class="mr-2">mdi-gavel</v-icon>
            รายการประมูลวันที่ {{ selectedDate }}
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-list v-if="selectedDateAuctions.length > 0">
              <v-list-item
                v-for="auction in selectedDateAuctions"
                :key="auction.id"
                :title="auction.title"
                :subtitle="`ราคาเริ่มต้น: ${auction.startPrice.toLocaleString()} บาท`"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" variant="tonal">
                    <span class="text-body-2">{{ auction.items }}</span>
                  </v-avatar>
                </template>
                <template v-slot:append>
                  <div class="d-flex flex-column gap-2">
                    <v-btn
                      size="small"
                      color="primary"
                      variant="tonal"
                      prepend-icon="mdi-file-pdf-box"
                      @click="openPdf(auction.pdfUrl)"
                    >
                      รายละเอียด
                    </v-btn>
                    <v-btn
                      size="small"
                      color="grey"
                      variant="tonal"
                      prepend-icon="mdi-printer"
                      @click="printDetails(auction)"
                    >
                      พิมพ์
                    </v-btn>
                  </div>
                </template>
              </v-list-item>
            </v-list>
            <div v-else class="text-center pa-4">
              ไม่มีรายการประมูลในวันที่เลือก
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <CookieConsent />
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import CookieConsent from '@/components/CookieConsent.vue'
const pdfPath = require('@/assets/pdf/Rest-92299.pdf')

// ข้อมูลตัวอย่างการประมูล
const auctionEvents = ref([
  {
    id: 1,
    date: new Date().toISOString().split('T')[0],
    title: 'ประมูลรถยนต์ Toyota Camry 2.0G',
    location: 'สำนักงานใหญ่',
    items: '1',
    description: 'รถยนต์มือสอง สภาพดี ปี 2020 สีขาวมุก เลขไมล์ 50,000 กม.',
    startPrice: 750000,
    pdfUrl: pdfPath.default,
    status: 'upcoming',
    color: 'primary'
  },
  {
    id: 2,
    date: new Date().toISOString().split('T')[0],
    title: 'ประมูลรถจักรยานยนต์ Honda PCX160',
    location: 'สาขาเชียงใหม่',
    items: '3',
    description: 'รถจักรยานยนต์มือสอง สภาพดี ปี 2023 สีดำ-แดง',
    startPrice: 65000,
    pdfUrl: pdfPath.default,
    status: 'upcoming',
    color: 'secondary'
  }
])

// วันที่ปัจจุบันและที่เลือก
const currentDate = ref(new Date())
const selectedDate = ref(new Date().toISOString().substr(0, 10))

// คำนวณรายการประมูลของวันที่เลือก
const selectedDateAuctions = computed(() => {
  console.log('Filtering events for date:', selectedDate.value)
  console.log('Available events:', auctionEvents.value)
  return auctionEvents.value.filter(event => event.date === selectedDate.value)
})

// ฟังก์ชันสำหรับปฏิทิน
const weekDays = ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส']
const currentMonthYear = computed(() => {
  const months = [
    'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
    'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
  ]
  return `${months[currentDate.value.getMonth()]} ${currentDate.value.getFullYear() + 543}`
})

const calendar = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const weeks = []
  let currentWeek = []
  
  // เพิ่มวันจากเดือนก่อนหน้า
  for (let i = 0; i < firstDay.getDay(); i++) {
    const prevDate = new Date(year, month, -i)
    currentWeek.unshift({
      date: prevDate.toISOString().substr(0, 10),
      currentMonth: false
    })
  }
  
  // เพิ่มวันในเดือนปัจจุบัน
  for (let date = 1; date <= lastDay.getDate(); date++) {
    const currentDate = new Date(year, month, date)
    if (currentWeek.length === 7) {
      weeks.push(currentWeek)
      currentWeek = []
    }
    currentWeek.push({
      date: currentDate.toISOString().substr(0, 10),
      currentMonth: true
    })
  }
  
  // เพิ่มวันจากเดือนถัดไป
  while (currentWeek.length < 7) {
    const nextDate = new Date(year, month + 1, currentWeek.length - lastDay.getDate())
    currentWeek.push({
      date: nextDate.toISOString().substr(0, 10),
      currentMonth: false
    })
  }
  weeks.push(currentWeek)
  
  return weeks
})

// ฟังก์ชันจัดการการคลิก
const selectDate = (date) => {
  selectedDate.value = date
  console.log('Selected date:', date)
  console.log('Events for date:', selectedDateAuctions.value)
}

const previousMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1)
}

const getEventsForDate = (date) => {
  const events = auctionEvents.value.filter(event => event.date === date)
  console.log('Events for date', date, ':', events)
  return events
}

const isSelectedDate = (date) => {
  return date === selectedDate.value
}

// ฟังก์ชันสำหรับปุ่มกดต่างๆ
const openPdf = (url) => {
  window.open(url, '_blank')
}

const printDetails = (auction) => {
  window.print()
}

const downloadCalendar = () => {
  // Logic for downloading calendar
  console.log('Downloading calendar...')
}

// เพิ่มข้อมูล slides สำหรับ carousel
const slides = ref([
  {
    src: 'https://images.unsplash.com/photo-1506399309177-3b43e99fead2?q=80&w=2068&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    title: 'ประมูลรถยนต์ประจำเดือน',
    description: 'พบกับรถยนต์คุณภาพดีพร้อมราคาพิเศษ'
  },
  {
    src: 'https://images.unsplash.com/photo-1590859808308-3d2d9c515b1a?q=80&w=2074&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    title: 'ประมูลรถยนต์ประจำเดือน',
    description: 'พบกับรถยนต์คุณภาพดีพร้อมราคาพิเศษ'
  },
  {
    src: 'https://images.unsplash.com/photo-1533497016719-cb32082a2338?q=80&w=1786&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    title: 'ประมูลรถยนต์ประจำเดือน',
    description: 'พบกับรถยนต์คุณภาพดีพร้อมราคาพิเศษ'
  }

])
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-2px);
}

.department-select {
  min-width: 200px;
}

/* Custom calendar styling */
:deep(.v-calendar) {
  background-color: white;
}

:deep(.v-calendar-weekly__head-weekday) {
  font-size: 0.9rem;
  font-weight: 600;
}

:deep(.v-calendar-weekly__day-label) {
  font-size: 0.9rem;
  font-weight: 500;
}

:deep(.v-event) {
  border-radius: 4px;
  padding: 2px 4px;
}

:deep(.v-event-summary) {
  font-size: 0.85rem;
  font-weight: 500;
}

@media print {
  .v-btn {
    display: none;
  }
}

.calendar-container {
  width: 100%;
  padding: 1rem;
}

.calendar-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 4px;
}

.calendar-table th {
  padding: 8px;
  text-align: center;
  font-weight: 500;
  color: #666;
}

.calendar-table td {
  padding: 0;
  text-align: center;
  vertical-align: top;
  height: 80px;
  border-radius: 8px;
  background-color: #f5f5f5;
  cursor: pointer;
  transition: all 0.2s;
}

.calendar-table td:hover {
  background-color: #e0e0e0;
}

.date-cell {
  padding: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.date-number {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 4px;
}

.current-month {
  background-color: white;
  border: 1px solid #e0e0e0;
}

.selected {
  background-color: #e3f2fd !important;
  border: 2px solid #1976d2 !important;
}

.has-events {
  background-color: #f0f7f3 !important;
}

.has-events .date-number {
  color: #235d3b;
  font-weight: 600;
}

.event-indicators {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.event-count {
  font-size: 0.8rem;
  font-weight: 500;
  color: #1976d2;
}

.event-dots {
  display: flex;
  gap: 2px;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 100%;
}

.event-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin: 1px;
  background-color: #235d3b;
}

td:not(.current-month) {
  opacity: 0.5;
}

.text-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 2rem;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  text-align: left;
}
</style>