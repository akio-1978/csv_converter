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

### 共通のオプション 
全入力フォーマットに共通するオプションです。
* -O --output
  * jinja2の処理結果を