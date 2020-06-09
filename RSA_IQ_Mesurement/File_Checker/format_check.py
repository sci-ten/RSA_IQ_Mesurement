'''
Created on 2020/06/05

@author: HIROTO
'''

import os


def check_file_extention(path,extention='csv'):
    try:
        file_extention = os.path.splitext(path)[1][1:]
        if extention==file_extention:
            return True
    except:
        return False

    return False

def check_paths_or_dirs_exsist(path_list):
    for ele in path_list:
        if os.path.isfile(ele) or os.path.isdir(ele)==True:
            return False
    return True


