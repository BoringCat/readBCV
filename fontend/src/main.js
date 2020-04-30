import Vue from 'vue'
import App from './App.vue'
import { Button, ConfigProvider, Form, Input, Layout, Collapse, Spin } from 'ant-design-vue';

Vue.component(Button.name, Button)
Vue.component("a-ConfigProvider", ConfigProvider)
Vue.component("Spin", Spin)
Vue.use(Form)
Vue.use(Layout)
Vue.use(Input)
Vue.use(Collapse)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
