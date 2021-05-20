import gzip
from urllib.request import urlopen
from urllib.error import URLError
from urllib.request import Request
from io import BytesIO
import re
import os

headers: dict = {'Accept-Encoding': 'gzip, deflate'}
site_name: str = 'http://www.zhongyoo.com/name'
index_file = open(os.getcwd() + '/results/' + 'index' + '.txt', 'w')


def get_website(url: str, header: dict):
    try:
        response: Request = Request(url, headers=header)
        html_bytes: bytes = urlopen(response).read()
        buff: BytesIO = BytesIO(html_bytes)
        f = gzip.GzipFile(fileobj=buff)
        result: str = f.read().decode('gbk', errors='replace')
    except URLError as error:
        print('Downloading error: ' + error.reason)
        result = ''
    return result


def process_pages_nav(pages: list):
    name_pattern: str = 'alt=\'(.*)\''
    detail_page_pattern: str = '<div class="sp"><span class="pics pics2"> <a href=\'(.*)\' class=\'title\'>'
    total_page = len(pages)
    for index, page in enumerate(pages):
        progress: str = format(float(index)/float(total_page), '.2f')
        print('progress: ' + progress + ' ' + str(index) + ' of ' + str(total_page))
        current_link: str = site_name + '/' + page
        current_html: str = get_website(current_link, headers)
        name_results: list = re.findall(name_pattern, current_html)
        detail_links: list = re.findall(detail_page_pattern, current_html)
        if len(name_results) == len(detail_links):
            for index_y, detail_link in enumerate(detail_links):
                process_detail_page(detail_link, name_results[index_y])
    print('get files complete')


def process_detail_page(link: str, name: str):
    detail_html: str = get_website(link, headers)
    dr = re.compile(r'<[^>]+>', re.S)
    html_text = dr.sub('', detail_html)
    start_index: int = html_text.find('show_view_05();')
    end_index: int = html_text.find('show_view_04();')
    text_result: str = html_text[start_index+15:end_index]
    clear_text = text_result.strip().replace('\r', '').replace('\u3000', '').replace('\t', '').split('\n')
    final_text = ''
    for line_text in clear_text:
        if line_text != '':
            final_text += line_text + '\n'
    final_text = final_text[0:len(final_text)-1]
    print('generate: ' + os.getcwd() + '/results/' + name + '.txt')
    f = open(os.getcwd() + '/results/' + name + '.txt', 'w')
    f.write(final_text)
    index_file.write(name + ' ' + link + '\n')


def process():
    html: str = get_website(site_name, headers)
    pages_pattern: str = '<option value=\'(.*)\''
    pages_link: list = re.findall(pages_pattern, html)
    process_pages_nav(pages_link)
