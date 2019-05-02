import time
import urllib
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

#ダウンロード
def download_page(url):
    import urllib.request
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(str(e))


#検索
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line+1)
        end_content = s.find(',"ow"', start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#リンク取得
def _images_get_all_items(page):
    _items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            _items.append(item)
            time.sleep(0.05)
            page = page[end_content:]
    return _items