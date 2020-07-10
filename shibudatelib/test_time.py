from main import addtime

path = "data/財団作成_別巻第1_4.0.xml"

f = open(path)
text = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()

text = addtime(text)

file = open('data/add_time.xml', 'w')
file.write(text)
file.close()