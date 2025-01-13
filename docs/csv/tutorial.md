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
CSVファイルの第一カラムには出席番号が含まれていますが、テンプレートには使用しません。

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
このテンプレートには部活および生徒の他に、クラスの担任の先生の名前の記述欄もありますがこれはcsvファイルには含まれないので、別途指定することにします。

```jinja2:demo.tmpl
<html>
<head> 
    <title>部活別生徒一覧</title>
</head>
<body>
<h1>部活別生徒一覧</h1>
担任 {{params.teacher}}
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
toj2コマンドを実行します。ここで外部パラメータとして担任の先生の名前を入れてあげます。

```sh
toj2 csv demo.tmpl demo.csv --out result.html --parameters teacher=A.Sawada
```
#### 実行結果
結果のHTMLが生成されます。csvファイルの中身と、コマンドから渡した外部パラメータがそれぞれ参照されています。

```html
<html>
<head> 
    <title>部活別生徒一覧</title>
</head>
<body>
<h1>部活別生徒一覧</h1>
担任 Kaji Taro
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
次に、どのようにこの動作を実現するのか説明します。
toj2は読み込んだcsvファイルを以下のような形のdictに変換します。

```python
{
    'cols' : ['col_00','col_01','col_02'], # csvカラム名のリスト、デフォルトは連番です
    'rows' : [ # csvの各行の内容を含んだリスト

        {   # csvの1行ごとにdictが生成されます
            # カラム名はリスト cols に格納された文字列です。データは全て文字列として扱われます。
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

csvファイル中の情報は欠けることなくこのdictに含まれています。このdictをjinja2で処理すれば好きな形式に変換することができます。これがtoj2の基本機能です。

## CSV変換固有のコマンドオプション
以下は実際にcsv変換を行う際に使用するコマンドラインオプションです。
toj2全体のコマンド引数については[共通の引数](../README.md#共通コマンド引数)を参照してください。
csvファイルに対してはオプション引数しか存在しないため、全ての引数が省略可能です。

#### --delimiter デリミタの指定
ファイルがタブ文字などカンマ以外で区切られている場合、任意の文字を指定できます。タブ区切りの場合は以下のように指定します。デフォルト値はカンマです。

```sh
# タブ区切りファイルの処理
toj2 csv test.tmpl test.csv --delimiter "\t"
```

#### --header ヘッダの使用
1行目をヘッダ名として項目名に使用します。例えばヘッダが`name, age, job`の場合、toj2は`cols`を`['name', 'age', 'job']`として生成し、同様に`row`には`row.name, row,age, row.job`を格納してjinja2へ渡します。
`--header`オプションと`--names`オプションが両方指定された場合、`--header`が優先されます。

```sh
# ヘッダ使用
toj2 csv test.tmpl test.csv --header
```

#### --slip-lines 行のスキップ
先頭から指定の行数を読み飛ばします。ほとんどの場合、このオプションはファイル先頭のヘッダ行を読み飛ばすために使います。[^skip-and-header]
例えば、ヘッダ行のあるCSVのヘッダ行を無視する場合には、`--skip-lins 1`とします。

```sh
# ヘッダをスキップ
toj2 csv test.tmpl test.csv --skip-lins 1
```

`--header`オプションと`--skip-lins`オプションが両方指定された場合、`--skip-lins`で読み飛ばした直後の行をヘッダとして扱います。 

```sh
# 2行目がヘッダになる
toj2 csv test.tmpl test.csv --skip-lins 1 --header
```

#### --names カラムに名前を付ける
カラム名を指定します。デフォルトではカラム名は、`['col_00', 'col_01', 'col_02']`のような連番になりますが、`--names`オプションを指定した以下の呼出しでは`['name', 'age', 'job']`のように命名されます。

**テンプレートの保守性のためには、常に--namesオプションを指定することを推奨します。**

```sh
# 左から順に、使用しない項目であっても名前を付ける
toj2 csv test.tmpl test.csv --names name age job
```
同じ名前が二回以上指定された場合、読み込まれる値は最後に読み込まれたものが使用されます。
`--header`オプションと`--names`オプションが両方指定された場合、`--header`が優先されます。

<details>
<summary>名前を付けることはテンプレートの意図を明確にする良い方法です</summary>

##### --namesオプション使用例

デモで書いた例を`--names`オプションを使用して書き直してみます。 [^readable]

```jinja2:namesdemo.tmpl
<html>
<head> 
    <title>部活別生徒一覧</title>
</head>
<body>
<h1>部活別生徒一覧</h1>
担任 {{params.teacher}}
<ul>
{# 部活名(club_name)でグループ化 #}
{%- for club_name, students in rows | groupby('club_name')%}
    <li>{{club_name}}
        <ul>
            {%- for student in students %}
            <li>{{student.name}}</li>
            {%- endfor %}
        </ul>
    </li>
    {%- endfor %}

</ul>
</body>
</html>
```
コマンドにオプションを追加します
```sh
toj2 csv namesdemo.tmpl demo.csv --out namesresult.html --names no name club_name --parameters teacher=A.Sawada
```
</details>

[トップへ](../README.md)

[^skip-and-header]: レアケースですが、6行目から始まるcsvファイルというものも見たことがあります。
