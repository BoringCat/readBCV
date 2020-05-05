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
        <p>{{ $t("message.warninfo.l1") }}<strong>{{ $t("message.warninfo.l1Strong") }}</strong></p>
        <p><s>{{ $t("message.warninfo.l2") }}</s></p>
        <p>{{ $t("message.warninfo.l3") }}</p>
        <p>{{ $t("message.warninfo.l4") }}</p>
      </a-form-item>
      <a-form-item :label="$t('message.inputTitle')">
        <a-input v-decorator="decorators['URL']" />
      </a-form-item>
      <a-form-item
        :wrapper-col="{ xs: {offset: 16, span: 8}, sm: { span: 6, offset: 16 }}"
        style="text-align: center;"
      >
        <Checkbox :checked="loadimg" @change="OnLoadImgChange">{{ $t('message.loadImages') }}</Checkbox>
      </a-form-item>
      <a-form-item :wrapper-col="{ xs: {span: 22, offset: 1}, sm: { span: 8, offset: 8 }}">
        <a-button type="primary" block html-type="submit">{{ $t('message.commit') }}</a-button>
      </a-form-item>
    </a-form>
    <hr />
    <Row v-if="contents.length" class="result">
      <Col
        :xs="{span:22, offset:1}"
        :sm="{span:20, offset:2}"
        :md="{span: 16, offset: 4}"
        :lg="{span: 14, offset: 5}"
        :xl="{span:12, offset: 6}"
        :xxl="{span: 8, offset: 8}"
      >
        <Spin :spinning="loading" :delay="500" :tip="$t('message.speedLimit')">
          <h2>{{ $t('message.result') }}</h2>
          <a-collapse v-if="loadimg" v-model="activeKey">
            <a-collapse-panel v-for="{img, isheader} in contents" :key="img" :header="(isheader?$t('message.cover'):'') + getName(img)">
              <div style="text-align: center;">
                <a @click="downloadByBlob(img, getName(img))">
                  <img :src="img" />
                </a>
              </div>
            </a-collapse-panel>
          </a-collapse>
          <div v-else v-for="{img, isheader} in contents" :key="img">
            <hr />
            <a @click="downloadByBlob(img, getName(img))">{{ (isheader?$t('message.cover'):'') + getName(img) }}</a>
          </div>
          <div>
            <h3>{{ $t('message.linkList') }}</h3>
            <pre>{{ contents.map(e=>e.img).join('\n') }}</pre>
          </div>
        </Spin>
      </Col>
    </Row>
  </div>
</template>

<script>
import { handleError, handleSuccess, handleWarning, closeOne } from "@/utils";
import { Row, Col } from "ant-design-vue";
import { switchLocale } from '@/i18n';
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
      contents: [],
      lastwarn: {},
      decorators: {
        URL: [
          "BCVURL",
          {
            rules: [
              {
                required: true,
                validator: (rule, value, callback) => {
                  if (/^https?:\/\/www.bilibili.com\/read\/cv\d+$/.test(value)) {
                    callback();
                  } else if (/^cv\d+$/.test(value)) {
                    callback();
                  } else if (/^\d+$/.test(value)) {
                    callback();
                  } else {
                    callback(this.$t('message.inputErrorMsg'));
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
      if (e.target.checked && this.contents.length) {
        this.lastwarn = handleWarning(
          this.$t('message.warning'),
          this.$t('message.loadImageIsOpen'),
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
      //连接建立失败
      handleError(
        this.$t('message.loadFailed'),
        this.$t('message.failToConnect'),
        30
      );
      this.loading = false;
    },
    websocketonmessage(e) {
      //数据接收
      const redata = JSON.parse(e.data);
      const fromcache = redata.fromcache || false;
      let have_header = false
      let header = redata.imgs.header;
      this.loading = false;
      this.contents = redata.imgs.contents.map(e=>{
        let isheader = this.getName(e) === this.getName(header)
        if (! have_header) if (isheader) have_header = true
        return {img: 'https:'+e, isheader}
      });
      if (! have_header) this.contents.unshift({img: header, isheader: true})
      if (fromcache) handleSuccess(
          this.$t('message.loadSuccess'),
          this.$t('message.loadFromCache'),
          10
        );
      else handleSuccess(this.$t('message.loadSuccess'), this.$t('message.loadFromWeb'), 10);
      if (this.loadimg)
        setTimeout(() => {
          if (this.lastwarn) closeOne(this.lastwarn);
          this.lastwarn = handleWarning(
          this.$t('message.warning'),
          this.$t('message.loadImageIsOpen'),
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
        handleError(this.$t('message.loadFailed'), e.reason || this.$t('message.failUnknownError'), 30);
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
@media (prefers-color-scheme: dark) {
  .warn, .form .ant-form-item-required, .form .ant-checkbox-wrapper, .form .ant-input, .result h2, .result h3,
  .result .ant-collapse > .ant-collapse-item > .ant-collapse-header {
    color: #EEE;
  }
  .result pre {
    color: #BBB;
  }
  .form .ant-input, .form .ant-input:hover, .result .ant-collapse {
    background-color: #111;
  }
  .result .ant-collapse-content {
    background-color: #2c2c2c;
  }
}
</style>
