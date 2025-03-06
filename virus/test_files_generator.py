#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   test_files_generator.py
@Time    :   2021/06/01 23:32:01
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@Desc    :   Create test python files
'''


if __name__ == '__main__':
    filenames = ["test1.py", "test2.py", "test3.py"]
    data = 'print("hello")\n'

    for file in filenames:
        f = open(file, "w")
        f.write(data)
        f.close()
    
