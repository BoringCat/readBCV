<template>
  <div id="app">
    <a-layout>
      <a-layout-header class="header logo">
        <span>{{ $t("title") }}</span>
      </a-layout-header>
      <a-layout class="layout">
        <div>
          <a-select class="select" v-model="$i18n.locale" @change="localeOnChange">
            <a-select-option v-for="({lang, name}, i) in langs" :key="`Lang${i}`" :value="lang">{{ name }}</a-select-option>
          </a-select>
        </div>
        <ReadBCV />
      </a-layout>
    </a-layout>
  </div>
</template>

<script>
import ReadBCV from "./components/Read.vue";

export default {
  name: "App",
  created () {
    document.title = this.$t("title")
    this.$i18n.locale = [document.cookie].map(e=>{
      let d = {}, ele = e.split(';')
      for ( let i in ele ) {
        let [name,value] = ele[i].split('=',2)
        d[name] = value
      }
      return d
      })[0]['locale'] || "zh_CN"
    // this.$i18n.locale = document.cookie.split(';').map(e=>{console.log(e)})
  },
  components: {
    ReadBCV,
  },
  data() {
    return { langs: [
      { lang: 'zh_CN', name: "简体中文" },
      { lang: 'en_US', name: "English (United States)" },
      { lang: 'zh_TW', name: "繁体中文" }
    ]};
  },
  methods: {
    localeOnChange(e) {
      document.title = this.$t("title")
      document.cookie = `locale=${e};expires=${new Date("9999-12-31 23:59:59").toGMTString()}`
    }
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
  text-align: center;
  padding: 16px;
  line-height: 2rem;
  font-size: 1.2rem;
  font-weight: bold;
  float: left;
  color: white;
}
.select {
  float: right;
  min-width: 190px;
  margin-top: 0.75rem;
  margin-right: 1rem;
  z-index: 999;
}
.layout {
  min-height: calc(100vh - 64px);
  background-color: white;
}
@media (prefers-color-scheme: dark) {
  .layout {
    background-color: #222;
  }
  .select .ant-select-selection, .ant-notification-notice {
    background-color: #111;
  }
  .ant-select-dropdown-menu-item, .ant-select-dropdown-menu-item-selected, .select.ant-select,
  .ant-notification-notice-message, .ant-progress-circle .ant-progress-text {
    color: #EEE;
  }
  .ant-notification-notice-close:hover {
    color: cornflowerblue;
  }
  .ant-notification, .ant-notification-notice-close {
    color: #CCC;
  }
  .ant-select-dropdown, .ant-select-dropdown-menu-item-selected {
    background-color: #2C2C2C;
  }
  .ant-select-dropdown-menu-item:hover:not(.ant-select-dropdown-menu-item-disabled),
  .ant-select-dropdown-menu-item-active:not(.ant-select-dropdown-menu-item-disabled) {
    background-color: #191919;
  }
  
}
</style>
