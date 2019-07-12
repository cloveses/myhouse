# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 23:08:41 2019

@author: hironaokumagai
"""

import time
import random

def pt(message,zikan):
    print(message)
    time.sleep(zikan)
from IPython.display import Image,display

url1 = "https://pbs.twimg.com/media/D-iiRYRUwAAbc4T.jpg"

url2 ="https://pbs.twimg.com/media/D-iiSuyVUAAvDWY.jpg"

url3 = "https://pbs.twimg.com/media/D-iiRYPUYAMb1DS.jpg"

url4 = "https://pbs.twimg.com/media/D-G9jnbVAAA7jlC.jpg"

url5 = "https://pbs.twimg.com/media/D-i2d3QU0AETz2L.jpg"

url6 = "https://pbs.twimg.com/media/D-i2d3UUEAInFEi.jpg"

url7 = "https://pbs.twimg.com/media/D-i2d3TUwAAhsiI.jpg"

url8 = "https://pbs.twimg.com/media/D-G9uIKVAAATu7s.jpg"

url9 = "https://pbs.twimg.com/media/D-iiRYRUYAIkAuE.jpg"

url10 = "https://pbs.twimg.com/media/D-iiRYLU4AEZxg1.jpg"

url11 = "https://pbs.twimg.com/media/D-G8gUxVAAEGOQt.jpg"

url12 = "https://pbs.twimg.com/media/D-iq403U8AE3pwy.jpg"

url13 = "https://pbs.twimg.com/media/D-iz5KyVAAESL17.jpg"

url14 = "https://pbs.twimg.com/media/D-iz5KwUwAAktOX.jpg"

nose =200
kuma =250
kodai =150
motii =200

pt('君の住む町は、１００年前からあの能勢に支配されている・・・',2)
pt('その名も能勢帝国',2)
syuzinkou= input("君の名前を教えてくれ")
print('おおぉ',syuzinkou,'か。。。')
time.sleep(2)
pt('いい名前じゃの',2)
answer1 = int(input('''能勢を倒したくないか？
                1,マジむかつくのでぶっ潰したい
                2,まー別に'''))

while True:
    if answer1 == 1:
        break
    elif answer1 == 2:
        pt('ほんとによいのか？',2)
        answer2 = int(input('''1,はい
         2,いいえ'''))
        
        if answer2 == 1:
            pt('うーむ、もう一度考えてみるのじゃ',2)
            continue
        elif answer2 == 2:
            print('そうじゃ、それでこそ',syuzinkou,'じゃ！')
            time.sleep(2)
            break
        else:
            pt('指定された数字のみ入力するのじゃ!',2)
            continue
pt('いきなりだが、能勢と戦うための君の奴隷を選んでもらう',2)
print('画像が確認できたらエンターで進んでね♬')

pt('まずもっちーだーーーーーー',2)
display(Image(url1))
pt('進むにはEnterを押してね',2)
input()
pt('次はクマだーーーーー',2)

display(Image(url2))
pt('進むにはEnterを押してね',2)
input()
pt('最後はこーだいだーーーーーーー',2)

display(Image(url3))
pt('進むにはEnterを押してね',2)
input()
pt('これが奴隷たちの能力だーーー',2)
print('''					
				
						
						
	奴隷	必殺技	HP	レア度	属性	
							
	クマ	空中土下座	250	★★★	マジメ	
	こーだい	シーチーシーブ	150	★★	カス	
	もっちー	イケメンの眼差し200	★	ヒモ	
						
''')
pt('どのどの奴隷といく？？',1)
print('''
    
     ①　クマ
     ②　こーだい
     ③　もっちー

''')
while True:
    
    pt('1~3の数字を選んでね',1)
    answer3 = int(input())


    if answer3 ==1:
        print(syuzinkou,'は　クマ　と行くんだな')
        dorei = str('クマ')
        mikata = kuma
        break
    elif answer3 ==2:
        print(syuzinkou,'は　こーだい　と行くんだな')
        dorei = str('こーだい')
        mikata = kodai
        break
    elif answer3 ==3:
        print(syuzinkou,'は　もっちーを選んだ')
        dorei = str('もっちー')
        mikata = motii
        break
    else:
        print('しっかり奴隷をえらんでよ！！！！')
       
       

display(Image(url4))


pt('能勢が現れた',2)


while True:
    if nose <= 0 :
        pt("能勢を倒すことに成功した！！！",2)
        pt("能勢はすさまじい姿になり、死んだ....",2)
        display(Image(url11))
        print("........fin")
        break
    elif mikata <= 0:
        pt('あれ、、、',2)
        print()
        pt('ちょっと待てよ、、、？',2)
        print()
        print('今の',dorei,'のHPは',mikata)
        time.sleep(2)
        print()
        pt('あ。',2)
        print()
        print(dorei,'死んでた…')
        print()
        time.sleep(2)
        pt('能勢に倒されてしまったのだ...',2)
        print()
        pt('やはり能勢には勝てないのだ',2)
        print()
        pt('これからは能勢に従って生きていこう',2)
        display(Image(url12))
        print("........fin")
        
        break
    elif nose > 0 and mikata > 0:
        while True:
            pt('能勢のターン',2)
            pt('能勢の攻撃!!!!',2)
            noselist = [5,6,7]
            nosekougeki = random.choice(noselist)
            if nosekougeki ==5:
                display(Image(url8))
                pt('「能勢の咆哮!!!」',2)
                print(dorei,'は100のダメージを受けた...')
                time.sleep(2)
                mikata = mikata-100
                print(dorei,'の残りHP:',mikata)
                time.sleep(2)
                if mikata <= 0 :break
            elif nosekougeki ==6:
                display(Image(url9))
                pt('「能勢のつぶらな瞳!!!!」',2)
                print(dorei,'は50のダメージを受けた...')
                time.sleep(2)
                mikata =mikata-50
                print(dorei,'の残りHP：',mikata)
                time.sleep(2)
                if mikata <= 0:break
            elif nosekougeki ==7:
                pt('「能勢の頭突き!!!」',2)
                pt('...',2)
                display(Image(url10))
                pt('技の直前に眼鏡を外すことができた。',2)
                pt('能勢は視力を失い攻撃を繰り出せなかった。',2)
                
            
            print(syuzinkou,'のターン')
            time.sleep(2)
            pt('さあ、どうする？',2)
            sentaku = int(input('''
                         1,殴る　　　2,蹴る
                         3,必殺技　'''))
            if sentaku == 1:
                nagurilist = [20,23,35,4]
                naguri = random.choice(nagurilist)
                display(Image(url14))
                time.sleep(2)
                print(dorei,'は',naguri,'のダメージを与えた')
                time.sleep(2)
                nose = nose-naguri
                print('能勢の残りHP：',nose)
                time.sleep(2)
                break
            elif sentaku == 2:
                kerulist = [40,45,74,1,0]
                keru = random.choice(kerulist)
                display(Image(url13))
                time.sleep(2)
                print(dorei,'は',keru,'のダメージを与えた')
                time.sleep(2)
                nose = nose-keru
                print('能勢の残りHP:',nose)
                time.sleep(2)
                break
            elif sentaku == 3:
                if answer3 == 1:
                    pt('おおっと、ここで空中土下座が繰り出された',2)
                    display(Image(url6))
                    print(dorei,'は170のダメージを与えた')
                    time.sleep(2)
                    nose = nose-170
                    print('能勢の残りHP:',nose)
                    time.sleep(2)
                    break 
                elif answer3 == 2:
                    pt('おおっと、ここでシーチーシーブーが繰り出された',2)
                    display(Image(url7))
                    print(dorei,'は185のダメージを与えた')
                    time.sleep(2)
                    nose = nose-185
                    print('能勢の残りHP:',nose)
                    time.sleep(2)
                    break
                elif answer3 == 3:
                    pt('おおっと、ここでイケメンのまなざし（ゴリゴリ）が繰り出された',2)
                    display(Image(url5))
                    pt('能勢が髪の毛で身長を4cmくらい盛っているのを見破った',3)
                    print(dorei,'は189のダメージを与えた')
                    time.sleep(2)
                    nose = nose-189
                    print('能勢の残りHP:',nose)
                    break
            else:
                print('ちゃんと選んでよー‼')
                time.sleep(2)
                