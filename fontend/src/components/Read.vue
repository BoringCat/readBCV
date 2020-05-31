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
        <p><strong>{{ $t("message.warninfo.title") }}</strong>{{ $t("message.warninfo.l1") }}<strong>{{ $t("message.warninfo.l1Strong") }}</strong></p>
        <p><s>{{ $t("message.warninfo.l2") }}</s></p>
        <p>{{ $t("message.warninfo.l3") }}</p>
        <p>{{ $t("message.warninfo.l4") }}</p>
        <p><a href="https://github.com/BoringCat/readBCV/blob/master/MetaFileHelp.md" target="_blank">MetaFile Help</a></p>
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
    <Row class="result">
      <Col
        :xs="{span:22, offset:1}"
        :sm="{span:20, offset:2}"
        :md="{span: 16, offset: 4}"
        :lg="{span: 14, offset: 5}"
        :xl="{span:12, offset: 6}"
        :xxl="{span: 8, offset: 8}"
      >
        <Spin :spinning="loading" :delay="500" :tip="$t('message.speedLimit')">
          <h2>{{ $t('message.result') }}
            <a-button v-if="loadimg && this.activeKey.length !== 0" type="dashed" class="showall" @click="activeKey = []">{{ $t('message.collapseAll') }}</a-button>
            <a-button v-if="loadimg && this.activeKey.length !== this.allkeys.length" type="dashed" class="showall" @click="activeKey = [...allkeys]">{{ $t('message.showAll') }}</a-button>
          </h2>
          <a-collapse v-if="loadimg && this.contents.length !== 0" v-model="activeKey">
            <a-collapse-panel v-for="{img, isheader, figcaption, title} in contents" :key="img" :header="(isheader?$t('message.cover'):'') + (title?title + ': ': '') + getName(img)">
              <div style="text-align: center;">
                <a class="showimg" @click="downloadUseBlob(img, getName(img))">
                  <img :src="img" />
                </a>
                <div class="figcaption">{{ figcaption }}</div>
              </div>
            </a-collapse-panel>
          </a-collapse>
          <div v-else v-for="{img, isheader, figcaption, title} in contents" :key="img">
            <hr />
            <a @click="downloadUseBlob(img, getName(img))">{{ (isheader?$t('message.cover'):'') + (title?title + ': ': '') + getName(img) }}</a>
            <pre class="figcaption">{{ figcaption }}</pre>
          </div>
          <div v-if="contents.length">
            <h3>
              {{ $t('message.linkList') }}
              <a-button type="primary" class="metalink" @click="TryMeta">{{ $t('message.metalink_dl') }}</a-button>
            </h3>
            <pre>{{ contents.map(e=>e.img).join('\n') }}</pre>
          </div>
        </Spin>
      </Col>
    </Row>
  </div>
</template>

<script>
import { handleError, handleSuccess, handleWarning, closeOne, genMetalink, getName } from "@/utils";
import { Row, Col } from "ant-design-vue";
import { switchLocale } from '@/i18n';
export default {
  components: {
    Row,
    Col
  },
  data() {
    return {
      getName,
      formLayout: "horizontal",
      form: this.$form.createForm(this, { name: "readbcv" }),
      activeKey: [],
      loading: false,
      loadimg: false,
      showall: false,
      bid: '',
      contents: [],
      allkeys: [],
      lastwarn: {},
      decorators: {
        URL: [
          "BURL",
          {
            rules: [
              {
                required: true,
                validator: (rule, value, callback) => {
                  if (/^https?:\/\/www.bilibili.com\/read\/cv\d+$/.test(value)) {
                    callback();
                  } else if (/^cv\d+$/.test(value)) {
                    callback();
                  } else if (/^https?:\/\/www.bilibili.com\/video\/[bB][Vv]\w+$/.test(value)) {
                    callback();
                  } else if (/^[bB][Vv]\w+$/.test(value)) {
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
    TryMeta() {
      let MetaFile = genMetalink(this.contents.map(e=>e.img),this.bid)
      let blob = new Blob([MetaFile], {type: 'application/octet-stream'});
      let durl = URL.createObjectURL(blob)
      this.downloadFile(durl, `${this.bid}.metalink`)
      URL.revokeObjectURL(durl);
    },
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          let postval = {...values, locale: this.$i18n.locale}
          this.bid = getName(values['BURL'])
          this.loading = true;
          if (/^cv\d+$/.test(values['BURL'])) postval['BURL'] = `https://www.bilibili.com/read/${values['BURL']}`
          else if (/^[bB][Vv]\w+$/.test(values['BURL'])) postval['BURL'] = `https://www.bilibili.com/video/cv${values['BURL']}`
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
      const status = redata.status || false;
      if (! status) {
        handleError(this.$t('message.loadFailed'), redata.errmsg || this.$t('message.failUnknownError'), 30);
        return
      }
      const fromcache = redata.fromcache || false;
      let have_header = false
      let header = redata.imgs.header;
      this.loading = false;
      this.contents = redata.imgs.contents.map(e=>{
        let imgurl, figcaption, title
        if (typeof(e) === 'object'){
          imgurl = e.url
          figcaption = e.figcaption
          title = e.title
        } else {
          imgurl = e
        }
        let isheader = this.getName(imgurl) === this.getName(header)
        if (! have_header) if (isheader) have_header = true
        return {img: imgurl, isheader, figcaption, title}
      });
      if (! have_header) this.contents.unshift({img: header, isheader: true})
      if (fromcache) handleSuccess(
          this.$t('message.loadSuccess'),
          this.$t('message.loadFromCache'),
          10
        );
      else handleSuccess(this.$t('message.loadSuccess'), this.$t('message.loadFromWeb'), 10);
      this.activeKey = [];
      this.allkeys = this.contents.map(e=>(e.img))
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
    downloadUseBlob(url, name) {
      fetch(url).then(res=>{
        res.blob().then(blob=>{
          let durl = URL.createObjectURL(blob)
          this.downloadFile(durl, name)
          URL.revokeObjectURL(durl);
        })
      })
    },
    downloadFile(href, name) {
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
.result .ant-spin-container {
  min-height: 8rem;
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
  margin-left: 1rem;
  line-height: initial;
}
.warn p:first-child {
  margin: 0;
}

.figcaption {
  color: #111;
  white-space: pre-wrap;
  overflow: visible;
  text-align: center;
}

.showall {
  float: right;
  margin: 0 3px;
}

h3 {
  margin: 0.25em 0;
  min-height: 32px;
  line-height: 32px;
}

button.metalink {
  float: right;
}

.showall, .showall:hover, .showall:focus {
  background-color: transparent;
}

@media (prefers-color-scheme: dark) {
  .warn, .form .ant-form-item-required, .form .ant-checkbox-wrapper, .form .ant-input, .result h2, .result h3,
  .result .ant-collapse > .ant-collapse-item > .ant-collapse-header, .figcaption, .showall {
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
  .ant-spin-nested-loading > div > .ant-spin .ant-spin-text {
    text-shadow: 0 1px 2px #111;
  }
}
</style>
