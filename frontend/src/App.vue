<template>
  <div>
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      @select="handleSelect"
      class="nav-menu"
    >
      <el-menu-item index="rewrite">文本降重</el-menu-item>
      <el-menu-item index="humanize">降低AI率</el-menu-item>
    </el-menu>

    <text-processor 
      :mode="activeIndex"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TextProcessor from './components/TextProcessor.vue'

const activeIndex = ref('rewrite')

const handleSelect = (key) => {
  activeIndex.value = key
}
</script>

<style>
.nav-menu {
  margin-bottom: 20px;
}
</style>
