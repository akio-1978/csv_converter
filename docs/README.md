# toj2
ドキュメントは作成中ですが、動作可能なものができたので一度リリースします。

## 一言でいうとこれは何？
csvやexcelをjinja2で処理できるツールです。

## 使用方法 使用例
ファイル変換の例を紹介します。ファイル形式に固有のオプションがある場合はこちらで解説します。
### csvファイルを変換する例
[toj2によるCSVファイル変換](./csv/tutorial.md)

### excelファイルを変換する例
[toj2によるExcelファイル変換](./excel/tutorial.md)

### jsonファイルを変換する例
[jsonについてはごくシンプルな動作のみ](JSONファイルの変換)なので、このファイル内で解説します。

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

## 実行方法
コマンドとして実行します。例えば以下のような形になります。

```sh
toj2 csv demo.tmpl demo.csv
```
引数については以下で解説します。
他に、変換するファイル形式ごとに固有のオプションを持つ場合もあります。それらは各ファイル形式のチュートリアルで解説します。

## 共通コマンド引数
全てのファイル形式に対して共通で使用する引数です。[^except-excel]

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

#### --out 出力ファイル
`-o output_file` または `--out output_file`

変換結果を出力するファイルを指定します。省略された場合、`sys.stdout`に出力されます。

#### --input-encoding --output-encoding 文字列エンコーディング

`--input-encoding enc`
`--output-encoding enc`

入出力ファイルのエンコーディングを指定します。デフォルトはUTF8です。**excelでは`--input-encoding`は無視されます。**

#### --parameter テンプレートパラメータ
jinja2テンプレートに任意の値を渡すことができます。値は`=`でキーと値に区切って指定します。指定できる数に制限はありません。

`--parameter PARAM1=A PARAM2=B `

この値は、テンプレート中で`param.PARAM1`のようにして参照できます。

#### --config-file 設定ファイル
ときどき、toj2の引数が長いものになることがあります。そのような場合、オプション引数をjsonにまとめることができます。

以下のようなコマンドが少し長いと感じるでしょう（以下はcsv変換用のオプションを含みます）。

```sh
toj2 csv sample.tmpl sample.csv --skip-lines 1 --out result.txt  --names one two three four --parameters PARAM1=A PARAM2=B PARAM3=C
```

このオプションを以下のような`config.json`としてまとめて記述します。設定ファイル内ではオプション名の先頭のふたつのハイフンは除去し、途中に現れるハイフンはアンダースコアに置き換えます。

```json
{
  "skip_lines": 1,
  "names": ["one", "two", "three", "four"],
  "parameters": {
      "PARAM1" : "A",
      "PARAM2" : "B",
      "PARAM3" : "C"
  }
}
```

そして、コマンドを以下のように実行すると、`config.json`の内容がオプションとして使用されます。
```sh
toj2 csv sample.tmpl sample.csv --config-file config.json
```

これだけではなく、**設定ファイルはコマンドラインからオーバーライドすることができます。**
```sh
toj2 csv sample.tmpl sample.csv --config-file config.json --skip-lines 0 --parameters PARAM1=X PARAM4=D
```
設定ファイル中の`skip-lines`は`1`ですが、ここでは`0`に置き換わります。

`--parameters`オプションのうち、パラメータ`PARAM1`の値は`X`に変更され、新たに`PARAM4`が追加されますが**`PARAM2`と`PARAM3`は影響を受けません。**設定ファイル内で値またはリストで記述するものは置き換えられ、オブジェクトで記述されるものはマージされます。**常にコマンドラインからの設定が優先して採用されます。

### JSONファイルの変換
JSONの処理については特に固有のオプションはなく、共通オプションのみが使用できます。

```sh
toj2 json jsontemplate.tmpl data.json
```

#### jinja2への出力形式
toj2はjsonを以下の形式にしてjinja2に渡します。
```python
{
    # 受け取ったjsonをjson.loadした結果
    'data': {},
    # 起動時に渡したパラメータ
    'params' : {'PARAM' : 'VALUE'}
}

```
JSONに関しては、toj2は単純にjinja2へのデータの中継を行うだけです。

[^out-option]: この例だと変換結果は`sys.stdout`に出力されます。`sys.stdin`からの入力と`sys.stdout`への出力を両方可能にするために出力先`--out`はオプションになっています。
[^except-excel]: Excel変換だけは位置引数から違っていたりして共通性がないのですが、それはExcel用の引数解説で解説します。
