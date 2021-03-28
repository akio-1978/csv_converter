# csv_converter
※書きかけです

csvファイルを読み込んで、jinja2テンプレートを使って変換するコマンドラインツールです。
特徴として、以下の機能を盛り込んでいます。

* csvファイルに含まれる内容だけでない、任意の文字列をオプションとして追加できる。
* jinja2テンプレートだけでは変換しづらい部分をpythonのコードで直接変換できる。
  * クラスのオーバーライドが必要にはなりますが。
* 素のjinja2が持っていない「ソートを伴わないgroupbyフィルタ」を追加している。
  * `uniq`コマンドみたいな動作をします。
  * これにより、csvファイル中の「行の出現順」を意識しながらgroupをまとめていくことができます。
  
## 使用例
東京メトロ有楽町線の駅を所在地の市区ごとに分類したYAMLに変換する例です。
### 変換元ファイル
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
### テンプレートファイル
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
### コマンド
ちゃんとしたコマンドの形式にするのはこの後のバージョンの予定です。
``` sh
python -m csv_converter.convert -H -O ./result.yml  ./templates/options.tmpl
```
### 変換結果
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