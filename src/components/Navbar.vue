<template>
  <nav>
    <v-list class="d-flex pa-0" nav>
      <v-list-item
        v-for="(item, index) in menuItems"
        :key="index"
        :to="item.path"
        class="menu-item"
        color="primary"
      >
        <template v-slot:default="{ isActive }">
          <div class="d-flex flex-column align-center">
            <v-icon :color="isActive ? 'primary' : 'grey'" class="mb-1">
              {{ item.icon }}
            </v-icon>
            <span :class="{ 'text-primary': isActive, 'text-grey': !isActive }">
              {{ item.title }}
            </span>
          </div>
        </template>
      </v-list-item>
    </v-list>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      menuItems: [
        { title: 'Dashboard', path: '/', icon: 'mdi-view-dashboard' },
        { title: 'Auctions', path: '/auctions', icon: 'mdi-gavel' },
        { title: 'Users', path: '/users', icon: 'mdi-account-group' },
        { title: 'สมัครสมาชิก', path: '/register', icon: 'mdi-account-plus' }
      ]
    }
  }
}
</script>

<style scoped>
.menu-item {
  min-width: 100px;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 8px;
}

.menu-item:hover {
  background-color: rgba(35, 93, 59, 0.1);
  transform: translateY(-2px);
}

.v-list-item--active {
  background-color: rgba(35, 93, 59, 0.15) !important;
}

span {
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.3s ease;
}
</style>