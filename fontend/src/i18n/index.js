import zh_CN from './zh_CN'
import en_US from './en_US'
import zh_TW from './zh_TW'

const messages = {
  zh_CN,
  en_US,
  zh_TW
}

function switchLocale(that, aim) {
  return that.$i18n.setLocaleMessage(aim, messages[aim])
}

export default messages
export { switchLocale }