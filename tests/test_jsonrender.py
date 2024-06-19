import unittest
from j2shrine.json.json_render import JsonRender
from j2shrine.json.json_context import JsonRenderContext
from tests.testutils import J2SRenderTest, RenderArgs


class JsonRenderTest(J2SRenderTest):

    def result_dir(self):
        """出力ディレクトリ名を返す"""
        return 'json'

    def test_simple_json(self):
        args = RenderArgs()
        args.template='tests/json/templates/simple_json.tmpl'
        args.src = 'tests/json/src/simple_json.json'
        
        
        self.file_convert_test(args=args,
                               expect='tests/json/expect/simple_json.sql',
                               )

    def file_convert_test(self, *, args, expect):
        context = JsonRenderContext(args=args)
        render = JsonRender(context=context)

        self.rendering_test(render=render, expect_file=expect, source=context.src)


if __name__ == '__main__':
    unittest.main()
