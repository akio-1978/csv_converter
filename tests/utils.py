import unittest

def rendering_test(*, ut, render, expect_file, source):
    
    result_file = 'tests/output/' + expect_file.rpartition('/')[2] + '.tmp'
    
    with open(source, encoding='utf-8') as source_reader:
        with open(result_file, 'w') as result_writer:
            render.render(source=source_reader, output=result_writer)

    return file_test(ut=ut, expect_file=expect_file, result_file=result_file)

def file_test(*, ut:unittest.TestCase, expect_file:str, result_file:str):
    with open(expect_file, encoding='utf-8') as expect_reader:
        with open(result_file, encoding='utf-8') as result_reader:
            result = result_reader.read()
            ut.assertEqual(expect_reader.read(), result)
            return result
    