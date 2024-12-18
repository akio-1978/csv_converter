[トップへ戻る](../README.md)

# toj2 チュートリアル csv ファイルの変換

toj2を使った csv ファイルの変換処理の例を挙げます。このチュートリアルは**jinja2 テンプレートの書き方については理解していることを前提としています。**

## 変換の内容

テストデータとして、東京の地下鉄のひとつ「東京メトロ有楽町線」の駅を始発の和光市駅から、途中の護国寺駅まで列挙した csv ファイルを用意しました（お近くでない方はイメージしづらくてすみません）。

このファイルを、「始発駅から順に各駅が所属する自治体毎にグループ化」した yaml のファイルに変換してみます。
始発の和光市駅から護国寺駅までの 12 駅を順番に並べた csv ファイル`yurakucho.csv`を jinja2 テンプレート`area_group.tmpl`を使って整形してみます。

### csv ファイル yurakucho.csv

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

### jinja2 テンプレート area_group.tmpl

グループ化と変換を行う jinja2 テンプレートファイル`area_group.tmpl`です。

```jinja2
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

これらを使って、以下のコマンドを実行します。

```sh
toj2 csv --header area_group.tmpl yurakucho.csv --out area_group.yml --parameters line=東京メトロ有楽町線
```
<details>
<summary>引数の意味はこちら（折り畳み）</summary>

#### 引数の意味
ここで指定した引数に付いて説明します。詳細は[README](../README.md)も参照してください。
- csv 変換するデータ種別をcsvファイルに指定します。指定必須です。
- --header csvファイルの先頭行 `number,name,area` をjinja2テンプレートの引数名として使用する。
  - 指定しない場合、先頭行もデータとして扱います。
- --out area_group.yml 変換結果を area_group.yml に出力します。
  - 指定しない場合は`sys.stdout`に出力します。
- --parameter テンプレートにパラメータを渡します。テンプレート内でパラメータ`line`から`東京メトロ有楽町線`の値を取得できるようになります。
</details>

### jinja2の実行
toj2はcsvファイルの内容を読み込み、各行とカラムの内容を持った以下の形式の`dict`を生成します。
カラム名のリスト`cols`やコマンドから渡されたパラメータ`params`から構成された`dict`がjinja2への引数として渡されます。
```python
{
    'cols' : ['number','name','area'], # csvカラム名のリスト
    'rows' : [                         # csvの各行の内容を含んだリスト

        {                              # csvの行
            'number' : 'Y-1',
            'name' : '和光市',
            'area' : '埼玉県和光市'
        }

    ],
    'params' : {                       # コマンド引数 --parameters で渡された値
        'line' : '東京メトロ有楽町線'
    }
}
```

### 変換結果

変換結果`area_group.yml`が以下の内容で作成されるはずです。

```yml
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

しかし、このYAMLは和光市の下に護国寺が来ていて、「始発駅から順に並べる」という条件を満たしていません。

### カスタムフィルター

`area_group.yml`が「始発駅から順に並べる」という条件を満たしていないのは、jinja2のgroupbyがグループの集約と同時にソートを行う仕様になっているからです。

csv ファイルはいろいろな使い方をされるので、「行の出現順が意味を持っている」ケースがあります。

この問題に対処するため、toj2 では`sequential_groupby`フィルタを用意しています。このフィルタは単にソートを行わないまま groupby を行います。
以下のように、テンプレートで sequential_groupby フィルタを使用します。

```jinja2
{{params.line}}:
  自治体別分類:
{%- for area, stations in rows | sequential_groupby('area') %}
    - {{area}}:
{%- for station in stations %}
      - {{station.line}}-{{station.number}}: {{station.name}}
{%- endfor %}
{%- endfor %}
```

すると、ソートを行わなずにグループ化された yaml データが得られます。

```yml
東京メトロ有楽町線:
  自治体別分類:
    - 埼玉県和光市:
        - Y-1: 和光市
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
    - 文京区:
        - Y-12: 護国寺
```

このように、toj2 では csv ファイルのような、取り扱うファイルの形式、データの意図に対応したカスタムフィルタも追加していきます。
フィルタの適用で対応しきれないようなケースでは jinja2 テンプレートそのものの機能で対応できます。toj2 は jinja2 への入力内容を整理すためのプログラムです。

toj2 による csv ファイルの取扱いに関する説明は以上です。
