# j2shrine
* j2shrineはjinja2をコマンドラインで実行するツールです。
* データを読み込んで、内容を引数としてjinja2を実行します。
* 入力データとしてcsvやExcelを扱えることが特徴です。
  * version0.1.0現在ではcsv、Excel、jsonの3つの形式に対応しています。

## 動作環境
python3.8 以上

## インストール
``` sh
pip install j2shrine-0.1.0-py3-none-any.whl
```

## コマンド使用方法

### 実行例
data.csvにテンプレートtemplate.j2を適用して、formatted.txtを得る例です。
```
j2shrine csv template.j2 data.csv -O formatted.txt
```

### コマンド構文
コマンドの基本的な構文は以下の形になっています。
```
j2shrine [入力フォーマット] [入力フォーマット固有の引数] [オプション]
```
オプションは全入力フォーマットに共通するものと、特定の入力フォーマットに固有のものがあります。

### 入力フォーマット
以下の3種類から指定します。
* csv
  * 入力をcsvフォーマットとして解釈します
  * csvファイルの解釈にはpythonのcsvモジュールを使用します
* excel
  * 入力をExcelファイルとして解釈します
  * Excelの解釈にはopenpyxlを使用します
* json
  * 入力をjsonとして解釈します
  * jsonの解釈にはpythonのjsonモジュールを使用します

### 共通のオプション 
全入力フォーマットに共通するオプションです。
* -O [file] --output [file]
  * jinja2の処理結果の出力先、省略時はstdoutへ出力します
* --input-encoding [encoding]
  * 入力データのエンコーディング、デフォルトはutf8です
* --output-encoding [encoding]
  * 出力データのエンコーディング、デフォルトはutf8です
* -p [PARAMETERS ...] --parameters [PARAMETERS ...]
  * テンプレート内で使用する変数を定義します
  * 変数を`[KEY]=[VALUE]`の形で定義すると、定義された値はjinja2から変数KEYとして呼び出せます
  * KEYとVALUEの間にはスペースを挟まないでください
  * このパラメータはいくつでも定義できます

### 固有の入力フォーマット
入力フォーマット毎に異なる引数を解説します。

#### CSVフォーマット
CSVフォーマットの処理は以下の構文で指定します。
``` sh
j2shrine csv [template] [source] options...
```
##### 位置引数
CSVフォーマットで使用する位置引数です。
* template（必須）
  * j2shrineが読み込んだcsvデータを処理するための、jinja2テンプレートを指定します
* source（任意）
  * csvデータを読み込むファイルを指定します。指定しない場合、stdinからの入力を受け付けます

##### オプション引数
CSVフォーマットに固有のオプション引数です。
* -H --header
  * csvデータの先頭行をヘッダとして認識します
  * ヘッダ行は各行のカラムの変数名として使用されます
  * ヘッダの指定を省略した場合、各カラムは`col00, col01, col02...`の連番で命名されます
* -s n --skip-lines n
  * csvデータの先頭n行を読み飛ばします
  * -Hオプションと同時にしていされた場合、読み飛ばし後の最初の行をヘッダとして認識します
* -d delimiter --delimiter delimiter
  * カラムを区切るデリミターを指定します、デフォルトは','です

この他に共通のオプションを指定することができます。

##### csvからjinja2へ渡されるパラメータ
csvを読み込んだ結果、j2shrineは以下のパラメータを渡してjinja2を起動します。
``` python
{
    'rows' : result, # csvの各行をdictで格納したlistです
    'headers' : self.headers, # csvの各行のカラム名に使用されたヘッダ名のlistです
    'params' : self.context.parameters # 起動時にオプション--parametersで指定された変数が格納されます
}
```

##### カスタムフィルター
csvを処理するために使用するカスタムフィルターが定義されています。
* sequential_group_by
  * 行を出現順にグループ化します
  * jinja2のフィルターgroup_byはgroup化の前にソートを行うため、csvを扱う場合には「行の出現順」が失われてしまうため、不向きなことがあります。
  * jinja2のgroup_byの動作 `A A B B A C` -> `A B C`
  * sequential_group_byの動作 `A A B B A C` -> `A B A C`
  