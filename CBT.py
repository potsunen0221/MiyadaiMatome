#!/usr/bin/env python
# coding: utf-8

import argparse as arg
import codecs
import json
import os
import random
import re
import sys

class pyKBCT:
    
    def __init__ (self, questions_data, miss=False):
        self.source = self.load(questions_data)
        self.path = questions_data
        self.miss = miss
        self.multi_list = {
            1:[[True,False,False,False,False],[False,True,False,False,False],[False,False,True,False,False],[False,False,False,True,False],[False,False,False,False,True]],
            2:[[True,True,False,False,False],[True,False,False,False,True],[False,True,True,False,False],[False,False,True,True,False],[False,False,False,True,True]],
            3:[[True,True,True,False,False],[True,False,True,False,True],[True,False,False,True,True],[False,True,True,True,False],[False,True,False,True,True]]
        }
        self.yn = {'y':True,'yes':True,'n':False,'no':False}
    
    def load(self, path):
        print('\n獣医国家試験の過去問をロードしています...')
        with open(path) as f:
            source = json.load(f)
        print('ロードが完了しました!')
        return source
    
    def save(self, path, history):
        print('\n回答履歴をセーブ中です。プログラムを終了させないでください。')
        with codecs.open(path, 'w', 'utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=0)
        print('セーブが完了しました!')
    
    def initialize(self):
        print('\nこれまでの回答履歴を削除しますか?')
        while True:
                delete = self.yn.get(input('[Y]es/[N]o? >> ').lower(), -1)
                if type(delete) is bool:
                    break
                print('エラー! もう一度入力してください。')
        if delete:
            try:
                for i in self.source:
                    i['solved'] = 0
                    i['miss'] = 0
                    i['rate'] = 0
                self.save(self.path, self.source)
            except:
                pass
        else:
            pass
        
    def myConditions(self, source):
        print('\n設定を行います。')
        
        set_condition = False
        while set_condition is not True:
            print('\n以下から解きたい回次を選んで半角英数で入力してください。(すべて選ぶ場合は入力なし。複数の場合は半角スペース区切り。)')
            years = sorted(list(set([i['year'] for i in source])))
            print("~"*(3*int(len(years)/2)-5),"回次リスト","~"*(3*int(len(years)/2)-5),sep="")
            print(*years)
            print("~"*3*len(years))
            select_year =  [int(x) for x in input().split()]
            if select_year: questions = [i for i in source if i['year'] in select_year]
            else: questions = source

            print('\n以下から解きたい問題区分を選んで半角英数で入力してください。(すべて選ぶ場合は入力なし。複数の場合は半角スペース区切り。)')
            print('~~~~~~区分リスト~~~~~~')
            print('必須問題 → "H"')
            print('学説試験問題(A) → "A"')
            print('学説試験問題(B) → "B"')
            print('~~~~~~~~~~~~~~~~~~~~~')
            select_category = input().upper().split()
            if select_category: questions = [i for i in questions if i['category'] in select_category]

            print('\n以下から解きたい分野を選んでコピペで入力してください。(すべて選ぶ場合は入力なし。複数の場合は半角スペース区切り。)')
            print('~~~~~~~~~~~~~~~~~~分野リスト~~~~~~~~~~~~~~~~~~')
            print('解剖組織 生理生化 薬理毒性 実験動物 法規倫理 放射線')
            print('病理 微生物 寄生虫 感染症 家禽疾病')
            print('魚病 動物衛生 公衆衛生')
            print('臨床繁殖 外科 内科')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            select_field = input().split()
            if select_field: questions = [i for i in questions if bool(set(i['field']) & set(select_field))]
            
            if self.miss: questions = [i for i in questions if i['rate'] <= 0.5]

            print(f'\n選んだ問題数は {len(questions)} 問です。')
            print(f'確定しますか?')
            while True:
                set_condition = self.yn.get(input('[Y]es/[N]o? >> ').lower(), -1)
                if type(set_condition) is bool:
                    break
                print('エラー! もう一度入力してください。')

        print('\n問題をランダムに出題しますか?')
        while True:
            random_set = self.yn.get(input('[Y]es/[N]o? >> ').lower(), -1)
            if type(random_set) is bool:
                break
            print('エラー! もう一度入力してください。')

        print('\n選択肢をランダムに出題しますか?')
        while True:
            shuffle_choices = self.yn.get(input('[Y]es/[N]o? >> ').lower(), -1)
            if type(shuffle_choices) is bool:
                break
            print('エラー! もう一度入力してください。')

        return questions, random_set, shuffle_choices
    
    def shuffler(self, q):
        while True:
            c_list = random.sample(q['property'],5)
            ox = [d.get('ox') for d in c_list]
            if ox in self.multi_list[q['multiple']]:
                answer = self.multi_list[q['multiple']].index(ox) + 1
                break
        return c_list, answer
    
    def main(self, miss=False):
        finish = 1
        while True:
            if finish == 1:
                questions, random_set, shuffle_choices = self.myConditions(self.source)
            incorrect = []
            num = 0
            correct = 0
            if random_set:
                qs = random.sample(questions, len(questions))
            else:
                qs = questions

            print('\n演習を開始します。')

            for q in qs:
                if shuffle_choices:
                    c_list, answer = self.shuffler(q)
                else:
                    c_list = q['property']
                    ox = [d.get('ox') for d in c_list]
                    answer = self.multi_list[q['multiple']].index(ox) + 1
                
                print(f"\n第{q['year']}回  {q['category']}問題  問{q['number']}",end="\t")
                print(f"問題正答率 : {q['rate']:.2%}\n")
                print(f"{q['question']}\n")

                if 'combination' in q:
                    print(f"{q['combination']}")

                if q['multiple'] == 1:
                    for i, c in enumerate([d.get('choice') for d in c_list],1):
                        print(f'{i}. {c}')
                else:
                    for (let, c) in zip(['a', 'b', 'c', 'd', 'e'], [d.get('choice') for d in c_list]):
                        print(f'{let}. {c}')
                    if q['multiple'] == 2:
                        print('\n1. a, b     2. a, e     3. b, c     4. c, d     5. d, e')
                    elif q['multiple'] == 3:
                        print('\n1. a, b, c     2. a, c, e     3. a, d, e     4. b, c, d     5. b, d, e')

                while True:
                    try:
                        res = int(input('\n回答 (半角数字) : '))
                    except:
                        res = -1
                    if res in [1, 2, 3, 4, 5]:
                        break
                    print('\nエラー! もう一度入力してください。')

                q['solved'] += 1
                num += 1

                if res == answer:
                    correct += 1 
                    print('\n正解です。')
                else:
                    incorrect.append(q)
                    q['miss'] += 1
                    print('\n不正解です。')
                    print(f'正解は {answer}')
                
                q['rate'] = round(1 - q['miss']/q['solved'], 4)

                print('\n【解説】')

                if 'comment' in q:
                    for com in q['comment']:
                        print(com)

                fLoop = True

                if q['multiple'] == 1:
                    for i, e in enumerate([d.get('exp') for d in c_list],1):
                        if e is not None:
                            if fLoop:
                                print('')
                                fLoop = False
                            print(f'{i}: {e}')
                else:
                    for (let, e) in zip(['a', 'b', 'c', 'd', 'e'], [d.get('exp') for d in c_list]):
                        if e is not None:
                            if fLoop:
                                print('')
                                fLoop = False
                            print(f'{let}: {e}')

                print(f'\n現在までの正答率 : {correct/num:.2%}')
                
                nextq = ''
                if num < len(questions):
                    nextq = input('\n次の問題へ ')
                if nextq == 'break':
                    break

            print('\n問題を解き終わりました。')
            print(f'{num}問中 {correct}問の正解です。\n')

            while True:
                print('\n間違えた問題を再演習する => 0')
                print('別の問題をとく => 1')
                print('演習を終える => 2')

                try:
                    finish = int(input('>>> '))
                except:
                    finish = -1

                if finish == 0:
                    questions = incorrect
                    if len(questions) != 0:
                        break
                    print('\n全問正解です。おめでとう!')
                elif finish == 1:
                    break
                elif finish == 2:
                    break
                else:
                    print('\nエラー! もう一度入力してください。')

            if finish == 2:
                break

        self.save(self.path, self.source)
        print('\nお疲れさまでした!')
        
        
if __name__ == "__main__":
    
#    dir = os.path.split(os.path.abspath(__file__))[0]
    dir = os.path.dirname(sys.executable)
    questions_data = dir + '/questions.json'
    
    print('\n宮大まとめ 3.0.5 (2022-12-11)')
    print('Copyright (C) 2019-2022 Asato Sekiya')
    print('\n宮大まとめはpythonでプログラムされた、テキストから問題抽出及び正誤判定を行うvetCBTおよび獣医師国家試験対策用のシステムです。')
    print('本システムは毎年、宮崎大学農学部獣医学科6年生によって作成される獣医師国家試験の解説集をCBTに近い形式で出力できるようにしたものです。')
    print('本システムの管理者以外による無断譲渡は固く禁止いたします。\n')
    
    print("'s'と入力すれば問題を開始します。")
    print("'e'と入力すればプログラムを終了します。")
    print("その他のオプションについては'option'と入力することで詳細を見ることができます。\n")
#     parser = arg.ArgumentParser()
#     parser.add_argument('-i', '--initialize', help='オプション：初期化', action='store_true')
#     parser.add_argument('-m', '--miss', help='オプション：正答率50%以下の問題を抽出', action='store_true')
#     parser.add_argument('questions_data', help='問題が記入されたjsonファイルのパス')
#     args = parser.parse_args()
    
    while True:
        command = input('>>> ')
        if command == 'option':
            print("正答率が低い問題のみを解く => 'm'")
            print("回答履歴を初期化する => 'i'")
            print("その他のオプションについては考え中です。")
        elif command in ['s','e','m','i']:
            break
        else:
            print('エラー! もう一度入力してください。')
    
    if command == 'i':
        kbct = pyKBCT(questions_data)
        kbct.initialize()
    elif command == 's':
        kbct = pyKBCT(questions_data)
        kbct.main()
    elif command == 'm':
        kbct = pyKBCT(questions_data,True)
        kbct.main()
    elif command == 'e':
        pass
