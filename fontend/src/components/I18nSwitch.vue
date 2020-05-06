<template>
  <Row>
    <Col :xs="{span:22, offset:1}" :sm="{ span: 16, offset:5 }">
    <a-select class="select" v-model="$i18n.locale" @change="localeOnChange">
      <a-select-option v-for="({lang, name}, i) in langs" :key="`Lang${i}`" :value="lang">{{ name }}</a-select-option>
    </a-select>
    </Col>
  </Row>
</template>

<script>
import { Row, Col } from "ant-design-vue";
export default {
  components: {
    Row,
    Col
  },
  data() {
    return {
      langs: [
        { lang: 'zh_CN', name: "简体中文" },
        { lang: 'en_US', name: "English (United States)" },
        { lang: 'zh_TW', name: "繁体中文" }
      ]
    };
  },
  methods: {
    localeOnChange(e) {
      document.title = this.$t("title")
      document.cookie = `locale=${e};expires=${new Date("9999-12-31 23:59:59").toGMTString()}`
    }
  }
}
</script>

<style>
.select {
  float: right;
  min-width: 190px;
  margin-top: 0.75rem;
}
@media (prefers-color-scheme: dark) {
  .select .ant-select-selection, .ant-notification-notice {
    background-color: #111;
  }
  .select.ant-select {
    color: #EEE;
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