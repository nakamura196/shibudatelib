from main import inf
import bs4
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('path', help='この引数の説明（なくてもよい）')

args = parser.parse_args()    # 4. 引数を解析

path = args.path

output_path = path + "_custom_when.xml"

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = bs4.BeautifulSoup(open(path), 'xml')

entries = soup.find_all(type="diary-entry")

flg = False

for i in range(len(entries)):
    entry = entries[i]

    id = entry.get("xml:id")

    if "DKB10001m-" in id:
        flg = True

    if "DKB10004m-" in id:
        flg = False

    if flg:

        # print(entry)
        head = entry.find("head")

        if not head:
            continue

        date_array = head.find_all("date")
        if len(date_array) == 2:

            renzokuFlg = True

            for date in date_array:
                # print(date)
                if "月" in date.text and "日" in date.text:
                    aaa = "bbb"
                else:
                    renzokuFlg = False

            if renzokuFlg:

                date1 = date_array[0]
                date2 = date_array[1]

                if date1["when"] < date2["when"]:
                    date2["when"] = date1["when"]
                    date2["type"] = "旧暦"
                else:
                    date1["when"] = date2["when"]
                    date1["type"] = "旧暦"
                

html = soup.prettify("utf-8")
with open(output_path, "wb") as file:
    file.write(html)