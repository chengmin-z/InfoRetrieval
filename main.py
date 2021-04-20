import gzip
from urllib.request import urlopen
from urllib.error import URLError
from urllib.request import Request
from io import BytesIO

# 经过了多次尝试后 已经登陆用户访问信息门户 只需要以下header
# Cookie使用时需要更新

bupt_headers = {
    # 'Host': 'my.bupt.edu.cn',
    # 'Connection': 'keep-alive',
    # 'Cache-Control': 'max-age=0',
    # 'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': 'qqmail_alias=zcm@bupt.edu.cn; JSESSIONID=10503EC3659706F6EE575426FE63B5E9'
}


# 访问特定网站使用GET请求 并使用headers

def get_website(url, headers):
    try:
        response = Request(url, headers=headers)
        html = urlopen(response).read()
        buff = BytesIO(html)
        f = gzip.GzipFile(fileobj=buff)
        result = f.read().decode('utf-8')
    except URLError as error:
        print('Downloading error: ' + error.reason)
        result = None
    return result


if __name__ == '__main__':
    buptUrl = 'http://my.bupt.edu.cn/xntz_content.jsp?urltype=news.NewsContentUrl&wbtreeid=1642&wbnewsid=88729'
    print(get_website(buptUrl, bupt_headers))
