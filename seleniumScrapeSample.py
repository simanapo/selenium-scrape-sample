from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import time

# ヘッドレスモードを有効にする場合
# options = Options()
# options.add_argument('--headless')
# chrome = webdriver.Chrome("c:/driver/chromedriver.exe", chrome_options=options)

chrome = webdriver.Chrome("c:/driver/chromedriver.exe")
chrome.get('https://www.google.co.jp/')

# 検索キーワード・サイト内検索キーサイト・取得ページ数入力
keyword = input("検索キーワード入力：")
search_keyword = input("サイト内検索キーワード入力(半角スペースで複数入力可)：")
per = input("何ページ目まで取得するか(半角数字入力)：")

# 検索実行
search_box = chrome.find_element_by_name("q")
search_box.send_keys(keyword)
search_box.send_keys(Keys.RETURN)

# 検索結果取得
result_title = []
result_url = []
rank = []
search_words_count = []
index = 1

# ページネーション単位で処理実行
for i in range(int(per)):
    try:
        for i, g in enumerate(chrome.find_elements_by_class_name("g")):
            try:
                r = g.find_element_by_class_name("r")
                # タイトル取得
                result_title.append(r.find_element_by_tag_name("h3").text)

                # URL取得
                result_url.append(r.find_element_by_tag_name("a").get_attribute("href"))

                rank.append(index)
                index += 1
            except:
                print("スキップ")

        for target_url in result_url:
            # 取得URLに遷移
            chrome.get(target_url)
            try:
                # サイト内検索キーワードから該当個数を取得
                search_keyword_box = ''
                for i, g in enumerate(search_keyword.split(" ")):
                    if len(chrome.find_elements_by_xpath("//*[contains(text(), '{0}')]".format(g))) > 0:
                        search_keyword_box += str(len(chrome.find_elements_by_xpath("//*[contains(text(), '{0}')]".format(g)))) + ','
                    else:
                        search_keyword_box += '0,'
                search_words_count.append(search_keyword_box.strip(','))
            except:
                search_words_count.append(0)

            chrome.back()

        # 次ページ取得・遷移
        next = chrome.find_element_by_css_selector("#navcnt table td.cur + td a")
        next.click()
    except:
        chrome.close()

    # 5秒間スリープ
    time.sleep(5)

# 検索結果をCSV出力
with open('[' + keyword + ']google_search_result.csv', 'w', newline='', encoding='CP932', errors='replace') as f:
    writer = csv.writer(f)
    writer.writerow(['検索キーワード:{0}'.format(keyword), 'サイト内検索キーワード:{0}'.format(search_keyword)])
    writer.writerows([rank])
    writer.writerows([result_title])
    writer.writerows([result_url])
    writer.writerows([search_words_count])