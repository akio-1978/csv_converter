import io
import sys
import argparse

# こんな形のオプションをつけたい
# python csv_translator.py [-h csvヘッダの有無] [-e csvファイルのエンコーディング] [-o 出力先]


if __name__ == '__main__':
    # windows対策
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # コマンドライン引数の処理
    parser = argparse.ArgumentParser(add_help=False)
    
    # 使用するテンプレートと処理するcsvファイル
    # コマンドラインで指定した順番にtemplate、csvの順に設定される
    parser.add_argument('template', help='jinja2 template file.')
    parser.add_argument('csv', help='transform csv.')

    # 先頭行をヘッダとして扱うか？
    parser.add_argument('-h', '--header', help='first line is header.', action='store_true')
    # 読み込む  csvファイルのエンコーディング
    parser.add_argument('-e', '--encoding', metavar='enc', help='file encoding.', nargs=1, default='utf-8')
    # ヘルプ
    parser.add_argument('--help', help='show help.', action='help')

    print(parser.parse_args())
