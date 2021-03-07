import unittest
from csv_transformer import TransfomerParameters
from csv_transformer import CsvTransformar
from csv_transformer import __version__


def test_version():
    assert __version__ == '0.1.0'

class CsvTransformerTest(unittest.TestCase):
    headerless_csv = '''\
G01,SG01, val001,val002,val003
G01,SG02, val101,val102,val103
G02,SG02, val201,val202,val203
'''
    headered_csv = '''\
GROUP, SUBGROUP, V1,V2,V3
G01,SG01, val001,val002,val003
G01,SG02, val101,val102,val103
G02,SG02, val201,val202,val203
'''

    template_to_json = '''\
{
    "groups" : [
{% for line in lines %}
        {
            "group" : "{{line.GROUP}}",
            "subgroups" : [
                {
                    "subgroup" : "{{line.SUBGROUP}}",
                    "V1" : "{{line.V1}}",
                    "V2" : "{{line.V2}}",
                    "V3" : "{{line.V3}}"
                }
            ]
        }
{%end-for%}
    ]
}
'''

    result_json='''/
{
    "list" : [
        {
            group="G01",
            sungroup="SG01"
            "V1" : "val001",
            "V2" : "val002",
            "V3" : "val003"
        },
        {
            group="G01",
            sungroup="SG02"
            "V1" : "val101",
            "V2" : "val102",
            "V3" : "val103"
        },
        {
            group="G02",
            sungroup="SG01"
            "V1" : "val201",
            "V2" : "val202",
            "V3" : "val203"
        },
    ]
}
'''
