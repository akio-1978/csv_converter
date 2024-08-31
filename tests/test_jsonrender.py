import unittest
from j2shrine.context import RenderContext
from j2shrine.json.json_render import JsonLoader
from j2shrine.processors import Jinja2Processor
from tests.testutils import J2SRenderTest


class JsonRenderTest(J2SRenderTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'json'

    def test_simple_json(self):
        ctx = self.default_context()
        ctx.template='tests/json/templates/simple_json.tmpl'
        ctx.source = 'tests/json/src/simple_json.json'
        
        
        self.file_convert_test(context=ctx,
                               expect='tests/json/expect/simple_json.sql',
                               )

    def file_convert_test(self, *, context, expect):
        context.out = self.result_file()
        loader = JsonLoader(context=context, processor=Jinja2Processor(context))

        self.processor_test(loader=loader, expect_file=expect)

    def default_context(self):
        ctx = RenderContext()
        ctx.parameters = {}
        ctx.template_encoding = 'utf8'
        ctx.input_encoding = 'utf8'
        ctx.output_encoding = 'utf8'
        
        return ctx


if __name__ == '__main__':
    unittest.main()
