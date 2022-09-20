import sys
import json
import time
from time import sleep

import psycopg2
import pytest
from os.path import dirname, abspath
import os,sys,json,shutil
sys.path.append(r'C:\cc\ep_local\product\EP-CAM\version\20220919\EP-CAM_beta_2.28.054_s36_jiami\Release')
sys.path.append(r'C:\EPSemicon\cc\epcam')
import epcam
import epcam_api
import job_operation
import layer_info
import re
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
import gl as gl


class EpGerberToODB:

    def is_chinese(self,string):
        """判断是否有中文
        :param     string(str):所有字符串
        :returns   :False
        :raises    error:
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False


    def ep_vs(self,job, step, file_path, out_path):
        pass
        # 比对
        tol = 0.9 * 25400
        isGlobal = True
        consider_sr = True
        map_layer_res = 200 * 25400
        all_result = {}  # 存放所有层比对结果
        all_layer=gl.all_layer
        for layer in all_layer:
            layer_result = epcam_api.layer_compare_point(job, step, layer, job, step, layer, tol, isGlobal, consider_sr,
                                                         map_layer_res)
            all_result[layer] = layer_result
        print("*" * 100)
        print(all_result)
        print("*" * 100)


    def traverse_gerber_pytest(self,job, step, file_path, index,job_id):
        # print("*"*30,job_id)
        # job_current = models.Job.objects.get(id=job_id)
        conn = psycopg2.connect(database="dms", user="readonly", password="123456", host="10.97.80.147", port="5432")
        cursor = conn.cursor()
        sql = '''SELECT a.layer_org from layer a
            where a.job_id = {}
                '''.format(job_id)
        cursor.execute(sql)
        conn.commit()
        ans = cursor.fetchall()
        conn.close()
        print(ans)

        all_layer_from_org = []
        for each in ans:
            # print(each[0])
            all_layer_from_org.append(each)

        print('all_layer_from_org::',all_layer_from_org)

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
                if self.is_chinese(file):
                    os.rename(file_path + r'/' + file, file_path + r'/''unknow' + str(index))
                    file = 'unknow' + str(index)
                    index = index + 1
                os.rename(file_path + r'/' + file,file_path + r'/' + file.replace(' ','-').replace('(','-').replace(')','-'))
                print("file name:",file.replace(' ','-').replace('(','-').replace(')','-'))
                ret = epcam_api.file_identify(os.path.join(root, file.replace(' ','-').replace('(','-').replace(')','-')))
                print("ret:",ret)
                data = json.loads(ret)
                file_format = data['paras']['format']
                file_name = data['paras']['name']
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



                if file_format == 'Excellon2':
                    print('file:',file)
                    print('''file.replace(' ','-').replace('(','-').replace(')','-'):''',file.replace(' ','-').replace('(','-').replace(')','-'))
                    conn = psycopg2.connect(database="dms", user="readonly", password="123456", host="10.97.80.147",port="5432")
                    cursor = conn.cursor()
                    sql = '''SELECT a.layer,a.status,a.units_ep,a.zeroes_omitted_ep,a."number_format_A_ep",a."number_format_B_ep" from layer a
                                where a.job_id = {} and a.layer = '{}'
                                    '''.format(job_id,file.replace(' ','-').replace('(','-').replace(')','-'))
                    print("sql：",sql)
                    cursor.execute(sql)
                    conn.commit()
                    ans = cursor.fetchall()
                    conn.close()
                    layer_e2 = ans[0][0]
                    print('layer_e2:',layer_e2)
                    layer_e2_status = ans[0][1]
                    print('layer_e2_status:', layer_e2_status)
                    layer_e2_units_ep = ans[0][2]
                    print('layer_e2_units_ep:', layer_e2_units_ep)
                    layer_e2_zeroes_omitted_ep = ans[0][3]
                    print('layer_e2_zeroes_omitted_ep:', layer_e2_zeroes_omitted_ep)
                    layer_e2_number_format_A_ep = ans[0][4]
                    print('layer_e2_number_format_A_ep:', layer_e2_number_format_A_ep)
                    layer_e2_number_format_B_ep = ans[0][5]
                    print('layer_e2_number_format_B_ep:', layer_e2_number_format_B_ep)


                    print('原来：',file_param)
                    try:
                        if layer_e2_status=='published':
                            file_param['units']=layer_e2_units_ep
                            file_param['zeroes_omitted'] = layer_e2_zeroes_omitted_ep
                            file_param['Number_format_integer'] = int(layer_e2_number_format_A_ep)
                            file_param['Number_format_decimal'] = int(layer_e2_number_format_B_ep)
                            file_param['tool_units'] = layer_e2.tool_units_ep
                        print('现在：',file_param)
                        re = epcam_api.file_translate(os.path.join(root, file.replace(' ','-').replace('(','-').replace(')','-')), job, step, file_name, file_param, '', '', '',[])
                    except:
                        print("except:"*5)
                        re = epcam_api.file_translate(os.path.join(root, file.replace(' ','-').replace('(','-').replace(')','-')), job, step, file_name, file_param, '', '', '',[])

                if file_format == 'Gerber274x':
                    print(file)
                    if (offsetFlag == False) and (min_1 < sys.maxsize * 0.5 and min_2 < sys.maxsize * 0.5):
                        offset1 = min_1
                        offset2 = min_2
                        offsetFlag = True
                    file_param['offset_numbers'] = {'first': offset1, 'second': offset2}
                    re = epcam_api.file_translate(
                        os.path.join(root, file.replace(' ', '-').replace('(', '-').replace(')', '-')), job, step,
                        file_name, file_param, '', '', '', [])  # translate
                if file_format == 'DXF':
                    print(file)
                    re = epcam_api.file_translate(
                        os.path.join(root, file.replace(' ', '-').replace('(', '-').replace(')', '-')), job, step,
                        file_name, file_param, '', '', '', [])  # translate

    def ep_gerber_to_odb_pytest(self,job, step, file_path, out_path,job_id):
        """Gerber转ODB
        :param     job(str):job名
        :param     step(str):step名
        :param     file_path(str):gerber文件夹路径
        :param     out_path:输出odb路径
        :returns   :None
        :raises    error:
        """
        # epcam.init()
        new_job_path = os.path.join(out_path, job)  # job若存在则删除
        if os.path.exists(new_job_path):
            shutil.rmtree(new_job_path)
        epcam_api.create_job(out_path, job)


        # time.sleep(20)



        job_operation.open_job(out_path, job)
        job_operation.create_step(job, step)
        job_operation.save_job(job)
        index = 1
        print("*"*100,job, step, file_path, index,job_id)
        self.traverse_gerber_pytest(job, step, file_path, index,job_id)
        job_operation.save_job(job)
        all_layer = layer_info.get_all_layer_name(job)  # 获得料号下所有layer
        gl.all_layer=all_layer
        #清空内存，防止同名料号出问题
        epcam_api.close_job(job)
        # time.sleep(20)
        # job_operation.delete_job(job)#delete会把odb文件夹删除的

if __name__ == "__main__":
    pass
    epcam.init()
    job = 'test1'
    step = 'orig'
    file_path = r'C:\Users\cheng.chen\Desktop\760'
    out_path = r'C:\job\test\odb'
    cc=EpGerberToODB()
    cc.ep_gerber_to_odb_pytest(job, step, file_path, out_path,268)