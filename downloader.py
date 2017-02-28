import urllib.request


class DownLoader:
    # 根据参数下载页面，并且返回下载的页面的bytes
    @staticmethod
    def download_html(opener, link, file_name, params):
        # 判断链接是否有参数
        if params is not None:
            link = link.format(params)
        req = urllib.request.Request(link)
        resp = opener.open(req)
        data = resp.read()
        # 如果文件名参数不为空则输出文件
        if file_name is not None:
            s = 'outputs\\'
            file_name = s + file_name  # 输出到outputs文件夹下
            print(file_name)
            f = open(file_name, 'wb')
            f.write(data)
            f.close()
        return data
