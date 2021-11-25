[トップへ戻る](../README.md)
# csvファイル処理の例
csvサブコマンドを使ったcsvファイルの変換処理の例です。

## 変換の内容
東京メトロ有楽町線の駅を自治体毎に分類したyamlのファイルにしてみます。
### 変換前データ

``` csv
pref,name,age
群馬県,浅利 靖,6
福岡県,千田 沙和,48
京都府,宮尾 唯衣,32
茨城県,野尻 友治,53
新潟県,水本 智之,51
新潟県,千野 克哉,41
愛媛県,磯田 碧依,21
神奈川県,徳丸 晶,68
神奈川県,桜木 富美子,46
茨城県,新田 芳太郎,33
```

``` jinja2
人名リスト:
{%- for pref, persons in lines | sequential_group_by('pref') %}
    - {{ward}}: 
{%- for station in stations %}
      - {{station.line}}-{{station.number}}: {{station.name}}
{%- endfor %}
{%- endfor %}
```
