<template>
  <div>
    <a-form
      :form="form"
      :label-col="{ span: 5 }"
      :wrapper-col="{ span: 16 }"
      @submit="handleSubmit"
      class="form"
    >
      <a-form-item label="B站专栏地址">
        <a-input v-decorator="decorators['URL']" />
      </a-form-item>
      <a-form-item :wrapper-col="{ span: 8, offset: 8 }">
        <a-button type="primary" block html-type="submit">分析</a-button>
      </a-form-item>
    </a-form>
    <hr />
    <a-layout class="result">
      <Spin :spinning="loading" :delay="500" tip="后端限流，等待后端返回中......">
      <h1>结果</h1>
      <a-collapse v-model="activeKey"></a-collapse>
      </Spin>
    </a-layout>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formLayout: "horizontal",
      form: this.$form.createForm(this, { name: "readbcv" }),
      activeKey: [],
      loading: false,
      decorators: {
        URL: [
          "BCVURL",
          {
            rules: [
              {
                required: true,
                validator(rule, value, callback) {
                  if (
                    /^https?:\/\/www.bilibili.com\/read\/cv\d+$/.test(value)
                  ) {
                    callback();
                  } else {
                    callback("请输入B站的专栏地址");
                  }
                }
              }
            ]
          }
        ]
      }
    };
  },
  methods: {
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
          this.loading = true
          setTimeout(()=>this.loading = false,5000)
        }
      });
    },
    handleSelectChange(value) {
      console.log(value);
      this.form.setFieldsValue({
        note: `Hi, ${value === "male" ? "man" : "lady"}!`
      });
    }
  }
};
</script>

<style>
.form {
  margin-top: 32px;
}
.result {
  background-color: white;
  margin: 16px 64px 0;
}
</style>
