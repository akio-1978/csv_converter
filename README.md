# j2shrine
pythonのテンプレートjinja2を使用して、任意のテキストのレンダリングを行うプログラムです。

## 同じようなプログラムは既に存在しますが？
* j2shrineは他のプログラムがサポートしない**csvファイルのレンダリング**をサポートします。
  * json/yaml等よくあるファイル形式もサポートします。
* レンダリングの前処理のためのカスタマイズ性を重視しています。

このreadmeは当面日本語のみで書きます。

  
## 動作イメージ
駅に関するデータを並べたcsvファイルを、所在地ごとにグルーピングしたyamlに変換します。
### ソースcsvファイル
csvファイルには、東京メトロ有楽町線に関する以下のデータが含まれます。
* 路線コード
  * 有楽町線は全て"Y"です。
* 駅番号
* 駅名
* 駅の所在する自治体
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
### 適用するテンプレート
j2shrineを使って、csvファイルに以下のテンプレートを適用します。
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
### 変換結果
自治体ごとにグルーピングされたyamlが出力されます
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
## コマンド
``` sh
j2shrine format template [source] [-h] [-o file] [--input-encoding enc] [--output-encoding enc] [-p [PARAMETERS ...]] [-H] [-d] [-s] 

  format                入力ファイルのフォーマットを指定します(csv|json|yaml)
  template              レンダリングに使用するテンプレート
  source                レンダリングするファイル、省略時はsys.stdinから読み込みます

optional arguments:
  -h, --help            show this help message and exit
  -o file, --out file   output file.
  --input-encoding enc  source encoding.
  --output-encoding enc
                        output encoding.
  -p [PARAMETERS ...], --parameters [PARAMETERS ...]
                        additional values [KEY=VALUE] format.
  -H, --header          use first line is header.
  -d , --delimiter      values delimiter.
  -s , --skip-lines     skip first n lines.
 ```
