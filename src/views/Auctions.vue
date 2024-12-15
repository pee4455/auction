<template>
  <v-container fluid>
    <!-- Live Bidding Dashboard -->
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-2">mdi-gavel</v-icon>
            การประมูลปัจจุบัน: รถยนต์ Toyota Camry 2.0G
            <v-spacer></v-spacer>
            <v-chip
              :color="auctionStatus.color"
              class="ml-2"
            >
              {{ auctionStatus.text }}
            </v-chip>
          </v-card-title>

          <v-card-text>
            <v-row>
              <!-- Current Price Display -->
              <v-col cols="12" md="4">
                <v-card variant="outlined" class="text-center pa-4">
                  <div class="text-h6 mb-2">ราคาปัจจุบัน</div>
                  <div class="text-h3 font-weight-bold text-primary">
                    ฿{{ formatPrice(currentPrice) }}
                  </div>
                  <div class="text-body-2 mt-2">
                    <v-icon color="success" size="small">mdi-arrow-up</v-icon>
                    เพิ่มขึ้น ฿{{ formatPrice(currentPrice - startingPrice) }}
                  </div>
                  <div class="text-caption text-grey mt-1">
                    ราคาเริ่มต้น: ฿{{ formatPrice(startingPrice) }}
                  </div>
                </v-card>
              </v-col>

              <!-- Timer Display -->
              <v-col cols="12" md="4">
                <v-card variant="outlined" class="text-center pa-4">
                  <div class="text-h6 mb-2">เวลาที่เหลือ</div>
                  <div class="text-h3 font-weight-bold" :class="timeLeft < 60 ? 'text-error' : 'text-primary'">
                    {{ formatTime(timeLeft) }}
                  </div>
                  <div class="text-body-2 mt-2">
                    <v-icon color="info" size="small">mdi-clock-outline</v-icon>
                    เริ่มเมื่อ {{ formatDateTime(startTime) }}
                  </div>
                  <div class="text-caption text-grey mt-1">
                    สิ้นสุดเวลา {{ formatDateTime(new Date(startTime.getTime() + timeLeft * 1000)) }}
                  </div>
                </v-card>
              </v-col>

              <!-- Bidder Info -->
              <v-col cols="12" md="4">
                <v-card variant="outlined" class="text-center pa-4">
                  <div class="text-h6 mb-2">ผู้ประมูลปัจจุบัน</div>
                  <div class="text-h3 font-weight-bold text-primary">
                    #{{ currentBidder || '-' }}
                  </div>
                  <div class="text-body-2 mt-2">
                    <v-icon color="info" size="small">mdi-account-group</v-icon>
                    ผู้เข้าร่วมทั้งหมด {{ totalBidders }} คน
                  </div>
                  <div class="text-caption text-grey mt-1">
                    จำนวนการประมูล {{ biddingHistory.length }} ครั้ง
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Admin Control Panel -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-2">mdi-shield-crown</v-icon>
            แผงควบคุมสำหรับผู้ดูแล
          </v-card-title>

          <v-card-text>
            <v-row>
              <!-- Auction Setup -->
              <v-col cols="12">
                <v-card variant="outlined" class="pa-4 mb-4">
                  <div class="text-subtitle-1 mb-3">ตั้งค่าการประมูล</div>
                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="initialPrice"
                        label="ราคาเริ่มต้น"
                        type="number"
                        prefix="฿"
                        :disabled="isAuctionActive"
                        hide-details
                        density="compact"
                        class="mb-3"
                      ></v-text-field>
                      <v-text-field
                        v-model="initialTime"
                        label="เวลาประมูล (นาที)"
                        type="number"
                        :disabled="isAuctionActive"
                        hide-details
                        density="compact"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="minBidIncrement"
                        label="การเพิ่มราคาขั้นต่ำ"
                        type="number"
                        prefix="฿"
                        :disabled="isAuctionActive"
                        hide-details
                        density="compact"
                        class="mb-3"
                      ></v-text-field>
                      <v-select
                        v-model="quickBidIncrements"
                        label="การเพิ่มราคาด่วน"
                        :items="availableIncrements"
                        multiple
                        chips
                        :disabled="isAuctionActive"
                        hide-details
                        density="compact"
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-card>

                <!-- Auction Controls -->
                <div class="d-flex flex-wrap gap-2 mb-4">
                  <v-btn
                    color="success"
                    :disabled="isAuctionActive"
                    @click="startAuction"
                    prepend-icon="mdi-play"
                    class="flex-grow-1"
                  >
                    {{ isPaused ? 'ดำเนินการต่อ' : 'เริ่มการประมูล' }}
                  </v-btn>
                  <v-btn
                    color="error"
                    :disabled="!isAuctionActive"
                    @click="stopAuction"
                    prepend-icon="mdi-stop"
                    class="flex-grow-1"
                  >
                    หยุดการประมูล
                  </v-btn>
                  <v-btn
                    color="warning"
                    :disabled="!isAuctionActive"
                    @click="pauseAuction"
                    prepend-icon="mdi-pause"
                    class="flex-grow-1"
                  >
                    พักการประมูล
                  </v-btn>
                  <v-btn
                    color="success"
                    variant="elevated"
                    @click="finishAuction"
                    :disabled="!isAuctionActive"
                    class="flex-grow-1"
                    prepend-icon="mdi-trophy"
                  >
                    จบการประมูล
                  </v-btn>
                </div>

                <!-- Time Management -->
                <v-card variant="outlined" class="pa-4 mb-4">
                  <div class="text-subtitle-1 mb-3">การจัดการเวลา</div>
                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="timeAdjustment"
                        label="ปรับเวลา (วินาที)"
                        type="number"
                        hide-details
                        density="compact"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <div class="d-flex gap-2">
                        <v-btn
                          color="primary"
                          variant="outlined"
                          @click="adjustTime(timeAdjustment)"
                          :disabled="!isAuctionActive"
                          class="flex-grow-1"
                        >
                          ปรับเวลา
                        </v-btn>
                        <v-btn
                          color="primary"
                          variant="outlined"
                          @click="extendTime(30)"
                          :disabled="!isAuctionActive"
                          class="flex-grow-1"
                        >
                          +30 วินาที
                        </v-btn>
                      </div>
                    </v-col>
                  </v-row>
                </v-card>

                <!-- Congratulation Dialog -->
                <v-dialog v-model="showCongrats" max-width="500">
                  <v-card class="text-center pa-6 congratulation-card">
                    <div class="firework"></div>
                    <div class="firework"></div>
                    <div class="firework"></div>
                    
                    <v-icon size="64" color="warning" class="mb-4">mdi-trophy</v-icon>
                    <h2 class="text-h4 mb-4">🎉 การประมูลสิ้นสุดแล้ว 🎉</h2>
                    
                    <div class="text-body-1 mb-4">
                      ผู้ชนะการประมูล: 
                      <v-chip color="primary" class="ma-2">
                        #{{ currentBidder }}
                      </v-chip>
                    </div>
                    
                    <div class="text-h5 mb-6">
                      ราคาสุดท้าย: 
                      <span class="text-primary">฿{{ formatPrice(currentPrice) }}</span>
                    </div>

                    <v-btn
                      color="primary"
                      variant="elevated"
                      @click="closeCongrats"
                      class="px-8"
                    >
                      ปิด
                    </v-btn>
                  </v-card>
                </v-dialog>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Bidding History -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-2">mdi-history</v-icon>
            ประวัติการประมูล
            <v-spacer></v-spacer>
            <v-btn
              color="error"
              variant="text"
              density="compact"
              prepend-icon="mdi-delete"
              @click="clearHistory"
            >
              ล้างประวัติ
            </v-btn>
            <v-chip color="info" size="small" class="ml-2">{{ biddingHistory.length }} รายการ</v-chip>
          </v-card-title>

          <v-card-text>
            <v-table hover>
              <thead>
                <tr>
                  <th class="text-left">เวลา</th>
                  <th class="text-left">ผู้ประมูล</th>
                  <th class="text-right">ราคา</th>
                  <th class="text-center">สถานะ</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="bid in biddingHistory" :key="bid.id">
                  <td>{{ formatDateTime(bid.timestamp) }}</td>
                  <td>
                    <v-chip size="small" color="primary" variant="outlined">
                      #{{ bid.bidderId }}
                    </v-chip>
                  </td>
                  <td class="text-right">฿{{ formatPrice(bid.amount) }}</td>
                  <td class="text-center">
                    <v-chip
                      :color="bid.status === 'accepted' ? 'success' : 'error'"
                      size="small"
                    >
                      {{ bid.status === 'accepted' ? 'ยอมรับ' : 'ปฏิเสธ' }}
                    </v-chip>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Auction Configuration
const initialPrice = ref(3290000)
const initialTime = ref(5) // minutes
const minBidIncrement = ref(1000)
const availableIncrements = [1000, 5000, 10000, 50000, 100000]
const quickBidIncrements = ref([1000, 5000, 10000])

// Auction State
const currentPrice = ref(initialPrice.value)
const startingPrice = ref(initialPrice.value)
const timeLeft = ref(initialTime.value * 60)
const startTime = ref(new Date())
const currentBidder = ref(null)
const totalBidders = ref(0)
const isAuctionActive = ref(false)
const timeAdjustment = ref(0)
const manualPrice = ref(currentPrice.value)

// Additional state for pause functionality
const isPaused = ref(false)
const lastBidPrice = ref(null)
const remainingTimeOnPause = ref(null)

// Mock Bidding History
const biddingHistory = ref([
  {
    id: 1,
    timestamp: new Date(),
    bidderId: 'A123',
    amount: 3291000,
    status: 'accepted'
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 30000),
    bidderId: 'B456',
    amount: 3290500,
    status: 'accepted'
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 60000),
    bidderId: 'C789',
    amount: 3290000,
    status: 'accepted'
  }
])

// Computed Properties
const auctionStatus = computed(() => {
  if (!isAuctionActive.value) {
    return { text: 'ปิดการประมูล', color: 'error' }
  }
  return { text: 'กำลังประมูล', color: 'success' }
})

const isValidSetup = computed(() => {
  return (
    initialPrice.value > 0 &&
    initialTime.value > 0 &&
    minBidIncrement.value > 0
  )
})

// Utility Functions
const formatPrice = (price) => {
  return Number(price).toLocaleString('th-TH')
}

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

const formatDateTime = (date) => {
  return new Date(date).toLocaleString('th-TH', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// Auction Control Functions
const startAuction = () => {
  if (isPaused.value) {
    // Resume from pause
    isAuctionActive.value = true
    timeLeft.value = remainingTimeOnPause.value
    currentPrice.value = lastBidPrice.value
    isPaused.value = false
    startTimer()

    // Add resume entry to history
    biddingHistory.value.unshift({
      id: biddingHistory.value.length + 1,
      timestamp: new Date(),
      bidderId: 'SYSTEM',
      amount: currentPrice.value,
      status: 'resumed'
    })
  } else if (isValidSetup.value) {
    // Start new auction
    currentPrice.value = Number(initialPrice.value)
    startingPrice.value = Number(initialPrice.value)
    timeLeft.value = Number(initialTime.value) * 60
    isAuctionActive.value = true
    startTime.value = new Date()
    isPaused.value = false
    lastBidPrice.value = null
    remainingTimeOnPause.value = null
    startTimer()

    // Add initial bid to history
    biddingHistory.value.unshift({
      id: biddingHistory.value.length + 1,
      timestamp: new Date(),
      bidderId: 'SYSTEM',
      amount: currentPrice.value,
      status: 'start'
    })
  }
}

const pauseAuction = () => {
  isAuctionActive.value = false
  isPaused.value = true
  lastBidPrice.value = currentPrice.value
  remainingTimeOnPause.value = timeLeft.value
  pauseTimer()

  // Add pause entry to history
  biddingHistory.value.unshift({
    id: biddingHistory.value.length + 1,
    timestamp: new Date(),
    bidderId: 'SYSTEM',
    amount: currentPrice.value,
    status: 'paused'
  })
}

const stopAuction = () => {
  if (confirm('คุณแน่ใจหรือไม่ที่จะหยุดการประมูล? การประมูลจะถูกยกเลิก')) {
    isAuctionActive.value = false
    isPaused.value = false
    lastBidPrice.value = null
    remainingTimeOnPause.value = null
    stopTimer()

    // Add stop entry to history
    biddingHistory.value.unshift({
      id: biddingHistory.value.length + 1,
      timestamp: new Date(),
      bidderId: 'SYSTEM',
      amount: currentPrice.value,
      status: 'stopped'
    })
  }
}

const adjustTime = (seconds) => {
  timeLeft.value = Math.max(0, timeLeft.value + Number(seconds))
}

const extendTime = (seconds) => {
  timeLeft.value += seconds
}

const setPrice = (price) => {
  if (price && Number(price) > currentPrice.value) {
    currentPrice.value = Number(price)
    // Add to history
    biddingHistory.value.unshift({
      id: biddingHistory.value.length + 1,
      timestamp: new Date(),
      bidderId: 'ADMIN',
      amount: Number(price),
      status: 'accepted'
    })
  }
}

const quickIncrementPrice = (increment) => {
  const newPrice = currentPrice.value + Number(increment)
  setPrice(newPrice)
}

const clearHistory = () => {
  // Show confirmation dialog
  if (confirm('คุณแน่ใจหรือไม่ที่จะล้างประวัติการประมูล?')) {
    biddingHistory.value = []
  }
}

// Timer Logic
let timerInterval
const startTimer = () => {
  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      stopAuction()
    }
  }, 1000)
}

const stopTimer = () => {
  clearInterval(timerInterval)
}

const pauseTimer = () => {
  clearInterval(timerInterval)
}

// Cleanup
onUnmounted(() => {
  clearInterval(timerInterval)
})

// Initial setup
onMounted(() => {
  // Add some mock data periodically
  setInterval(() => {
    if (isAuctionActive.value && !isPaused.value) {
      const randomIncrement = quickBidIncrements.value[
        Math.floor(Math.random() * quickBidIncrements.value.length)
      ]
      const newPrice = currentPrice.value + randomIncrement

      const newBid = {
        id: biddingHistory.value.length + 1,
        timestamp: new Date(),
        bidderId: `USER${Math.floor(Math.random() * 999)}`,
        amount: newPrice,
        status: 'accepted'
      }
      
      currentPrice.value = newBid.amount
      currentBidder.value = newBid.bidderId
      biddingHistory.value.unshift(newBid)
      totalBidders.value = new Set(biddingHistory.value.map(bid => bid.bidderId)).size
    }
  }, 5000) // Add new bid every 5 seconds
})

// Add new state
const showCongrats = ref(false)

// Add new functions
const finishAuction = () => {
  if (confirm('คุณแน่ใจหรือไม่ที่จะจบการประมูล?')) {
    showCongrats.value = true
    isAuctionActive.value = false
    isPaused.value = false
    lastBidPrice.value = null
    remainingTimeOnPause.value = null
    stopTimer()
    
    // Add final bid to history
    biddingHistory.value.unshift({
      id: biddingHistory.value.length + 1,
      timestamp: new Date(),
      bidderId: currentBidder.value,
      amount: currentPrice.value,
      status: 'final'
    })
  }
}

const closeCongrats = () => {
  showCongrats.value = false
}
</script>

<style scoped>
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.gap-2 {
  gap: 8px;
}

.gap-4 {
  gap: 16px;
}

.congratulation-card {
  overflow: hidden;
  position: relative;
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
  color: white;
}

@keyframes firework {
  0% {
    transform: translate(var(--x), var(--initialY));
    width: var(--initialSize);
    opacity: 1;
  }
  50% {
    width: 0.5vmin;
    opacity: 1;
  }
  100% {
    width: var(--finalSize);
    opacity: 0;
  }
}

.firework,
.firework::before,
.firework::after {
  --initialSize: 0.5vmin;
  --finalSize: 45vmin;
  --particleSize: 0.2vmin;
  --color1: yellow;
  --color2: khaki;
  --color3: white;
  --color4: lime;
  --color5: gold;
  --color6: mediumseagreen;
  --y: -30vmin;
  --x: -50%;
  --initialY: 60vmin;
  content: "";
  animation: firework 2s infinite;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, var(--y));
  width: var(--initialSize);
  aspect-ratio: 1;
  background: 
    radial-gradient(circle, var(--color1) var(--particleSize), #0000 0) 50% 0%,
    radial-gradient(circle, var(--color2) var(--particleSize), #0000 0) 100% 50%,
    radial-gradient(circle, var(--color3) var(--particleSize), #0000 0) 50% 100%,
    radial-gradient(circle, var(--color4) var(--particleSize), #0000 0) 0% 50%,
    radial-gradient(circle, var(--color5) var(--particleSize), #0000 0) 80% 90%,
    radial-gradient(circle, var(--color6) var(--particleSize), #0000 0) 95% 90%;
  background-size: var(--initialSize) var(--initialSize);
  background-repeat: no-repeat;
}

.firework::before {
  --x: -50%;
  --y: -50%;
  --initialY: -50%;
  --rotation: 180deg;
  transform: translate(-50%, -50%) rotate(var(--rotation));
}

.firework::after {
  --x: -50%;
  --y: -50%;
  --initialY: -50%;
  --rotation: 45deg;
  transform: translate(-50%, -50%) rotate(var(--rotation));
}

.firework:nth-child(2) {
  --x: 30vmin;
}

.firework:nth-child(2),
.firework:nth-child(2)::before,
.firework:nth-child(2)::after {
  --color1: pink;
  --color2: violet;
  --color3: fuchsia;
  --color4: orchid;
  --color5: plum;
  --color6: lavender;  
  --finalSize: 40vmin;
  left: 30%;
  top: 60%;
  animation-delay: -0.25s;
}

.firework:nth-child(3) {
  --x: -30vmin;
  --y: -10vmin;
}

.firework:nth-child(3),
.firework:nth-child(3)::before,
.firework:nth-child(3)::after {
  --color1: cyan;
  --color2: lightcyan;
  --color3: lightblue;
  --color4: PaleTurquoise;
  --color5: SkyBlue;
  --color6: lavender;
  --finalSize: 35vmin;
  left: 70%;
  top: 40%;
  animation-delay: -0.4s;
}
</style>