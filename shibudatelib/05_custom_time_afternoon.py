from main import inf
import bs4
import argparse    # 1. argparseをインポート

'''
parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('path', help='この引数の説明（なくてもよい）')

args = parser.parse_args()    # 4. 引数を解析

path = args.path
'''

path = "data/20210122DKB02_schedule_ino.xml_inf.xml_custom_when.xml_custom_time.xml_custom_head.xml"

output_path = path + "_custom_afternoon.xml"

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = bs4.BeautifulSoup(open(path), 'xml')

times = soup.find_all("time")

# current = 0
for time in times:

    ps = str(time.previous_sibling).strip()

    if "午後" in ps or "午后" in ps:
        when = time.get("when")

        when_split = when.split(":")

        h = int(when_split[0])
        h = h + 12

        time["when"] = str(h).zfill(2) + ":" + when_split[1] + ":" + when_split[2]

html = soup.prettify("utf-8")
with open(output_path, "wb") as file:
    file.write(html)