<template>
  <div id="app">
    <a-layout>
      <a-layout-header class="header logo">
        <span>{{ $t("title") }}</span>
        <a title="GitHub - BoringCat/readBCV" class="togithub" href="https://github.com/BoringCat/readBCV" target="_blank">
        <github :size="20" class="gitimg" />
        readBCV
        </a>
      </a-layout-header>
      <a-layout class="layout">
        <div>
          <I18nSwitch />
        </div>
        <ReadBCV />
      </a-layout>
    </a-layout>
  </div>
</template>

<script>
import ReadBCV from "@/components/Read.vue";
import I18nSwitch from "@/components/I18nSwitch.vue";
import github from "@/icons/github.vue";

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
    I18nSwitch,
    github
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
  text-align: center;
  padding: 16px;
  line-height: 2rem;
  font-size: 1.2rem;
  font-weight: bold;
  float: left;
  height: auto;
  color: white;
}
.layout {
  min-height: calc(100vh - 64px);
  background-color: white;
}
.togithub {
  font-weight: initial;
  font-size: 0.9rem;
  color: white;
  float: right;
}
@media (min-width: 576px) {
  .togithub {
    margin-left: -10rem;
  }
}
.togithub:hover {
  color: white;
}

.gitimg {
  margin-bottom: -0.35rem;
}

@media (prefers-color-scheme: dark) {
  .layout {
    background-color: #222;
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
}
</style>
