import io
import contextlib
import argparse

def get_stream(*, source:str | io.TextIOWrapper, encoding:str='utf8', mode:str='r'):
    """入出力ラッパー
        with文で使う前提
        ファイル名を受け取ったらopenし、TextIOWrapperならencodingを変更して再構築する。
        openしたファイルはcloseし、TextIOWrapperならcloseしない。
    """
    if not isinstance(source, io.TextIOWrapper):
        return contextlib.closing(open(source, encoding=encoding, mode=mode))
    else:
        return contextlib.nullcontext(io.TextIOWrapper(source, encoding=encoding))
    
class KeyValuesParseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        """=区切りで複数与えられた値をdictで格納する
            ex.
            args:A=1 B=2 C=3
            dict:{'A' : '1', 'B' : '2', 'C' : '3'}
        """
        setattr(namespace, self.dest, self.parse_key_values(values))

    def parse_key_values(self, values):
        key_values = {}
        for value in values:
            key_value = value.partition('=')
            key_values[key_value[0]] = key_value[2]
        return key_values
