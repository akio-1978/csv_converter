# csv_converter
機械翻訳英語に少しづつ修正中当分日英併記
rewriting to english slowly. 

convert CSV format by Jinja2 Template Engine.

## Features
* convert csv any format by template.
* can specify the extra value to not included in csv by argument.
* if hard to convert by janja template only. can pre process by python.
  * require converter class override
* for keep line sequence. added unsorted group filter.(like uniq)

* テンプレートを使うことによって、csvファイルの内容を構造化した形式に変換できる
* csvファイルに含まれる内容だけでない、任意の文字列をオプションとして追加できる
* if jijna2テンプレート変換しづらい場合、pythonコードで変換の前処理ができます
  * 変換クラスのオーバーライドが必要になります
* jinja2にソートしない"group_by"フィルタを追加(`uniq`コマンドみたいな動作をします)
  
## Example
This is an example of converting stations on the Tokyo Metro Yurakucho Line into YAML classified by location.
東京メトロ有楽町線の駅を所在地の市区ごとに分類したYAMLに変換する例です。
### source csv file
``` csv
line,number,name,ward
Y,1,Wakoshi,Wako-shi
Y,2,Chikatetsu-narimasu,Itabashi-ku
Y,3,Chikatetsu-akatsuka,Nerima-ku
Y,4,Heiwadai,Nerima-ku
Y,5,Hikawadai,Nerima-ku
Y,6,Kotake-mukaihara,Nerima-ku
Y,7,Senkawa,Toshima-Ku
Y,8,Kanamecho,Toshima-Ku
Y,9,Ikebukuro,Toshima-Ku
```
### Template to use
```
stations:
  ward:
{%- for ward, stations in lines | sequential_group_by('ward') %}
    - {{ward}}: 
{%- for station in stations %}
      - {{station.line}}-{{station.number}}: {{station.name}}
{%- endfor %}
{%- endfor %}
```
### command line
``` sh
python -m csv_converter.convert -H -O [converted file]  [template to use]
```
### Conversion result
``` yml
stations:
  ward:
    - Wako-shi:
      - Y-1: Wakoshi
    - Itabashi-ku:
      - Y-2: Chikatetsu-narimasu
    - Nerima-ku:
      - Y-3: Chikatetsu-akatsuka
      - Y-4: Heiwadai
      - Y-5: Hikawadai
      - Y-6: Kotake-mukaihara
    - Toshima-Ku:
      - Y-7: Senkawa
      - Y-8: Kanamecho
      - Y-9: Ikebukuro
```
