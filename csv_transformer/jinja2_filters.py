from itertools import groupby

records =[
    {'a' : 1, 'b' : 'b_str1', 'c': 'c_str1'},
    {'a' : 1, 'b' : 'b_str11', 'c': 'c_str11'},
    {'a' : 2, 'b' : 'b_str2', 'c': 'c_str2'},
]

def groups(records, field):
    result_list = []
    group_list = groupby(records, lambda e:e[field])
    for key, group in group_list:
        result_list.append(group)
    return result_list

if __name__ == '__main__':

    groups_object = groups(records, 'a')
    for item in groups_object:
        print(item)
