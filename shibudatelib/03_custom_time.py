from main import inf
import bs4
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('path', help='この引数の説明（なくてもよい）')

args = parser.parse_args()    # 4. 引数を解析

path = args.path

output_path = path + "_custom_time.xml"

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = bs4.BeautifulSoup(open(path), 'xml')

entries = soup.find_all(type="diary-entry")

flg = False

for i in range(len(entries)):
    entry = entries[i]

    

    p = entry.find("p")

    if not p:
        continue

    times = p.find_all("time")

    current = 0
    for time in times:
        when = time.get("when")

        when_split = when.split(":")

        h = int(when_split[0])

        if current > h:
            h = h + 12

        current = h

        time["when"] = str(h).zfill(2) + ":" + when_split[1] + ":" + when_split[2]

html = soup.prettify("utf-8")
with open(output_path, "wb") as file:
    file.write(html)