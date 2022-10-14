# import os,sys,json,shutil
# path = os.path.dirname(os.path.realpath(__file__)) + r'/base'
# sys.path.append(path)
# epcam_path = path + r'/epcam'
# sys.path.append(epcam_path)
# import epcam
# import epcam_api
# import job_operation
# import layer_info
# import re

import sys
import json
import time
from time import sleep

import psycopg2
import pytest
from os.path import dirname, abspath
import os,sys,json,shutil
# sys.path.append(r'C:\cc\ep_local\product\EP-CAM\version\20220919\EP-CAM_beta_2.28.054_s36_jiami\Release')
sys.path.append(r'C:\EPSemicon\cc\epcam')
import epcam
import epcam_api
import job_operation
import layer_info
import re
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
import gl as gl
from config import RunConfig



def is_chinese(string):
    """判断是否有中文
    :param     string(str):所有字符串
    :returns   :False
    :raises    error:
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def Traverse_Gerber(job, step, file_path,index):
    """转换Gerber文件
    :param     job(str):job名
    :param     step(str):step名
    :param     file_path(str):文件路径
    :param     index(int):序号
    :returns   :None
    :raises    error:
    """
    for root, dirs, files in os.walk(file_path):
        epcam_api.file_translate_init(job)
        offsetFlag = False
        offset1 = 0
        offset2 = 0
        for file in files:
            if is_chinese(file):
                os.rename(file_path+r'/'+file,file_path+r'/''unknow'+str(index))
                file='unknow'+str(index)
                index=index+1
            ret = epcam_api.file_identify(os.path.join(root, file))
            data = json.loads(ret)
            file_format = data['paras']['format']
            file_param = data['paras']['parameters']
            file_minNum = file_param['min_numbers']
            min_1 = file_minNum['first']
            min_2 = file_minNum['second']
            # file_param = {'Coordinates':'Absolute',
            #               'Decimal_numbers':True,
            #               'Number_format_integer':2,
            #               'Number_format_decimal':4,
            #               'data_type':'Ascii',
            #               'file_size':1391.0,
            #               'format':'Excellon2',
            #               'separator_char':'nl',
            #               'text_line_width':0.0,
            #               'tool_units':'Inch',
            #               'units':'Inch',
            #               'zeroes_omitted':'Leading'}
            if file_format == 'Gerber274x' or file_format == 'Excellon2' or file_format == 'DXF':
                print(file)
                if file_format == 'Gerber274x':
                    if (offsetFlag == False) and (abs(min_1 - sys.maxsize) > 1e-6 and abs(min_2 - sys.maxsize) > 1e-6):
                        offset1 = min_1
                        offset2 = min_2
                        offsetFlag = True
                    file_param['offset_numbers'] = {'first':offset1, 'second':offset2}
                re = epcam_api.file_translate(os.path.join(root, file), job, step, file, file_param, '', '', '', [])    #translate
        for dir_name in dirs:
            Traverse_Gerber(job, step, os.path.join(root,dir_name),index)

def gerber_to_odb(job, step, file_path, out_path):
    """Gerber转ODB
    :param     job(str):job名
    :param     step(str):step名
    :param     file_path(str):gerber文件夹路径
    :param     out_path:输出odb路径
    :returns   :None
    :raises    error:
    """
    epcam.init()
    new_job_path = os.path.join(out_path, job)             #job若存在则删除
    if os.path.exists(new_job_path):
        shutil.rmtree(new_job_path)
    epcam_api.create_job(out_path,job)
    job_operation.open_job(out_path,job)
    job_operation.create_step(job,step)
    job_operation.save_job(job)
    index=1
    Traverse_Gerber(job,step,file_path,index)
    job_operation.save_job(job)
    all_layer=layer_info.get_all_layer_name(job)   #获得料号下所有layer

    # #比对
    # tol = 0.9 * 25400
    # isGlobal = True
    # consider_sr = True
    # map_layer_res = 200 * 25400
    # all_result = {}     #存放所有层比对结果
    # for layer in all_layer:
    #     layer_result = epcam_api.layer_compare_point(job, step, layer, job, step, layer, tol, isGlobal, consider_sr, map_layer_res)
    #     all_result[layer] = layer_result

    # a = 0


if __name__=="__main__":
    job='hige001a'
    step='orig'
    file_path=r'C:\cc\share\temp_2093_1665738392\gerber\hige001a'
    out_path=r'C:\job\test\odb'
    gerber_to_odb(job, step, file_path, out_path)
    data2 = {"cmd":"show_layer", "job":job, "step": 'orig', "layer": 'gtl'}
    js = json.dumps(data2)
    epcam.view_cmd(js)
