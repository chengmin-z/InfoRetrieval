import logging
import signal
import time

from crawler import Crawler
from extract import ExtractorClient
import search
import extract

from sanic import Sanic
from sanic import response
from sanic import exceptions

app = Sanic('Remote')


@app.exception(exceptions.NotFound)
async def ignore_404():
    return response.text('errorUrl', status=404)


@app.post('infoAccess/extraction')
async def extraction(request):
    query_str: str = request.json.get('input')
    start = time.perf_counter()
    result = ExtractorClient.process(content=query_str)
    end = time.perf_counter()
    print('Extractor Running time: %s Seconds' % (end - start))
    return response.json({'code': 200, 'msg': 'success', 'data': result['body']['Content']}, status=200)


@app.post('infoAccess/retrieval')
async def retrieval(request):
    query_str: str = request.json.get('input')
    start = time.perf_counter()
    result = search.retrieval_query(query_str)
    end = time.perf_counter()
    print('Retrieval Running time: %s Seconds' % (end - start))
    return response.json({'code': 200, 'msg': 'success', 'data': result}, status=200)


@app.get('infoAccess/getNames')
async def get_names(request):
    result = extract.get_all_name()
    return response.json({'code': 200, 'msg': 'success', 'data': result}, status=200)


@app.post('infoAccess/getInfoContent')
async def get_info_content(request):
    name: str = request.json.get('name')
    result = extract.get_info_content(name)
    return response.json({'code': 200, 'msg': 'success', 'data': result}, status=200)


def main():
    print('[INFO] Welcome to use the backend of retrieval system')
    update_file = input('[INFO] Do you want to update the datafiles and construct inverted index? (yes/on): ')
    if update_file == 'yes':
        Crawler().process()
        print('[INFO] progress: Creating inverse index txt_file')
        search.create_inverse_txt()
        print('[INFO] progress: Created inverse index txt_file done')
    else:
        update_reverse_index = input('[INFO] Do you want to construct inverted index? (yes/on): ')
        if update_reverse_index == 'yes':
            print('[INFO] progress: Creating inverse index txt_file')
            search.create_inverse_txt()
            print('[INFO] progress: Created inverse index txt_file done')

    print('[INFO] Backend running')

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    _logFmt = logging.Formatter('%(ascTime)s %(levelName).1s %(lineno)-3d %(funcName)-20s %(message)s',
                                datefmt='%H:%M:%S')
    _consoleHandler = logging.StreamHandler()
    _consoleHandler.setLevel(logging.DEBUG)
    _consoleHandler.setFormatter(_logFmt)

    log = logging.getLogger(__file__)
    log.addHandler(_consoleHandler)
    log.setLevel(logging.DEBUG)

    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
