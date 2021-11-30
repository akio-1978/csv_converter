[トップへ戻る](../README.md)
# csvファイル処理の例
csvサブコマンドを使ったcsvファイルの変換処理の例です。

## 変換の内容
東京メトロ有楽町線の駅を列挙したcsvファイルを、各駅を自治体毎に分類したyamlのファイルにしてみましょう。
### 変換前データ
全駅は長いので、和光市駅から護国寺駅までの12駅を並べてcsvファイルを作成しました。

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

### テンプレート
このテンプレートを使って、自治体ごとに分類したYAMLを生成します。

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
