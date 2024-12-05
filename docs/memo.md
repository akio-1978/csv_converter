# デモります！
CSVファイルをjinja2テンプレートで変換するプログラムのドキュメントがなかなか書き上がらないのでデモります。
## いまから何をやるの？
CSVデータの行を分類してjsonに変換します。高機能な変換を行うためにjinja2を使います。
### 変換するCSVデータ
以下のcsvはとある学校の、クラスごとに分類した学生の名簿です。これをクラスごとに分類したjsonにします。
csvのカラムは"クラス,氏名,その他"です（その他カラムは使いません）。データはクラス順にソートされていません。
```csv:demo.csv
1,佐藤 はじめ,xxxxxx
2,斎藤 かな,xxxxxx
3,清田 浩一,xxxxxx
2,小林 裕太,zzzzzz
```
### jinja2テンプレートを用意
このcsvファイルを整形するために以下のjinja2テンプレートを使用します。
```jinja2:demo.tmpl
{
    {%- for class_no, students in rows | groupby('col_00')%}
    "{{class_no}}組" : [
    {% for student in students %}
        "{{student.col_01}}"{% if not loop.last %},{% endif -%}
    {% endfor %}
    ]{% if not loop.last %},{% endif %}{% endfor %}
}
```
### コマンド実行
ではコマンドを実行して変換します！
```sh
toj2 csv demo.tmpl demo.csv -o result.json
```
### 実行結果
```json:result.json
{
    "1組" : [
    
        "佐藤 はじめ"
    ],
    "2組" : [
    
        "斎藤 かな",
        "小林 裕太"
    ],
    "3組" : [
    
        "清田 浩一"
    ]
}
```
生徒がクラスごとに分類されましたね！
jinja2をフルに使えるので必要に応じて様々な加工を行うことができます。

## これだけじゃないんだ！
これだけでも、CSVをjinja2で処理するのはちょっと珍しい試みです。
でも本当はCSVだけじゃなくて**Excelもjinja2で処理できるようになってます！**
あと少しドキュメント書いたらリリースしたいなぁと思ってます。乞うご期待・・・
