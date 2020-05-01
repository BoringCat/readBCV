<template>
  <a-ConfigProvider :locale="zh_CN">
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
  </a-ConfigProvider>
</template>

<script>
import ReadBCV from "./components/Read.vue";
import zh_CN from "ant-design-vue/lib/locale-provider/zh_CN";
export default {
  name: "App",
  components: {
    ReadBCV
  },
  data() {
    return {
      zh_CN
    };
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
  /* height: 31px; */
  /* background: rgba(255, 255, 255, 0.2);
  margin: 16px 28px 16px 0; */
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
