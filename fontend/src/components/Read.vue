<template>
  <div>
    <a-form
      :form="form"
      :label-col="{ xs: {span:22, offset:1}, sm: {span: 5, offset:0} }"
      :wrapper-col="{ xs: {span:22, offset:1}, sm: { span: 16, offset:0 }}"
      @submit="handleSubmit"
      class="form"
    >
      <a-form-item
        :wrapper-col="{ xs: {span: 22, offset: 1}, sm: { span: 16, offset: 4 }}"
        class="warn"
      >
        <p>
          提示信息： 由于B站限制，无法直接实现右键菜单
          <strong>“使用......下载选定链接”</strong>
        </p>
        <p>
          <s>你的下载器可以不带Referrer就当我没说</s>
        </p>
        <p>为防止B站返回421，后端处理速度限制为10秒/个</p>
        <p>服务器缓存数据时间为7天</p>
      </a-form-item>
      <a-form-item label="B站专栏地址">
        <a-input v-decorator="decorators['URL']" />
      </a-form-item>
      <a-form-item
        :wrapper-col="{ xs: {offset: 16, span: 8}, sm: { span: 6, offset: 16 }}"
        style="text-align: center;"
      >
        <Checkbox :checked="loadimg" @change="OnLoadImgChange">加载图片</Checkbox>
      </a-form-item>
      <a-form-item :wrapper-col="{ xs: {span: 22, offset: 1}, sm: { span: 8, offset: 8 }}">
        <a-button type="primary" block html-type="submit">分析</a-button>
      </a-form-item>
    </a-form>
    <hr />
    <Row v-if="imglist.length" class="result">
      <Col
        :xs="{span:22, offset:1}"
        :sm="{span:20, offset:2}"
        :md="{span: 16, offset: 4}"
        :lg="{span: 14, offset: 5}"
        :xl="{span:12, offset: 6}"
        :xxl="{span: 8, offset: 8}"
      >
        <Spin :spinning="loading" :delay="500" tip="后端限流，等待后端返回中......">
          <h2>结果</h2>
          <a-collapse v-if="loadimg" v-model="activeKey">
            <a-collapse-panel v-for="img in imglist" :key="img" :header="getName(img)">
              <div style="text-align: center;">
                <a @click="downloadByBlob('https:'+img, getName(img))">
                  <img :src="'https:'+img" />
                </a>
              </div>
            </a-collapse-panel>
          </a-collapse>
          <div v-else v-for="img in imglist" :key="img">
            <hr />
            <a @click="downloadByBlob('https:'+img, getName(img))">{{ getName(img) }}</a>
          </div>
          <div>
            <h3>批量链接：</h3>
            <pre>{{ imglist.map(e=>'https:'+e).join('\n') }}</pre>
          </div>
        </Spin>
      </Col>
    </Row>
  </div>
</template>

<script>
import { handleError, handleSuccess, handleWarning, closeOne } from "@/utils";
import { Row, Col } from "ant-design-vue";
export default {
  components: {
    Row,
    Col
  },
  data() {
    return {
      formLayout: "horizontal",
      form: this.$form.createForm(this, { name: "readbcv" }),
      activeKey: [],
      loading: false,
      loadimg: false,
      imglist: [],
      lastwarn: {},
      decorators: {
        URL: [
          "BCVURL",
          {
            rules: [
              {
                required: true,
                validator(rule, value, callback) {
                  if (/^https?:\/\/www.bilibili.com\/read\/cv\d+$/.test(value)) {
                    callback();
                  } else if (/^cv\d+$/.test(value)) {
                    callback();
                  } else if (/^\d+$/.test(value)) {
                    callback();
                  } else {
                    callback("请输入B站的专栏地址，如: https://www.bilibili.com/read/cv5743037 或 cv5743037");
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
          let postval = {...values}
          this.loading = true;
          if (/^\d+$/.test(values['BCVURL'])) postval['BCVURL'] = `https://www.bilibili.com/read/cv${values['BCVURL']}`
          else if (/^cv\d+$/.test(values['BCVURL'])) postval['BCVURL'] = `https://www.bilibili.com/read/${values['BCVURL']}`
          this.initWebSocket(postval);
        }
      });
    },
    OnLoadImgChange(e) {
      this.loadimg = e.target.checked;
      if (this.lastwarn) {
        closeOne(this.lastwarn);
        this.lastwarn = {};
      }
      if (e.target.checked && this.imglist.length) {
        this.lastwarn = handleWarning(
          "注意",
          "已开启加载图片功能，请留意流量消耗",
          30
        );
      }
    },
    getName(url) {
      let l = url.split("/");
      return l[l.length - 1];
    },
    initWebSocket(values) {
      //初始化weosocket
      const https = /^http(s)?:$/.exec(window.location.protocol)[1] || "";
      const wsuri = `ws${https}://${window.location.host}/api/v1/readcv`;
      this.websock = new WebSocket(wsuri);
      this.websock.onopen = () => {
        this.websocketsend(JSON.stringify(values));
      };
      this.websock.onmessage = this.websocketonmessage;
      this.websock.onerror = this.websocketonerror;
      this.websock.onclose = this.websocketclose;
    },
    websocketonerror() {
      //连接建立失败重连
      handleError("获取失败", "无法连接到服务器", 30);
      this.loading = false;
    },
    websocketonmessage(e) {
      //数据接收
      const redata = JSON.parse(e.data);
      const fromcache = redata.fromcache || false;
      this.loading = false;
      this.imglist = redata.imgs;
      if (fromcache) handleSuccess("获取成功", "已加载缓存中的图片列表", 10);
      else handleSuccess("获取成功", "已加载图片列表", 10);
      if (this.loadimg)
        setTimeout(() => {
          if (this.lastwarn) closeOne(this.lastwarn);
          this.lastwarn = handleWarning(
            "注意",
            "已开启加载图片功能，请留意流量消耗",
            30
          );
        }, 100);
    },
    websocketsend(Data) {
      //数据发送
      this.websock.send(Data);
    },
    websocketclose(e) {
      //关闭
      if (e.code !== 1000 && e.code !== 1006)
        handleError("获取失败", e.reason || "未知错误", 30);
      this.loading = false;
    },
    downloadByBlob(url, name) {
      let image = new Image();
      image.setAttribute("crossOrigin", "anonymous");
      image.src = url;
      image.onload = () => {
        let canvas = document.createElement("canvas");
        canvas.width = image.width;
        canvas.height = image.height;
        let ctx = canvas.getContext("2d");
        ctx.drawImage(image, 0, 0, image.width, image.height);
        canvas.toBlob(blob => {
          let url = URL.createObjectURL(blob);
          this.download(url, name);
          // 用完释放URL对象
          URL.revokeObjectURL(url);
        });
      };
    },
    download(href, name = "pic") {
      let eleLink = document.createElement("a");
      eleLink.download = name;
      eleLink.href = href;
      eleLink.click();
      eleLink.remove();
    }
  }
};
</script>

<style>
.form {
  margin-top: 8px;
}
.result img {
  max-width: 100%;
  max-height: 40vh;
  /* height: auto; */
}
.warn {
  margin-bottom: 10px;
}
.warn p {
  margin-bottom: 0;
  margin-left: 4.6rem;
  line-height: initial;
}
.warn p:first-child {
  margin: 0;
}
</style>
