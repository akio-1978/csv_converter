# toj2
ドキュメントは作成中ですが、動作可能なものができたので一度リリースします。

## 一言でいうとこれは何？
csvやexcelをjinja2で処理できるツールです。

## 使用例
### csvファイルを変換する例
オプションの解説も一緒に書いてあります。
[csvファイルをjinja2で変換してみる](./csv/tutorial.md)

## 動作条件
#### pythonバージョン
たぶんpython3.8 以上で動きます（開発を始めた時点では3.8を使ってました）。
#### インストール
PyPIには上げないので、このリポジトリから直接取得してください。
```sh
pip install git+https://github.com/akio-1978/toj2
```
#### 依存性
jinja2とopenpyxlを使用しています。

## 共通コマンド引数
どのデータ種別を扱うときでも共通して使用する引数の解説です。
変換対象によっては共通より拡張されていることがあります。詳しくは各変換仕様を参照願います（主にExcel）。

### 位置引数
記述位置で意味が決まる引数です。
位置引数だけ指定してtoj2を実行すると以下のようなイメージになります。[^out-option]

```sh
toj2 csv demo.tmpl demo.csv
```

#### 処理データ種別
指定必須です。以下のいずれかから処理対象のファイルを指定します。
- csv
- excel
- json

値がexcelの場合は位置引数にも変化があるので、[excel変換仕様](./excel/tutorial.md)を確認してください。

#### jinja2テンプレートファイル
指定必須です。実行されるjinja2テンプレートファイルを指定します。
**jinja2のFileSystemLoaderにはこのファイルが配置されたディレクトリが指定されます。** ここを基準に他のテンプレートのinclude等が行えます。

#### 変換対象ファイル
変換元として読み込むファイルを指定します。省略した場合、`sys.stdin`からの読込みになります。

### オプション引数
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


### Excelファイルの処理
**Excel変換の解説を記述次第この記述は移動します。**
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
[^out-option]: この例だと変換結果は`sys.stdout`に出力されます。`sys.stdin`からの入力と`sys.stdout`への出力を両方可能にするために出力先`--out`はオプションになっています。
