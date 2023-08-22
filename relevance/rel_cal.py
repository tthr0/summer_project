import requests
from bs4 import BeautifulSoup

website_url = "https://sample.com"  # 対象のウェブサイトのURL
values_to_check = ["(VALUE)", "(VALUE)", "(VALUE)"]  # 関連性を調べる値のリスト

# ウェブサイトへアクセスしてページのHTMLを取得
response = requests.get(website_url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

related_weight = 0


for value in values_to_check:
    related = False

    for paragraph in soup.find_all('p'):
        if value in paragraph.get_text():
            related = True
            related_weight += 1
            break
    
    if related:
        print(f"値 '{value}' は関連性があります。")
    else:
        print(f"値 '{value}' は関連性がありません。")

print("関連度:",related_weight)
