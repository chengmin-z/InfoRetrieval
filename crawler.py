import gzip
from typing import TextIO
from urllib.request import urlopen
from urllib.error import URLError
from urllib.request import Request
from io import BytesIO
import re
import os


class Crawler:

    def __init__(self):
        self.__headers: dict = {'Accept-Encoding': 'gzip, deflate'}
        self.__site_name: str = 'http://www.zhongyoo.com'
        self.__index_file: TextIO = open(os.getcwd() + '/results/' + 'index.txt', 'w')

    def __get_website(self, url: str):
        try:
            response: Request = Request(url, headers=self.__headers)
            html_bytes: bytes = urlopen(response).read()
            buff: BytesIO = BytesIO(html_bytes)
            f = gzip.GzipFile(fileobj=buff)
            result: str = f.read().decode('gbk', errors='replace')
        except URLError as error:
            print('Downloading error: ' + error.reason)
            result = ''
        return result

    def __process_pages_nav(self, pages: list):
        name_pattern: str = 'alt=\'(.*)\''
        detail_page_pattern: str = '<div class="sp"><span class="pics pics2"> <a href=\'(.*)\' class=\'title\'>'
        total_page = len(pages)
        for index, page in enumerate(pages):
            progress: str = format(float(index)/float(total_page), '.2f')
            print('progress: ' + progress + ' ' + str(index) + ' of ' + str(total_page))
            current_link: str = self.__site_name + '/name/' + page
            current_html: str = self.__get_website(current_link)
            name_results: list = re.findall(name_pattern, current_html)
            detail_links: list = re.findall(detail_page_pattern, current_html)
            if len(name_results) == len(detail_links):
                for index_y, detail_link in enumerate(detail_links):
                    self.__process_detail_page(detail_link, name_results[index_y])
        print('get files complete')

    def __process_detail_page(self, link: str, name: str):
        print('process: ' + link)
        detail_html: str = self.__get_website(link)
        image_pattern: str = 'src="(.*).jpg"'
        image_results: list = re.findall(image_pattern, detail_html)
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
        self.__index_file.write(name + ' ' + link + ' ')
        if len(image_results) != 0:
            self.__index_file.write(self.__site_name + image_results[0] + '.jpg' + '\n')
        else:
            self.__index_file.write('\n')

    def process(self):
        html: str = self.__get_website(self.__site_name + '/name')
        pages_pattern: str = '<option value=\'(.*)\''
        pages_link: list = re.findall(pages_pattern, html)
        self.__process_pages_nav(pages_link)
