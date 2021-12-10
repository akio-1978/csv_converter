[トップへ戻る](../README.md)
# チュートリアル csvファイル処理の例
csvサブコマンドを使ったcsvファイルの変換処理の例です。

## 前提
このチュートリアルの読者は**jinja2テンプレートの記述方法を充分理解していることが前提です。j2shrineによってcsvファイルをjinja2で処理する部分のみについて解説します。

## 変換の内容
東京メトロ有楽町線の駅を列挙したcsvファイルを、各駅を自治体毎に分類したyamlのファイルにしてみましょう。
### 変換の流れ 
起点の和光市駅から護国寺駅までの12駅を順番に並べたcsvファイルを作成しました。
この`yurakucho.csv`をjinja2テンプレート`area_group.tmpl`を使って整形してみます。

### csvファイル yurakucho.csv

``` 
number,name,area
Y-1,和光市,埼玉県和光市
Y-2,地下鉄成増,板橋区
Y-3,地下鉄赤塚,練馬区
Y-4,平和台,練馬区
Y-5,氷川台,練馬区
Y-6,小竹向原,練馬区
Y-7,千川,豊島区
Y-8,要町,豊島区
Y-9,池袋,豊島区
Y-11,東池袋,豊島区
Y-12,護国寺,文京区
```

### jinja2テンプレート area_group.tmpl

``` jinja2
{{params.line}}:
  自治体別分類:
{%- for area, stations in rows | groupby('area') %}
    - {{area}}: 
{%- for station in stations %}
      - {{station.line}}-{{station.number}}: {{station.name}}
{%- endfor %}
{%- endfor %}
```

### 変換コマンド実行
以下のコマンドを実行します。

``` sh
j2shrine csv -H area_group.tmpl yurakucho.csv -o area_group.yml -p line=東京メトロ有楽町線
```
### 変換結果
うまくいけば、変換結果`area_group.yml`が以下の内容で作成されているはずです。

``` yml
東京メトロ有楽町線:
  自治体別分類:
    - 埼玉県和光市:
      - Y-1: 和光市
    - 文京区:
      - Y-12: 護国寺
    - 板橋区:
      - Y-2: 地下鉄成増
    - 練馬区:
      - Y-3: 地下鉄赤塚
      - Y-4: 平和台
      - Y-5: 氷川台
      - Y-6: 小竹向原
    - 豊島区:
      - Y-7: 千川
      - Y-8: 要町
      - Y-9: 池袋
      - Y-11: 東池袋
```

### jinja2へ渡される引数
csvファイルの中身は以下のようなdictに変換してjinja2へ渡しています。

このdictをjinja2テンプレートでレンダリングすれば、csvファイルを任意の形式に変換す
ることができます。

``` python
{
    'headers' : ['number','name','area'], 
    'rows' : [
        {
            'number' : 'Y-1',
            'name' : '和光市',
            'area' : '埼玉県和光市'
        },
        # 以下護国寺まで12駅分続く
    ], 
    'params' : [
        {
            'line' : '東京メトロ有楽町線'
        }
    ]
}
```
基本的な使い方はこれだけです！
