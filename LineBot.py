# @(#) LineBot.py
# by:
#  shun.nonomura
#
# Usage:
#  python3 /path/to/LineBot.py
#
# Description:
#  Webの記事を取得してLineにPUSH通知する
# _______________________________________________



# ライブラリインポート
# ===============================================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from linebot import LineBotApi
from linebot.models import TextSendMessage
import time



# 定数定義
# ===============================================
USER_ID = "ユーザID"
ACCESS_TOKEN = "アクセストークン"



# Class定義
# ===============================================
# Class名         ：WebScrapingAndPushLineMessage
# Description     ：記事を取得してLINEへPUSH
# インスタンス変数：無し
class WebScrapingAndPushLineMessage:


    # ===============================================
    # method_name：get_trend_kiji
    # Description：ヘッドレスchromeでWebページににアクセスして記事を取得
    # 引数1      ：サイトURL
    # 引数2      ：記事要素のクラス名
    # 引数3      ：記事タイトルのタグ
    # 引数4      ：プッシュするメッセージのヘッダ
    # 引数5      ：取得する記事の数（リストに格納するので開始は「0固定」）
    # 引数6      ：記事の取得数
    def get_trend_kiji(self,url,class_name,title_tag,message_header,num,num_max):
  
        # global変数を定義
        global push_line_messages
  
        # headless chrome起動オプション
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,1024')
  
        # 使用するドライバーを指定
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptInsecureCerts'] = True
        driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capabilities)
  
        # chromeで指定のURLにアクセス
        driver.get(url)
        time.sleep(5)
  
        # 記事要素のクラス名を指定して取得
        class_info = driver.find_elements_by_class_name(class_name)
  
        # 取得した情報を格納するリストを作成
        title_list = []
        url_list = []
        # 取得する記事の数を指定（リストに取得記事を格納しているので０始まり、↓の例は上位10記事を取得）
        start = num
        end = num_max  

        # 取得したclass情報からタグ情報を取得
        for element in class_info:
  
            url = element.find_element_by_tag_name('a').get_attribute('href')
            title = element.find_element_by_tag_name(title_tag).text
  
            title_list.append(title)
            url_list.append(url)
 
        # 通知用のメッセージを格納する変数を定義
        push_line_messages = message_header
  
        # 通知用のメッセージを作成
        while start <= end:
  
            push_line_messages = push_line_messages + "・" + title_list[start] + "\n" + url_list[start] + "\n\n"
            start += 1
  
        driver.close()
        driver.quit()


    # ===============================================
    # method_name：exec_push_message
    # Description：ラインへメッセージをプッシュする
    # 引数1      ：プッシュするメッセージを格納した変数
    def exec_push_message(self,push_line_messages):

        line_bot_api = LineBotApi(ACCESS_TOKEN)
        messages = TextSendMessage(text=push_line_messages)
        line_bot_api.push_message(USER_ID, messages=messages)



# メイン処理  
# ===============================================
if __name__ == "__main__":

    try:

        # クラスのインスタンス化
        kijiget_and_linepush = WebScrapingAndPushLineMessage()

        # Qiitaの記事取得
        class_name = "css-16qp2r"
        url = "https://qiita.com/"
        title_tag = "h2"
        message_header = "▼Qiita トレンド記事\n\n"
        num = 0
        num_max = 9
        kijiget_and_linepush.get_trend_kiji(url,class_name,title_tag,message_header,num,num_max)
        kijiget_and_linepush.exec_push_message(push_line_messages)

        # はてなブログの記事取得
        class_name = "entrylist-contents"
        url = "https://b.hatena.ne.jp/hotentry/it"
        title_tag = "h3"
        message_header = "▼はてぶろ トレンド記事\n\n"
        num = 0
        num_max = 9
        kijiget_and_linepush.get_trend_kiji(url,class_name,title_tag,message_header,num,num_max)
        kijiget_and_linepush.exec_push_message(push_line_messages)


    except Exception as e:

        # プッシュするエラーメッセージ
        error_message = "===== Scraping Error =====\nエラーが発生しました\n---------- Error Message ----------\n{}".format(e)
        kijiget_and_linepush.exec_push_message(error_message)

