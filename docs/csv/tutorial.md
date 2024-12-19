[トップへ](../README.md)
# CSVファイル変換
toj2のCSVファイル変換機能についての解説です。

## 解っている人はこちら

[既に機能を理解している人はこちら](#csv変換固有のコマンドオプション)でコマンド引数を参照できます。

## 変換デモ
まず実際に変換するデモをやります。
デモで使用するデータとテンプレートはdocs/csv/samplesディレクトリに置いてあります。

#### デモのシナリオとデータ
以下のcsvファイルはとある学校の生徒を`出席番号,氏名,部活`で列挙しただけのファイルです。
このファイルに含まれる生徒達を所属する部活ごとに分類して、結果をHTML化します。

```csv:demo.csv
1,佐藤 はじめ,サッカー部
2,斎藤 かな,陸上部
3,清田 浩一,陸上部
4,小林 裕太,サッカー部
5,宮田 敦,サッカー部
6,久米 ひろ子,茶道部
```
#### jinja2テンプレート
このcsvファイルをHTMLに変換するためのjinja2テンプレートを作成します。
ここで、HTML文書のタイトル部分はコマンドラインから指定することにします。

```jinja2:demo.tmpl
<html>
<head> 
    <title>{{params.title}}</title>
</head>
<body>
<ul>
{# 部活名(col_02)でグループ化 #}
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
</body>
</html>
```

#### 実行
toj2コマンドを実行します。
```sh
toj2 csv demo.tmpl demo.csv --out result.html --parameters title=部活別生徒リスト
```
#### 実行結果
結果のHTMLが生成されます。これがtoj2の機能です。

```html
<html>
<head> 
    <title>部活別生徒リスト</title>
</head>
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
</body>
</html>
```

### 動作の仕組み
変換を行うにはtoj2がcsvから生成するデータ形式を理解する必要があるので、解説します。
toj2が読み込んだcsvファイルは以下のようなdictに変換されて、jinja2テンプレートへ渡されています。

```python
{
    'cols' : ['col_00','col_01','col_02'], # csvカラム名のリスト、独自に命名することもできます
    'rows' : [ # csvの各行の内容を含んだリスト

        {   # csvの1行ごとにdictが生成されます
            # ヘッダやパラメータで指定がなければ、カラム名はcol_00, col_01...の連番です
            'col_00' : '1',
            'col_01' : '佐藤 はじめ',
            'col_02' : 'サッカー部'
        },
        # 以下略
    ],
    'params' : { # コマンド引数 --parameters で渡された値はここに格納されます
        'title' : '部活別生徒リスト'
    }                       
}
```

このdictをjinja2で処理することで、任意の変換が行われます。

## CSV変換固有のコマンドオプション
toj2全体のコマンド引数については[共通の引数](../README.md#共通コマンド引数)を参照してください。
csvファイルに対してはオプション引数しか存在しないため、全ての引数が省略可能です。

#### デリミタ
ファイルがタブ文字などカンマ以外で区切られている場合、任意の文字を指定できます。タブ区切りの場合は以下のように指定します。

```sh
# タブ区切りファイルの処理
toj2 csv test.tmpl test.csv --delimiter "\t"
```

#### ヘッダ
1行目をヘッダ名として項目名に使用します。例えばヘッダが`name, age, job`の場合、jinja2が受け取る`row`には`row.name, row,age, row.job`が格納されます。
`--header`オプションと`--names`オプションが両方指定された場合、`--header`が優先されます。

```sh
# ヘッダ使用
toj2 csv test.tmpl test.csv --header
```

もしもヘッダよりも多くカラムがある場合、`row.name, row,age, row.job, row.col_03`などのように連番で補完します。

#### 行スキップ
先頭から指定の行数を読み飛ばします。
例えば、ヘッダ行のあるCSVのヘッダ行を無視する場合には、`--skip-lins 1`とします。

```sh
# ヘッダをスキップ
toj2 csv test.tmpl test.csv --skip-lins 1
```

`--header`オプションと`--skip-lins`オプションが両方指定された場合、`--skip-lins`で読み飛ばした直後の行をヘッダとして扱います。[^skip-and-header]

```sh
# 2行目がヘッダになる
toj2 csv test.tmpl test.csv --skip-lins 1 --header
```

#### カラム名指定
ヘッダ項目名を実行時に直接指定します。以下の呼出しでは`row`には`row.name, row,age, row.job`が格納されます。

```sh
# 直接名前指定
toj2 csv test.tmpl test.csv --names name age job
```

`--header`オプションと`--names`オプションが両方指定された場合、`--header`が優先されます。

[トップへ](../README.md)

[^skip-and-header]: このような使い方は通常あり得ませんが、開発中に実際に必要なcsvファイルを見たので実装しています。
