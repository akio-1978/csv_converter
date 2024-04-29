import io

class StreamWrapper:
    """入出力ラッパー
        with文で使う前提
        ファイル名とTextIOWrapper(多分stdin/stdout)を区別せずに扱うためのユーティリティ
        ファイル名を受け取ったらopenするが、TextIOWrapperならencodingを変更して再構築する。
        openしたファイルはcloseするが、TextIOWrapperならcloseしない。
    """
    
    def __init__(self, *, useof:str | io.TextIOWrapper, encoding:str=None, mode:str='r') -> None:
        self.useof = useof
        self.encoding = encoding
        self.mode = mode
        # TextIOWrapperなら__exit__でcloseしない
        self.is_file = not isinstance(useof, io.TextIOWrapper)
    
    def __enter__(self):
        
        if self.is_file:
            self.stream = open(self.useof, encoding=self.encoding, mode=self.mode)
        else:
            self.stream = io.TextIOWrapper(
                self.useof.buffer, encoding=self.encoding)
        return self.stream
    
    def __exit__(self, etype, evalue, traceback):
        if etype:
            return False
        if self.is_file:
            self.stream.close()
        return True
