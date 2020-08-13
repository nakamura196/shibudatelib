from main import adddate

path = "data/01.xml"

f = open(path)
text = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()

text = '''
<div type="diary-entry" xml:id="DKB10003m-20">
    <head>（十一月）十日　晴</head>
    <p>例刻出省、戸籍掛之者儀ニ付見込少丞へ申立る、取調草案類出来す
        遠州静岡藩管轄地江御貸下之紙幣之儀ニ付、岡本江承合す、夕方小川街邸に至る、織田其外有司面会す、駿河台にて邸宅見分す、松本新作を訪ふ、不在にて面会なし、夜に入帰宿、此夜尾高藍香郷里より来る、家君之書持参す</p>
</div>
<head>（五月）あああ三十日ああああ</head>
'''

text = adddate(text)

print(text)

file = open('data/add_date.xml', 'w')
file.write(text)
file.close()