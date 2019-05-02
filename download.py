#Import Libraries
import time
import hashlib
import urllib
import os
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import get_image as GI
import recognition

#検索ワード
recognition_dict=recognition.detection_words
os.mkdir(recognition.image_folder_name)
for word in recognition_dict:
    #ダウンロード数
    imageNum = 100 #最大値100
    USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    
    T0 = time.time()   #開始時間
    #画像リンク取得
    temp = word
    items = []
    
    search = temp.replace(" ", "%20")
    
    print("検索ワード:" + search)
    URL = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    p = urlparse(URL)
    query = urllib.parse.quote_plus(p.query, safe='=&')
    URL = '{}://{}{}{}{}{}{}{}{}'.format(p.scheme, p.netloc, p.path,';' if p.params else '', p.params,'?' if p.query else '', query,'#' if p.fragment else '', p.fragment)
    RAW_HTML = (GI.download_page(URL))
    time.sleep(0.05)
    items.extend(GI._images_get_all_items(RAW_HTML))
    
    print("ダウンロード開始")
    
    errorCount = 0
    Cnt = 0
    folderName = recognition.image_folder_name+'/'+ str(recognition_dict[word])
    if os.path.exists(folderName)==False:
        os.mkdir(folderName)#フォルダー作成
    for item in items:
        if Cnt == imageNum:
            break
        try:
            outputPath = folderName + '/' + hashlib.md5(item.encode('utf-8')).hexdigest() + ".jpg"
            print('-------------------------------------------------------------------')
            if os.path.isfile(outputPath):
                print(outputPath + " ダウンロード済み画像のためスキップ")
            else:
                REQ = urllib.request.Request(item, headers={"User-Agent": USER_AGENT})
                RESPONSE = urlopen(REQ)
                DATA = RESPONSE.read()
                open(outputPath, 'wb').write(DATA)
                RESPONSE.close()
                pass
    
            print("ダウンロード完了 ====> "+str(item))
    
        except IOError:
            errorCount += 1
            Cnt -= 1
            print("IOError"+str(item))
        except HTTPError as e:
            errorCount += 1
            Cnt -= 1
            print("HTTPError"+str(item))
        except URLError as e:
            errorCount += 1
            Cnt -= 1
            print("URLError "+str(item))
        except UnicodeEncodeError as e:
            errorCount += 1
            Cnt -= 1
            print("UnicodeEncodeError "+str(item))
        print('-------------------------------------------------------------------')
        Cnt += 1

print("\n")
print("ダウンロード完了")
print("\n"+str(errorCount)+" ----> 合計エラー数")