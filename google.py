"""Selenium で Google を開いて検索するサンプルスクリプト"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def main():
    # Chrome の起動オプションを作成
    options = Options()
    options.add_argument("--start-maximized")

    # WebDriver を起動（必要な ChromeDriver を自動インストール）
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    try:
        # Google トップページを開く
        driver.get("https://www.google.com")
        time.sleep(3)

        # 検索ボックス要素を取得して検索語を入力
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium Python")

        # 検索を送信
        search_box.submit()

        # 結果表示を待機
        time.sleep(5)
    finally:
        # ブラウザを閉じる
        driver.quit()


if __name__ == "__main__":
    main()

