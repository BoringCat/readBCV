const title = "readBCV —— 提取B站專欄圖片"

const message = {
    warninfo: {
        title: "提示信息： ",
        l1: "由於B站限製，無法直接實現右鍵菜單",
        l1Strong: "“使用......下載選定鏈接”",
        l2: "你的下載器可以不帶Referrer就當我冇說",
        l3: "為防止B站返回421，後端處理速度限製為10秒/個",
        l4: "服務器緩存數據時間為7天"
    },
    inputTitle: "B站專欄地址",
    loadImages: "加載圖片",
    commit: "分析",
    speedLimit: "後端限流，等待後端返回中......",
    result: "結果",
    cover: "封麵: ",
    linkList: "批量鏈接：",
    inputErrorMsg: '請輸入B站的專欄地址，如: https://www.bilibili.com/read/cv0000000 或 cv0000000',
    warning: '註意',
    loadImageIsOpen: '已開啓加載圖片功能，請留意流量消耗',
    loadFailed: '獲取失敗',
    failToConnect: '無法連接到服務器',
    failUnknownError: '未知錯誤',
    loadSuccess: '獲取成功',
    loadFromCache: '已加載緩存中的圖片列錶',
    loadFromWeb: '已加載圖片列錶',
}

export default { title, message }