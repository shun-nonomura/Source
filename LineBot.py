# @(#) LineBot.py
# by:
#  shun.nonomura
#
# Usage:
#  python3 /path/to/LineBot.py
#
# Description:
#  Qiitaの記事を取得してLineにPUSH通知する
# _______________________________________________


# ライブラリインポート
# ===============================================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from linebot import LineBotApi
from linebot.models import TextSendMessage
import time



# 変数定義
# ===============================================
USER_ID = "Uff13b91191ecce3bed733b321913a92b"
ACCESS_TOKEN = "PPu6DFSWh2lgMz8GcCUivIsIOU5z6FnYpyBXRG8unD4KWzSoDnvr60Iv0Pf3lyqGHi63kuAZiPYt7M9E9srvPGVKhslvPLGFQHIEHS/oNrLmreh2fb4+dW3mFYsRT/c+TaQiDrdLt5r3L0opQqlJJQdB04t89/1O/w1cDnyilFU="



# 関数定義
# ===============================================
# 関数名：get_trend_kiji
# 説明　：ヘッドレスchromeでQiitaのTOPページにアクセスして記事を取得
# 引数1 ：サイトURL
# 引数2 ：記事要素のクラス名
# 引数3 ：記事タイトルのタグ
# 引数4 ：プッシュするメッセージのヘッダ
# ===============================================
def get_trend_kiji(url,class_name,title_tag,message_header):

    # global変数を定義
    global push_line_messages
    global num
    global num_max

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
    num = 0
    num_max = 9

    # 取得したclass情報からaタグ、h2タグを取得
    for element in class_info:

        url = element.find_element_by_tag_name('a').get_attribute('href')
        title = element.find_element_by_tag_name(title_tag).text

        title_list.append(title)
        url_list.append(url)
    
    # 通知用のメッセージを格納する変数を定義
    push_line_messages = message_header

    # 通知用のメッセージを作成
    while num <= num_max:

        push_line_messages = push_line_messages + "・" + title_list[num] + "\n" + url_list[num] + "\n\n"
        num += 1

    driver.close()
    driver.quit()



# ===============================================
# 関数名：exec_push_message
# 説明　：ラインへメッセージをプッシュする
# 引数　：プッシュするメッセージを格納した変数
# ===============================================
def exec_push_message(push_line_messages):

    line_bot_api = LineBotApi(ACCESS_TOKEN)
    messages = TextSendMessage(text=push_line_messages)
    line_bot_api.push_message(USER_ID, messages=messages)



#                メイン処理  
# ===============================================
if __name__ == "__main__":

    try:
        # global変数を定義
        global push_line_messages


        # qiita trend記事TOP10を取得
        class_name = "css-16qp2r"
        url = "https://qiita.com/"
        title_tag = "h2"
        message_header = "▼Qiita トレンド記事\n\n"
        get_trend_kiji(url,class_name,title_tag,message_header)
        # 取得した記事をプッシュ通知
        exec_push_message(push_line_messages)


        # はてぶろ trend記事TOP10を取得
        class_name = "entrylist-contents"
        url = "https://b.hatena.ne.jp/hotentry/it"
        title_tag = "h3"
        message_header = "▼はてぶろ トレンド記事\n\n"
        get_trend_kiji(url,class_name,title_tag,message_header)
        # 取得した記事をプッシュ通知
        exec_push_message(push_line_messages)


    # classから情報が取得できない場合はリストに値が入らないので「IndexError」になったときはエラー内容をプッシュする
    except IndexError as e:

        # プッシュするエラーメッセージ
        error_message = "===== Scraping Error =====\nHTML要素が変更された可能性があります\n---------- Error Message ----------\n{}".format(e)

        # エラーメッセージをプッシュ
        exec_push_message(error_message)

