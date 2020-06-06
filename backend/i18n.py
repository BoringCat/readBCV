class I18nClass():
    class zh_CN():
        cover = '封面'
        video_cover = '视频封面'
        queue_full = '队列已满'
        page_not_found = '找不到该页面'
        unknown_error = '未知错误'
        server_limit = '后端请求限制'
        illegal_request = '非法请求'
        remote_is_return = 'B站服务器返回'

    class en_US():
        cover = 'Cover'
        video_cover = 'Video cover'
        queue_full = 'Queue is full'
        unknown_error = 'Unknown error'
        page_not_found = 'Page Not Found'
        server_limit = 'Limited by server'
        illegal_request = 'Illegal request'
        remote_is_return = 'Return code from bilibili server is'

    class zh_TW():
        cover = '封麵'
        video_cover = '視訊封麵'
        queue_full = '隊列已滿'
        page_not_found = '找不到該頁麵'
        unknown_error = '未知錯誤'
        server_limit = '後端請求限製'
        illegal_request = '非法請求'
        remote_is_return = 'B站服務器返回'

    @classmethod
    def t(self, msg, locale):
        c = getattr(self, locale, None)
        if not c:
            return msg
        return getattr(c, msg, msg)

t = I18nClass.t