# 宮大まとめ

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

宮大まとめはpythonでプログラムされた、問題抽出と正誤判定を行うvetCBT/獣医師国家試験対策用のシステムです。  
本システムは毎年、宮崎大学農学部獣医学科6年生によって作成される獣医師国家試験の解説集をCBTに近い形式で出力できるようにしたものです。  
現在、exe化して環境構築(python3の導入)なしで実行できるように調整中です。
 
## DEMO

準備中です。

## Features

- CBT形式で獣医師国家試験の必須問題、A問題、B問題を受けられます。
- 回答の正誤判定、解説を一問ごとに行います。
- 間違えた問題をやり直すことが出来ます。
- セーブ機能があるので、過去に間違えたことのある問題、正答率の低い問題を選択的に出題できます。
- 問題および選択肢のランダム出力に対応しているので、選択肢で正答を覚えることを防ぎます。

## Requirement

- python(3.8.1)  
- 問題と解答、解説を含むjson形式のテキストファイルを別途ダウンロードする必要があります。  
  ダウンロードフォームは別途作成中です。  
  現在は[サンプル](test.json)として第60回獣医師国家試験の一部を用意しています。

## Usage

MiyadaiMatomeフォルダをダウンロードし、pythonで実行してください。
```sh
$ python3 /Users/hoge/Desktop/MiyadaiMatome/CBT.py # hoge内にはユーザー名
```

# Author
 
* 作成者  
関谷 麻杜
* 所属  
宮崎大学医学獣医学総合研究科
* E-mail  
asat.myz.vet[at]gmail.com
  ([at]→@)
