# toj2
ドキュメントは作成中ですが、動作可能なものができたので一度リリースします。


## 一言でいうとこれは何？
csvやexcelをjinja2で処理できるツールです。


## 動作条件
#### pythonバージョン
たぶんpython3.8 以上で動きます。開発を始めた時点では3.8をっていたので。
#### 依存性
jinja2とopenpyxlを使用しています。
#### インストール
PyPIには上げないので、このリポジトリから直接取得してください。
```sh
pip install git+https://github.com/akio-1978/toj2
```

## 使い方デモ
実際にtoj2を使用してCSVファイルを変換するデモです。
デモで使用するデータとテンプレートはdocs/samplesディレクトリに置いてあります。

<details>
<summary>デモ内容（折り畳み）</summary>

#### デモのシナリオとデータ
以下のcsvはとある学校の1年生をクラスごとに分類した学生の名簿です。名簿と言っても
`出席番号,氏名,部活`で列挙しただけのテキストファイルですが、今回はこの名簿内の生徒達を所属する部活ごとに分類して、結果をHTML化します。

```csv:demo.csv
1,佐藤 はじめ,サッカー部
2,斎藤 かな,陸上部
3,清田 浩一,陸上部
4,小林 裕太,サッカー部
5,宮田 敦,サッカー部
6,久米 ひろ子,茶道部
```
#### janja2テンプレート
このcsvファイルを整形するためのjinja2テンプレートを作成します。デモ用なのでHTMLとしてはいい加減な形式です。


```jinja2:demo.tmpl
<html>
<head><title>部活別生徒リスト</title></head>
<body>
<ul>
{%- for club_name, students in rows | groupby('col_02')%}
    <li>{{club_name}}
        <ul>
            {%- for student in students %}
            <li>{{student.col_01}}</li>
            {%- endfor %}
        </ul>
    </li>
    {%- endfor %}
</ul>
</body></html>
```


#### 実行
toj2コマンドを実行します。
```sh
toj2 csv demo.tmpl demo.csv --out result.html
```
#### 実行結果
生徒を所属する部活ごとにまとめたHTMLが生成されます。

```html
<html>
<head><title>部活別生徒リスト</title></head>
<body>
<ul>
    <li>サッカー部
        <ul>
            <li>佐藤 はじめ</li>
            <li>小林 裕太</li>
            <li>宮田 敦</li>
        </ul>
    </li>
    <li>茶道部
        <ul>
            <li>久米 ひろ子</li>
        </ul>
    </li>
    <li>陸上部
        <ul>
            <li>斎藤 かな</li>
            <li>清田 浩一</li>
        </ul>
    </li>
</ul>
</body></html>
```
</details>

toj2はこれだけのツールですが、jinja2のおかげで色々なことができます。
また、同様のツールでcsvファイルが扱えるツールは少なくて、excelまでサポートしているのが強みですが、**肝心のExcelファイル変換については、現在急いでドキュメントを作成中です。**

---

## コマンド引数
toj2では他のコマンドラインツールと同じように位置引数とオプション引数を取りますが、処理対象のファイルによってオプション引数以外に位置引数も変動します。
実際の実行イメージは各ファイルごとの引数解説のところで載せています。

### 共通位置引数
全データ形式に共通する位置引数およびオプションについて解説します。

#### 処理データ種別
処理対象のファイルを指定します。以下のいずれかです。
- csv
- excel
- json
この引数によって、この引数より後ろの位置引数とオプション引数に変化があります。

#### jinja2テンプレートファイル
変換に使うjinja2テンプレートです。このテンプレートが配置された場所を起点として、他のテンプレートをincludeすることにも使えます。

#### 変換対象ファイル
変換元として読み込むファイルを指定します。省略した場合、`sys.stdin`からの読込みになります。**excelではファイル名は省略不可です。**

### 共通オプション引数
すべてのデータ形式で設定可能なオプション引数です。

#### 出力ファイル
`-o output_file` または `--out output_file`

変換結果を出力するファイルを指定します。省略された場合、`sys.stdout`に出力されます。

#### 文字列エンコーディング

`--input-encoding enc`
`--output-encoding enc`

入出力ファイルのエンコーディングを指定します。デフォルトはUTF8です。**excelでは`--input-encoding`は無視されます。**

#### テンプレートパラメータ
jinja2テンプレートに任意の値を渡すことができます。値は`=`でキーと値に区切って指定します。指定できる数に制限はありません。

`--parameter PARAM1=A PARAM2=B `

この値は、テンプレート中で`param['PARAM1']`のようにして参照できます。

---

### CSVファイルの処理
CSVファイルを処理する際の動作と、コマンドラインオプションについて説明します。

#### コマンド実行イメージ
```sh
toj2 csv csvtemplate.tmpl data.csv --out result.txt
```

#### jinja2への出力形式
toj2はCSVファイルの各行を読み込み、以下の形式にして`jinja2.render`に渡します。`jinja2.render`が返した文字列がtoj2の戻り値になります。
```python
{
    # 読み取った行の値のdictが入ったlist
    'rows': [dict, dict, dict...],
    # 読み取ったカラム名が入ったlist
    'cols': ['name1', 'name2', 'name3', ...],
    # 起動時に渡したパラメータ
    'params' : {'PARAM' : 'VALUE'}
}
```
### CSVファイル処理オプション
CSVファイル処理の際に指定可能なオプションです。
#### デリミタ
ファイルがタブ文字などカンマ以外で区切られている場合、任意の文字を指定できます。タブ区切りの場合は以下のように指定します。

`--delimiter "\t"`

#### ヘッダ
1行目をヘッダ名として項目名に使用します。

`--header`

#### 行スキップ
先頭から指定の行数を読み飛ばします。ヘッダのあるCSVに対してヘッダを無視する場合`--skip-lins 1`とします。

`--skip-lins 1`

#### カラム名指定
jinja2テンプレートが受け取るカラムの名前を指定します。省略された場合、カラム名は左から順に`col_00, col_01...`と連番で自動生成されます。

`--names a b c`

この場合カラム名は`a, b, c`となり、3カラムを超える場合は`col_03, col_04`と自動生成されます。

---

### Excelファイルの処理
Excelファイルを処理する際の動作及びコマンドオプションについて説明します。

#### コマンド実行イメージ
excelでは処理対象のシート及びセルの指定などが含まれるため、引数が多くなります。

```sh
toj2 excel exceltemplate.tmpl data.xlsx 1 A1:D4 --out result.txt
```

#### jinja2への出力形式
toj2はExcelファイルをシートごとに読み込み、以下の形式にしてjinja2に渡します。
多数のシートを扱うためにCSVより複雑になっています。
```python
{
  # 各シートごとのリスト
  'sheets' : [
    {
      'name': 'sheet_name',           # シート名
      'abs': {'PARAM' : 'VALUE'},     # 指定座標セル
      'rows': [[dict,dict, dict...]], # シート内容の行と列
    }
    ...
  ]
  # 起動時に渡したパラメータ
  'params' : {'LABEL' : 'VALUE'}
}
```

### Excelファイル処理オプション
Excelファイルはオプション以外にも固有の位置引数を持ちます。
#### **読込みファイル**
必須の位置引数です。**共通ではオプションですが、excelファイルの場合は必須です。**
変換元として読み込むファイルを指定します。excelの場合は`sys.stdin`からの読込みは行えず、**必ずファイルを指定する必要があります。**
#### **シート範囲**
必須の位置引数です。
読込むシートを指定します。シートは1度に複数指定可能です。**数値は1オリジンです。**シート番号の後に`:`を付与することで、指定したシート番号に続く全てのシートを取得できます。
```
# 1枚目のシートのB2:E4を取得する
toj2 excel exceltemplate.tmpl data.xlsx 1 B2:E4 -o result.txt
# 3枚目のシートのB2:E4を取得する
toj2 excel exceltemplate.tmpl data.xlsx 3 B2:E4 -o result.txt
# 1枚目の全てのシートから全てのシートのB2:E4を取得する
toj2 excel exceltemplate.tmpl data.xlsx 1: B2:E4 -o result.txt
```
#### **セル範囲指定**
必須の位置引数です。
シート内から読みだすセルの範囲を指定します。excelでは読み取ったセルの先頭からjinja2に渡すカラム名の自動生成が始まります。**指定したセル範囲がA2:E4の場合、カラム名`col_00`はB列を示します。**

以下のような書き方で、データを持つすべての行を指定することも可能です。（全ての、という範囲はopenpyxlに依存します）
```
# 1枚目のシートのB2からE列の全てのデータを読み取る
toj2 excel exceltemplate.tmpl data.xlsx 1 B2:E -o result.txt
```

#### カラム名指定
csvと似た機能オプションです。
jinja2テンプレートが受け取るカラムの名前を指定します。省略された場合、カラム名は左から順に`col_00, col_01...`と連番で自動生成されます。
ただし、excelでは取得したセル範囲から順に`--names`が適用されます。
```
# 1枚目のシートのB2:E4を取得する
toj2 excel exceltemplate.tmpl data.xlsx 1 B2:E4 --names a b c -o result.txt
```
この場合、カラム名`a`はB列のカラムに対して適用されます。

#### 指定位置セル指定

各シート内で指定したセル範囲外にある値を取得してjinja2テンプレートに任意の値を`--absolute`オプションで取得します。値は`LABEL=CELL`の形式です。

```
# セルA1とA2にある値を取得
toj2 excel exceltemplate.tmpl data.xlsx 1 B2:E --absolute LABEL=A1 -o result.txt
```
この値は、テンプレート中で`sheet.abs.A1`のようにして参照できます。

### JSON処理
JSONの処理については特に固有のオプションはありません。

```sh
toj2 json jsontemplate.tmpl data.json --out result.txt
```

#### jinja2への出力形式
toj2はjsonを以下の形式にしてjinja2に渡します。
```python
{
    # 受け取ったjson
    'data': {},
    # 起動時に渡したパラメータ
    'params' : {'PARAM' : 'VALUE'}
}

```

JSON処理については現時点では注力していません。JSON、XML、YAMLなどをjinja2で処理してくれるソフトウェアは既にあるので、信頼性の面でそちらをお勧めします。ただしサポートは継続します。