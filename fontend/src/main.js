import Vue from 'vue'
import App from './App.vue'
import VueI18n from 'vue-i18n'
import { Button, Form, Input, Layout, Collapse, Spin, Progress, Checkbox, Select } from 'ant-design-vue';
import messages from '@/i18n'

Vue.component(Button.name, Button)
Vue.component("Spin", Spin)
Vue.component("Progress", Progress)
Vue.component("Checkbox", Checkbox)
Vue.use(Form)
Vue.use(Layout)
Vue.use(Input)
Vue.use(Collapse)
Vue.use(Select)
Vue.use(VueI18n)

Vue.config.productionTip = false

const i18n = new VueI18n({
  locale: 'en_US', // 设置地区
  messages, // 设置地区信息
})

new Vue({
  i18n,
  render: h => h(App),
}).$mount('#app')
