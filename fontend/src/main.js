import Vue from 'vue'
import App from './App.vue'
import { Button, Form, Input, Layout, Collapse, Spin, Progress, Checkbox } from 'ant-design-vue';

Vue.component(Button.name, Button)
Vue.component("Spin", Spin)
Vue.component("Progress", Progress)
Vue.component("Checkbox", Checkbox)
Vue.use(Form)
Vue.use(Layout)
Vue.use(Input)
Vue.use(Collapse)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
