from main import addtime, adddate, inf
import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('path', help='この引数の説明（なくてもよい）')

args = parser.parse_args()    # 4. 引数を解析

path = args.path

f = open(path)
text = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()

text = addtime(text)
text = adddate(text)

ipath = path + "_add.xml"

file = open(ipath, 'w')
file.write(text)
file.close()

opath = path + "_inf.xml"

inf(ipath, opath)