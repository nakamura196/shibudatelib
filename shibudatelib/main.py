import re
import hashlib
import requests
from kanjize import int2kanji, kanji2int
from jeraconv import jeraconv
import bs4

idMap = {}
huMap = {}

# 日付の追加処理　(1)廿→20　(2)正月→1月(3)閏四月
# 第十一時がミス
# 時間を足していく

'''
(1)日付→単語として扱うもの
*6-12：「別巻第一日記」
*164-170：「渋沢栄一日記」
*1506-1519：「四日市伏木新潟巡回紀行」
*7194-7207：「四日市」
*9156-9163：「三日程」日付ではない、でもここは手修正か

(2)数値が分割されて還元されてしまっているもの
*3986-4010：「廿一日」
*6699-6703：「三十日」
*7019-7025：「十一日」
*14466-14469：「十一時」

(3)日付として変換したいもの
*4242-4259：「正月」→1月
*5387-5395：「正月」→1月、「朔」→1日、後者は個別確認が必要か
*5742-5479：「正月」→1月、「元日」→1日
'''

numbers = "元一二弐三四五六七八九十廿卅正朔千百"

itaiji = {
    "元" : "一",
    "廿": "二十",
    "卅" : "三十",
    "弐" : "二",
    "正" : "一",
    "朔" : "一"
}

stops_array = ["日記", "四日市", "三日程"]

stops_map = {}
for s in stops_array:
    stops_map[s] = hashlib.md5(s.encode('utf-8')).hexdigest()

# J2W クラスのインスタンス生成
# このタイミングで変換の要となる JSON データが load される
j2w = jeraconv.J2W()

def addtag(pattern, text):
    m = re.findall(pattern, text)
    for i in range(len(m)):
        e = m[len(m) - 1 -i]
        id = hashlib.md5(e.encode('utf-8')).hexdigest()
        idMap[id] = e
        text = text.replace(e, id)
    return text

def adddate(text):
    warekiPattern = "[明慶大昭][治応正和]"
    yearPattern = "["+numbers+"]+?年"
    monthPattern = "["+numbers+"]+?月"
    dayPattern = "["+numbers+"]+?日"

    # 除外語を置換
    for stopword in stops_map:
        text = text.replace(stopword, stops_map[stopword])
    
    # 4
    text = addtag(warekiPattern + yearPattern + monthPattern + dayPattern, text)
    
    # 3
    text = addtag(warekiPattern + yearPattern + monthPattern, text)
    text = addtag(yearPattern + monthPattern + dayPattern, text)
    
    # 2
    text = addtag(warekiPattern + yearPattern, text)
    text = addtag(yearPattern + monthPattern, text)
    text = addtag(monthPattern + dayPattern, text)

    # 1
    text = addtag(yearPattern, text)
    text = addtag(monthPattern, text)

    text = addtag(dayPattern, text)

    for id in idMap:
        value = idMap[id]

        whenObj = getwhen(value)

        text = text.replace(id, "<date"+(" when='"+whenObj["when"]+"'" if whenObj["when"] != None else '')+(" evidence='"+whenObj["evidence"]+"'" if whenObj["evidence"] != None else '')+">"+value+"</date>")

    # 除外語を戻す
    for stopword in stops_map:
        text = text.replace(stops_map[stopword], stopword) 

    return text

def getwhen(value):
    when = None
    note = None


    nengo = None

    newValue = value

    

    for key in itaiji:
        newValue = newValue.replace(key, itaiji[key])

    if value[0:2] in ["慶応", "大正", "明治", "昭和"]:
        nengo = value[0:2]
        newValue = newValue[2:]

    terms = {"年" : "XX", "月" : "XX", "日": "XX"}

    for term in terms:
        if term in newValue:
            org = newValue.split(term)[0]
            terms[term] = str(kanji2int(org)).zfill(2)
            newValue = newValue.replace(org+term, "")

    seireki_year = "XXXX" # terms["年"] if nengo else None
    if nengo:
        param = nengo+str(terms["年"])+'年'
        try:
            seireki_year = str(j2w.convert(param))
        except Exception as e:
            print(param, e)
    
    when = seireki_year
    
    month = terms["月"]
    day = terms["日"]

    if month != "XX":
        when += "-" + month

        
        if day != "XX":
            when += "-" + day

    elif day != "XX":
        when += "-XX-"+day
    
  
    # print(value, when)

    note = ""

    if "XXXX" == seireki_year:
        note += ", year"

    if len(when) != 4:
        if "XX" == month:
            note += ", month"
        
        if "XX" == day:
            note += ", day"


    if note != "":
        note = note[2:]
    else:
        note = None

    obj = {
        "date" : value,
        "when" : when,
        "evidence" : note
    }

    

    return obj



def inf(inputpath, outputpath):
    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = bs4.BeautifulSoup(open(inputpath), 'xml')

    currentYear = "XXXX"

    if not soup.find("text"):
        return

    texts = soup.find("text").find_all("text")

    for text in texts:

        if not text.find("head"):
            continue

        dates = text.find("head").find_all("date")
        
        if len(dates) > 0:
        
            when = dates[0].get("when")
            year = when.split("-")[0]
            if year != "XXXX":
                currentYear = year

        dates = text.find_all("date")

        for date in dates:
            if date.get("when"):
                when = date.get("when")
                year = when.split("-")[0]
                if year == "XXXX":

                    date["when"] = when.replace(year, currentYear)                
                    note = date.get("evidence")
                    note = note.replace("year", "year inferenced")
                    date["evidence"] = note

    html = soup.prettify("utf-8")
    with open(outputpath, "wb") as file:
        file.write(html)

def addtime(text):
    hourPattern = "["+numbers+"]+?時"
    minutePattern = "["+numbers+"]+?分"
    halfPattern = "半"
    
    # 3
    text = addtag(hourPattern + halfPattern, text)

    # 2
    text = addtag(hourPattern + minutePattern, text)

    # 1
    text = addtag(hourPattern, text)

    for id in idMap:
        value = idMap[id]

        whenObj = getTimeWhen(value)

        text = text.replace(id, "<time"+(" when='"+whenObj["when"]+"'" if whenObj["when"] != None else '')+(" cert='"+whenObj["cert"]+"'" if whenObj["cert"] != None else '')+">"+value+"</time>")

    return text

def getTimeWhen(value):
    when = None
    note = None

    newValue = value

    for key in itaiji:
        newValue = newValue.replace(key, itaiji[key])

    terms = {"時" : "00", "分" : "00"}

    for term in terms:
        if term in newValue:
            org = newValue.split(term)[0]
            terms[term] = str(kanji2int(org)).zfill(2)
            newValue = newValue.replace(org+term, "")

    

    
    hour = terms["時"]
    minute = terms["分"]

    if "半" in value:
        minute = "30"

    when = hour + ":" + minute + ":00"

    obj = {
        "time" : value,
        "when" : when,
        "cert" : "low"
    }

    

    return obj

def addWeather(inputpath, outputpath):
    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = bs4.BeautifulSoup(open(inputpath), 'xml')

    currentYear = "XXXX"

    if not soup.find("text"):
        return

    entries = soup.findAll("div", {"type" : "diary-entry"})

    for entry in entries:

        subtype = ""

        head = entry.find("head")

        if not head:
            continue

        headStr = head.text

        weathers = []

        if "晴" in headStr:
            weathers.append("晴")

        if "雨" in headStr:
            weathers.append("雨")

        if "曇" in headStr:
            weathers.append("曇")

        if "雪" in headStr:
            weathers.append("雪")
            
        if len(weathers) > 0:
            subtype += "&weather="+(",").join(weathers)

        dates = head.find_all("date")

        for date in dates:
            when = date.get("when")
            whens = when.split("-")

            if len(whens) == 3 and "XX" not in when:
                subtype += "&date="+when
                break

        if subtype != "":
            entry["subtype"] = subtype[1:]

    html = soup.prettify("utf-8")
    with open(outputpath, "wb") as file:
        file.write(html)