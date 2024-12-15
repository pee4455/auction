<template>
  <v-list class="sidebar-list pa-4" nav>
    <div class="text-center mb-6">
      <v-avatar size="80" color="primary" class="mb-2">
        <span class="text-h4 text-white">A</span>
      </v-avatar>
      <h2 class="text-white text-h6 font-weight-medium">Admin Menu</h2>
    </div>

    <v-list-item
      v-for="(item, index) in menuItems"
      :key="index"
      :to="item.path"
      :value="item.path"
      class="mb-2 sidebar-item"
      rounded="lg"
      color="white"
    >
      <template v-slot:prepend>
        <v-icon :icon="item.icon" color="white"></v-icon>
      </template>

      <v-list-item-title class="text-white">{{ item.title }}</v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: 'SideBar',
  data() {
    return {
      menuItems: [
        { title: 'Dashboard', path: '/', icon: 'mdi-view-dashboard' },
        { title: 'Manage Auctions', path: '/auctions', icon: 'mdi-gavel' },
        { title: 'Manage Users', path: '/users', icon: 'mdi-account-group' }
      ]
    }
  }
}
</script>

<style scoped>
.sidebar-list {
  background-color: #235d3b;
  height: 100%;
}

.sidebar-item {
  transition: all 0.3s ease;
  margin-bottom: 8px;
}

.sidebar-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
  transform: translateX(4px);
}

.v-list-item--active {
  background-color: rgba(255, 255, 255, 0.15) !important;
}

.v-list-item-title {
  font-size: 0.95rem;
  font-weight: 500;
}

/* Custom scrollbar for sidebar */
::-webkit-scrollbar {
  width: 5px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
  