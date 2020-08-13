from main import inf
import bs4
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('path', help='この引数の説明（なくてもよい）')

args = parser.parse_args()    # 4. 引数を解析

path = args.path

output_path = path + "_custom_head.xml"

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = bs4.BeautifulSoup(open(path), 'xml')

entries = soup.find_all(type="diary-entry")

flg = False

for i in range(len(entries)):
    entry = entries[i]

    head = entry.find("head")

    if not head:
        continue

    times = head.find_all("time")

    if len(times) > 0:
        for time in times:
            time.unwrap()

    

html = soup.prettify("utf-8")
with open(output_path, "wb") as file:
    file.write(html)