"""
referrence
https://www.youtube.com/watch?v=Gh0qRBHbnVs
"""

#文字列の代入
name = "jaganiku"
birthplace = "東京"
print("私は{}です。出身は{}です。".format(name, birthplace))
print(f"私は{name}っす。出身は{birthplace}っす。")

#エスケープシーケンス
print("いつものか帰り道とは違うルートで、 \n帰ってみようかな")

#書式化
print("10新数=%d, 16進数=%x, 10進浮動小数点=%f" % (16, 16, 16))

#大文字小文字
print("hello".upper())
print("HELLO".lower())

#文字列の分割
sentence = "　こんにちは。\n私はロボットです。"
messages = sentence.split("\n")
print(messages)

#文字列の結合
print('\n'.join(messages))

#空白の削除
print(sentence.strip())

#文字列の置換
print(sentence.replace("ロボット", "人間"))

#文字列の検索
print(sentence.find("。"))

#文字列への変換
print(str(1))
print(str(1.5))
print(str([1, 2]))

#包含関係
a, b = 'sba', 'gsba'
print(a in b)

#リスト操作
numbers = [0, 3, 8, -4, 9, 1]
print(numbers[1])
print(numbers[-1])
print(numbers)
numbers.append(2)
numbers.insert(0, 5)#先頭に5
numbers.insert(0, -3)#最後に-3
numbers.remove(5)#5という"値"を削除する
numbers.pop(-3)#後ろから3番目の"index"を削除

#filter　で奇数を除外
def isEven(number):
    if(number % 2 == 0):
        return True
    else:
        return False

print(list(filter(isEven, numbers)))

#index番号の取得
print(numbers.index(8))

#sort
numbers.sort()
numbers.sort(reverse=True)

#dictionary
dictionary = {
    "A":"これは",
    "B":"ただの",
    "C":"辞書",
    "D":"です"
}

print("辞書" in dictionary.values())

#中身をすべて表示
for key, value in dictionary.items():
    print(f"キーは'{key}',値は'{value}'です。")

#値の取得
dictionary.get("F")#キーがなくてもエラーが起きないのが[]との違い

dictionary.pop("A")#キーがA
dictionary.clear()#すべて削除
dictionary.keys()#すべてのkey

#条件式
a = 3
if 0 <= a < 10 and a % 2 == 0:
    print("一桁の偶数")
elif a < 0 and a % 2 == 1:
    print("負の奇数")
else:
    print("整数")

#制御構文
for number in numbers:
    print(number)

for i in range(10, 20):#10スタートで10個
    print(i)

for i in range(10):
    if i == 3:
        print('3をスキップ')
        continue
    if i == 6:
        print('終了')
        break#for文の終了
    print(i)

#複数の要素
lasts = ['鈴木', '田中', '佐藤']
firsts = ['健一', '二郎', '三太']
for last, first in zip(lasts, firsts):
    print(last + first)

#indexを取得
for i, last in enumerate(lasts):
    print(f"{i}番目の名前は{last}です。")

#内包表記
nums = []
for i in range(5):
    nums.append(i * 2)

numbers = {2 * i for i in range(5)}
print(numbers)

#例外処理
num = 0
def devide(a, b):
    try:
        print(f"結果:{a/b}")
    except ZeroDivisionError as e:
        print("0を使ったエラー")
        print(e)
    except TypeError as e:
        print("型が違います")
        print(e)
        #pass#何も実行しない場合
    else:#正常に終了した場合のみ挙動
    #finally:#exceptに行った後も含む挙動
        print("正常に終わりました。")


devide(10, 2)
devide(10, 0)
devide("a", 0)

#クラス
class Person:
    def __init__(self, name):
        self.name = name
        self.nationality = "Japan"

    def say_hello(self):
        print(f"私の国籍は{self.nationality}です。")

    def say_name(self):
        print(f"私の名前は{self.name}です。")

person = Person("Taro")
person.say_hello()
person.say_name()

#クラスの継承
class Kid(Person):
    def say_hello(self, age):
        print(f"{self.name}は{age}です。")

kid = Kid("健介")
kid.say_hello(2)


#privateクラス(インスタンスから関数を呼び出せない)
class Person:
    __nationality = "Japan"

    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"私の国籍は{self.__nationality}です。")

    def __say_name(self):
        print(f"私の名前は{self.name}です。")

person = Person("Taro")
#person.nationality #オブジェクトからの呼び出しなのでエラーが起きる
#person.__say_name() #privateな関数なので、エラーが起きる
person.say_hello()#クラス内からフィールド呼び出しであるため、エラーが起きない


