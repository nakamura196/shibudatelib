from main import adddate

path = "data/01.xml"

f = open(path)
text = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()

text = '''
<div type="diary-entry" xml:id="DKB10003m-20">
    <head>（十一月）十日　晴</head>

       <body>
                    <div type="month">
                        <head>
                            <date>十二月</date>
                        </head>
                        <div type="day" xml:id="DKB20015m-1">
                            <head>
                                <date>十七日（水）</date>
                            </head>
                            <listEvent>
                                <event>
                                    <p>午前十一時　　帝国劇場役員会（中央亭）</p>
                                </event>
                                <event>
                                    <p>　　　　　　　午後一時半　　教育調査会（文部大臣官舎）</p>
                                </event>
                                <event>
                                    <p>　　　　　　　午後四時　　　渡米実業団記念会（日本橋クラブ）</p>
                                </event>
                            </listEvent>
                        </div>
                        </div>
                        </body>

                        
    <p>例刻出省、戸籍掛之者儀ニ付見込少丞へ申立る、取調草案類出来す
    午前十一時　　帝国劇場役員会（中央亭）
    <head>
                            <date>十二月</date>
                        </head>
                        <div type="day" xml:id="DKB20015m-1">
                            <head>
                                <date>十七日（水）</date>
                            </head>
                            <listEvent>
                                <event>
                                    <p>午前十一時　　帝国劇場役員会（中央亭）</p>
                                </event>
                                <event>
                                    <p>　　　　　　　午後一時半　　教育調査会（文部大臣官舎）</p>
                                </event>
                                <event>
                                    <p>　　　　　　　午後四時　　　渡米実業団記念会（日本橋クラブ）</p>
                                </event>
                            </listEvent>
                        </div>
                        <div type="day" xml:id="DKB20015m-2">
                            <head>
                                <date>十八日（木）</date>
                            </head>
                            <listEvent>
                                <event>
                                    <p>午後一時　　　第一銀行</p>
                                </event>
                                <event>
                                    <p>　　　　　　　午後三時　　　諸井恒平氏ヨリ御案内</p>
                                </event>
                            </listEvent>
                        </div>
    <date>十八日（木）</date>
        遠州静岡藩管轄地江御貸下之紙幣之儀ニ付、岡本江承合す、夕方小川街邸に至る、織田其外有司面会す、駿河台にて邸宅見分す、松本新作を訪ふ、不在にて面会なし、夜に入帰宿、此夜尾高藍香郷里より来る、家君之書持参す</p>
</div>
<head>（五月）あああ三十日ああああ</head>
'''

text = adddate(text)

print(text)

file = open('data/add_date.xml', 'w')
file.write(text)
file.close()