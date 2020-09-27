<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Video Subtitles
        </q-toolbar-title>
       </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
         <q-scroll-area class="fit">
          <q-list>

            <template v-for="(menuItem, index) in menuLinks">
              <q-item :key="index" clickable :active="index == activeIndex" @click="setActive(index)">
                <q-item-section avatar>
                  <q-icon :name="menuItem.icon" />
                </q-item-section>
                <q-item-section>
                  {{ menuItem.label }}
                </q-item-section>
              </q-item>
              <q-separator :key="'sep' + index"  v-if="menuItem.separator" />
            </template>
          </q-list>
        </q-scroll-area>
    </q-drawer>
  </q-layout>
</template>

<script>

const menuList = [
  {
    icon: 'home',
    label: 'Início',
    separator: true
  },
  {
    icon: 'subtitles',
    label: 'Legendas'
  },
  {
    icon: 'account_box',
    label: 'Perfil',
    separator: true
  },
  {
    icon: 'error',
    label: 'Sobre'
  }
]

export default {
  name: 'MainLayout',

  data () {
    return {
      leftDrawerOpen: false,
      menuLinks: menuList,
      activeIndex: 0
    }
  },
  methods: {
    setActive (idx) {
      this.activeIndex = idx
    }
  }
}
</script>
