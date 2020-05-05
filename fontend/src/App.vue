<template>
  <div id="app">
    <a-layout>
      <a-layout-header class="header logo">
        readBCV —— 提取B站专栏图片
      </a-layout-header>
      <a-layout class="layout">
        <ReadBCV />
      </a-layout>
    </a-layout>
  </div>
</template>

<script>
import ReadBCV from "./components/Read.vue";
export default {
  name: "App",
  components: {
    ReadBCV
  },
  data() {
    return { };
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
.logo {
  padding: 16px;
  line-height: 2rem;
  text-align: center;
  font-size: 1.2rem;
  font-weight: bold;
  float: left;
  color: white;
}
.layout {
  min-height: calc(100vh - 64px);
  background-color: white;
}
</style>
