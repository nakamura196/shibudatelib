# shibudatelib

## インストール

~~~
pip install git+https://github.com/nakamura196/shibudatelib.git -t lib
~~~

## 実行

~~~
# モジュールをインストールした lib にパスを通しておく
import sys

sys.path.append('lib')

# モジュール内の関数を import する
from shibudatelib.main import adddate

text = '現在原本は、明治二年の和綴横帳の分及び明治十七年の第一銀行京都支店所蔵分を除く外、'

# モジュール内の関数を呼び出す
print(adddate(text))
~~~
