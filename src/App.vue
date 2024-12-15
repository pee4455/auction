<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      temporary
      class="custom-drawer"
    >
      <Sidebar />
    </v-navigation-drawer>

    <v-app-bar
      app
      flat
      class="px-4"
      height="80"
      color="background"
    >
      <v-app-bar-nav-icon
        @click="drawer = !drawer"
        class="hidden-md-and-up"
      ></v-app-bar-nav-icon>
      
      <v-spacer></v-spacer>
      
      <div class="hidden-sm-and-down">
        <Navbar />
      </div>
    </v-app-bar>

    <v-main>
      <v-container fluid class="pa-0">
        <transition
          name="page"
          mode="out-in"
        >
          <router-view></router-view>
        </transition>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Sidebar
  }
}
</script>