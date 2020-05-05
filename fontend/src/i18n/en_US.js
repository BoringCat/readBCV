const title = "readBCV —— Extract images from article at Bilibili"

const message = {
    warninfo: {
        l1: "Notes: Limited by Bilibili. Use",
        l1Strong: '"Download selected links by ......" is impossible',
        l2: "Or your downloader can create tasks without Referrer in headers",
        l3: "Avoid Bilibili return 421 when access too fast. Each access from server limit at 10 seconds",
        l4: "The data for each article will keep a week"
    },
    inputTitle: "Article's URL",
    loadImages: "Load images",
    commit: "Commit",
    speedLimit: "Waiting for response......",
    result: "Result",
    cover: "This is Cover: ",
    linkList: "linkList",
    inputErrorMsg: "Please input Bilibili Article's URL: https://www.bilibili.com/read/cv0000000 Or cv0000000",
    warning: 'Warning',
    loadImageIsOpen: 'Will load image now. Please care about network traffic limit',
    loadFailed: 'Failed',
    failToConnect: 'Unable to connect server',
    failUnknownError: 'Unknown Error',
    loadSuccess: 'Success',
    loadFromCache: 'Load list from server cache',
    loadFromWeb: 'Image list is loaded',
}

export default { title, message }