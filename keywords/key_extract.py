import requests
from bs4 import BeautifulSoup

import termextract.mecab
import termextract.janome
import termextract.core
from janome.tokenizer import Tokenizer
import collections

import json

# 指定のURLからテキストを取得する関数
def get_text_from_url(url):
    # 指定されたURLにGETリクエストを送信し、レスポンスを取得
    response = requests.get(url)
    html_content = response.content
    
    # レスポンスのテキスト部分をBeautifulSoupを使ってパースし、テキストのみ抽出
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    
    return text

# メインの処理
def main():
    # キーワードを抽出したい対象のURLを指定
    target_url = "https://www.keio.ac.jp/ja/about/"
    
    # 指定したURLからテキストを取得
    text = get_text_from_url(target_url)

    # Janomeを使ってテキストを単語にトークン化
    t = Tokenizer()
    tokens = t.tokenize(text)

    frequency = termextract.janome.cmp_noun_dict(tokens)

    lr = termextract.core.score_lr(
        frequency,
        ignore_words=termextract.mecab.IGNORE_WORDS,
        lr_mode=1, average_rate=1)

    term_imp = termextract.core.term_importance(frequency, lr)

    keywords_list = []

    data_collection = collections.Counter(term_imp)
    for cmp_noun, value in data_collection.most_common():
    #    print(termextract.core.modify_agglutinative_lang(cmp_noun),value, sep="\t")

        keywords_list.append({"keyword" : termextract.core.modify_agglutinative_lang(cmp_noun), "value" : value})

    #keyword_listをJSON形式で出力
    with open("keywords.json", "w", encoding="utf-8") as json_file:
        json.dump(keywords_list, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()

    