import io
import contextlib

def get_stream(*, source:str | io.TextIOWrapper, encoding:str='utf8', mode:str='r'):
    """入出力ラッパー
        with文で使う前提
        ファイル名を受け取ったらopenし、TextIOWrapperならencodingを変更して再構築する。
        openしたファイルはcloseし、TextIOWrapperならcloseしない。
    """
    if not isinstance(source, io.TextIOWrapper):
        return contextlib.closing(open(source, encoding=encoding, mode=mode))
    else:
        return contextlib.nullcontext(io.TextIOWrapper(source.buffer, encoding=encoding))
    
