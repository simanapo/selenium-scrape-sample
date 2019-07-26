from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import time

class Scrape:

    def __init__(self, keyword, search_keyword, per):
        self.keyword = keyword
        self.search_keyword = search_keyword
        self.per = per

        # 検索結果取得
        self.result_title = []
        self.result_url = []
        self.rank = []
        self.search_words_count = []
        self.index = 1

    # メイン処理
    def execute(self):
        # ヘッドレスモードを有効にする場合
        # options = Options()
        # options.add_argument('--headless')
        # chrome = webdriver.Chrome("c:/driver/chromedriver.exe", chrome_options=options)

        chrome = webdriver.Chrome("c:/driver/chromedriver.exe")
        chrome.get('https://www.google.co.jp/')

        self.scrape_search_keyword(chrome)
        self.output()

    # スクレイピング処理
    def scrape_search_keyword(self, chrome):
        # 検索実行
        search_box = chrome.find_element_by_name("q")
        search_box.send_keys(self.keyword)
        search_box.send_keys(Keys.RETURN)

        # ページネーション単位で処理実行
        for i in range(int(self.per)):
            try:
                for i, g in enumerate(chrome.find_elements_by_class_name("g")):
                    try:
                        r = g.find_element_by_class_name("r")
                        # タイトル取得
                        self.result_title.append(r.find_element_by_tag_name("h3").text)

                        # URL取得
                        self.result_url.append(r.find_element_by_tag_name("a").get_attribute("href"))

                        self.rank.append(self.index)
                        self.index += 1
                    except:
                        print("スキップ")

                # 次ページ取得・遷移
                next = chrome.find_element_by_css_selector("#navcnt table td.cur + td a")
                next.click()
            except:
                print('エラーが発生しました。')

        for target_url in self.result_url:
            # 取得URLに遷移
            chrome.get(target_url)
            # 5秒間スリープ
            time.sleep(5)

            try:
                # サイト内検索キーワードから該当個数を取得
                search_keyword_box = ''
                for i, g in enumerate(self.search_keyword.split(" ")):
                    if len(chrome.find_elements_by_xpath("//*[contains(text(), '{0}')]".format(g))) > 0:
                        search_keyword_box += str(len(chrome.find_elements_by_xpath("//*[contains(text(), '{0}')]".format(g)))) + ','
                    else:
                        search_keyword_box += '0,'
                self.search_words_count.append(search_keyword_box.strip(','))
            except:
                self.search_words_count.append(0)

        chrome.close()

    # CSV出力処理
    def output(self):
        with open('[' + self.keyword + ']google_search_result.csv', 'w', newline='', encoding='CP932', errors='replace') as f:
            writer = csv.writer(f)
            writer.writerow(['検索キーワード:{0}'.format(self.keyword), 'サイト内検索キーワード:{0}'.format(self.search_keyword)])
            writer.writerows([self.rank])
            writer.writerows([self.result_title])
            writer.writerows([self.result_url])
            writer.writerows([self.search_words_count])

# 検索キーワード・サイト内検索キーサイト・取得ページ数入力
keyword = input("検索キーワード入力：")
search_keyword = input("サイト内検索キーワード入力(半角スペースで複数入力可)：")
per = input("何ページ目まで取得するか(半角数字入力)：")

# 実行
scrape = Scrape(keyword, search_keyword, per)
scrape.execute()