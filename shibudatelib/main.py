import re
import hashlib

idMap = {}

def addtag(pattern, text):
    m = re.findall(pattern, text)
    for e in m:
        id = hashlib.md5(e.encode('utf-8')).hexdigest()
        idMap[id] = e
        text = text.replace(e, id)
    return text

def adddate(text):
    warekiPattern = "[明慶大昭][治応正和]"
    yearPattern = "[一二三四五六七八九十廿]+?年"
    monthPattern = "[一二三四五六七八九十廿]+?月"
    dayPattern = "[一二三四五六七八九十廿]+?日"
    
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
        text = text.replace(id, "<date>"+idMap[id]+"</date>")

    return text