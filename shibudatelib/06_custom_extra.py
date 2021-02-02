from main import inf
import bs4
import argparse    # 1. argparseをインポート
import re

'''
parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('path', help='この引数の説明（なくてもよい）')

args = parser.parse_args()    # 4. 引数を解析

path = args.path
'''

path = "data/20210122DKB02_schedule_ino_nakamura_chk210130.xml"

output_path = path + "_custom_extra.xml"

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = bs4.BeautifulSoup(open(path), 'xml')

dates = soup.find_all("date")

for date in dates:
    del date["evidence"]

times = soup.find_all("time")

# current = 0
for time in times:

    del time["cert"]

    del time["evidence"]

    ps = str(time.previous_sibling).strip()

    if "午後" in ps or "午后" in ps or ("午" in ps and "後" not in ps and "前" not in ps and "后" not in ps):

        prefix = ""
        if "午後" in ps:
            prefix = "午後"
        elif "午后" in ps:
            prefix = "午后"
        elif "午" in ps:
            prefix = "午"

        when = time.get("when")

        time.string = prefix + time.text.strip()

        when_split = when.split(":")

        h = int(when_split[0])
        h = h + 12

        time["when"] = str(h).zfill(2) + ":" + when_split[1] + ":" + when_split[2]

    elif "午前" in ps:

        time.string = "午前" + time.text.strip()

bodies = soup.find_all("body")
for body in bodies:
    divs = body.find_all("div", attrs={"type" : "month"})
    for div in divs:
        month = div.find("head").find("date", attrs={"when" : re.compile(r'')}).get("when").split("-")[1]
        
        for date in div.find_all("date", attrs={"when" : re.compile(r'')}):
            when = date.get("when")
            es = when.split("-")
            if len(es) > 1 and es[1] == "XX":
                date["when"] = es[0] + "-" + month + "-" + es[2]

html = str(soup) # .prettify("utf-8")

map = {
    "正午" : '''<time when="12:00:00">正午</time>''',
    "午〇時半" : '''<time when="12:30:00">午〇時半</time>''',
    "午後〇半時" : '''<time when="12:30:00">午後〇半時</time>''',
    "午時" : '''<time when="12:00:00">午時</time>''',
}

keys = ["午前", "午後", "午后", "牛"]

for key in keys:


    key2 = '''{}
          <time'''.format(key)

    key3 = '''{}<time'''.format(key)


    map[key2] = "<time"
    map[key3] = "<time"

for key in map:
    html = html.replace(key, map[key])

with open(output_path, "w") as file:
    file.write(html)