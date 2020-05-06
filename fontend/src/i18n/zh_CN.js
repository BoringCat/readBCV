const title = "readBCV —— 提取B站专栏图片"

const message = {
    warninfo: {
        title: "提示信息： ",
        l1: "由于B站限制，无法直接实现右键菜单",
        l1Strong: "“使用......下载选定链接”",
        l2: "你的下载器可以不带Referrer就当我没说",
        l3: "为防止B站返回421，后端处理速度限制为10秒/个",
        l4: "服务器缓存数据时间为7天"
    },
    inputTitle: "B站专栏地址",
    loadImages: "加载图片",
    commit: "分析",
    speedLimit: "后端限流，等待后端返回中......",
    result: "结果",
    cover: "封面: ",
    linkList: "批量链接：",
    inputErrorMsg: '请输入B站的专栏地址，如: https://www.bilibili.com/read/cv0000000 或 cv0000000',
    warning: '注意',
    loadImageIsOpen: '已开启加载图片功能，请留意流量消耗',
    loadFailed: '获取失败',
    failToConnect: '无法连接到服务器',
    failUnknownError: '未知错误',
    loadSuccess: '获取成功',
    loadFromCache: '已加载缓存中的图片列表',
    loadFromWeb: '已加载图片列表',
}

export default { title, message }