import { notification } from 'ant-design-vue'

const _genAxiosError = (h, error) => {
  if (error.response && typeof error.response.data === 'object') {
    return h('div', {}, [
      h(
        'span', {}, [
        h('strong', {}, '错误信息: '),
        h(
          'span',
          { props: { style: { wordBreak: 'break-word' } } },
          error.response.data.msg || error.response.data.errmsg
        )
      ]),
      h('br', {}, null),
      h('span', {}, [
        h('strong', {}, '详细信息: '),
        h(
          'pre',
          { props: { style: { wordBreak: 'break-word', margin: 0 } } },
          JSON.stringify(error.response.data.detail, null, 2)
        )
      ])
    ])
  } else {
    return h(
      'span', {}, [
      h('strong', {}, '未知错误：'),
      h('span', { props: { style: { wordBreak: 'break-word' } } }, String(error))
    ]
    )
  }
}

const _showNotifi = (status, title, msg, duration) => {
  const key = (new Date()).getTime()
  let interval = duration * 25 / 3
  if (interval < 50) interval = 50
  let b = (1000 / interval)
  let a = duration * b
  let strokeColor = 'green'
  switch (status) {
    case 'success':
      strokeColor = 'green'
      break;
    case 'error':
      strokeColor = 'red'
      break;
    case 'info':
      strokeColor = 'blue'
      break;
    case 'warn':
    case 'warning':
      strokeColor = 'orange'
      break;
  }
  let time = setInterval(() => {
    a--
    notification[status]({
      key,
      icon: h => h('Progress',
        {
          props: {
            type: 'circle',
            percent: a / b / duration * 100,
            width: 36,
            strokeWidth: 10,
            strokeColor,
            format: percent => ((percent / 100 * duration).toFixed(0))
          }
        },
        null
      ),
      message: title,
      description: msg,
      duration: 0,
      onClose() {
        a = 0
        clearInterval(time)
      }
    })
    if (a <= 0) {
      clearInterval(time)
      notification.close(key)
    }
  }, interval)
  notification[status]({
    key,
    icon: h => h('Progress',
      {
        props: {
          type: 'circle',
          percent: 99.99,
          width: 36,
          strokeWidth: 10,
          strokeColor,
          format: percent => ((percent / 100 * duration).toFixed(0))
        }
      },
      null
    ),
    message: title,
    description: msg,
    duration: 0,
    onClose() {
      a = 0
      clearInterval(time)
    }
  })
  return {key, time}
}

const closeOne = ({key, time}) => {
  clearInterval(time)
  notification.close(key)
}

const handleAxiosError = (error, title, duration = 30) => {
  if (Axios.isCancel(error)) { return }
  return _showNotifi('error', title, h => _genAxiosError(h, error), duration)
}
const handleError = (title, msg, duration = 30) => {
  return _showNotifi('error', title, msg, duration)
}
const handleSuccess = (title, msg, duration = 3) => {
  return _showNotifi('success', title, msg, duration)
}
const handleInfo = (title, msg, duration = 3) => {
  return _showNotifi('info', title, msg, duration)
}
const handleWarning = (title, msg, duration = 3) => {
  return _showNotifi('warning', title, msg, duration)
}

const getProtocol = url => {
  try {
    return /^(https?):\/\//.exec(url)[1]
  } catch (error) {
    
  }
}

const getName = url => {
  let l = url.split("/");
  return l[l.length - 1];
}

const MetaLinkObj = {
  header: '<?xml version="1.0" encoding="utf-8"?>\n<metalink version="3.0" xmlns="http://www.metalinker.org/" type="dynamic" pubdate="Fri, 22 May 2020 12:04:55 GMT" generator="readbcv" xmlns:mm0="https://readbcv.boringcat.top/">\n <files>\n',
  footer: ' </files>\n</metalink>',
  format: '  <file name="{folder}/{name}">\n   <mm0:timestamp>{now}</mm0:timestamp>\n   <resources maxconnections="1">\n    <url protocol="{protocol}" type="{protocol}" preference="100">{url}</url>\n   </resources>\n  </file>\n',
  formater (folder, url) {
    return this.format.replace(/{folder}/g, folder)
                      .replace(/{name}/g,getName(url))
                      .replace(/{protocol}/g,getProtocol(url))
                      .replace(/{now}/g,parseInt(new Date().getTime() / 1000))
                      .replace(/{url}/g,url)
  }
}

const genMetalink = (urls, folder) => {
  let ms = MetaLinkObj.header
  urls.forEach(url => {
    ms = ms + MetaLinkObj.formater(folder, url)
  })
  return ms + MetaLinkObj.footer
}

export { handleAxiosError, handleError, handleSuccess, handleInfo ,handleWarning, closeOne, genMetalink, getName }
