from cc_method import GetTestData,DMS
import pytest
from os.path import dirname, abspath
import os,sys,json,shutil
path = r'C:\cc\python\epwork\dms\job_manage\epcam'
sys.path.append(path)
import epcam,job_operation,epcam_api
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from g_cc_method_no_django import Asw
from epcam_cc_method_no_django import EpGerberToODB
from os.path import dirname, abspath
import os,sys,json,shutil
# from g_cc_method_local import Asw
import time
import urllib  # 导入urllib库
import urllib.request
import re
import psycopg2
import requests
import rarfile
from cc_method import DMS
from config import RunConfig



def get_data(file_path):
    """
    读取参数化文件
    :param file_path:
    :return:
    """
    data = []
    with(open(file_path, "r")) as f:
        dict_data = json.loads(f.read())
        for i in dict_data:
            data.append(tuple(i.values()))
    return data

@pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
def test_gerber_to_odb_ep_local_convert(job_id,prepare_test_job_clean_g):
    print("G软件VS开始啦！")
    asw = Asw(r"C:\EPSemicon\cc\gateway.exe")#拿到G软件

    data = {}#存放当前测试料号的每一层的比对结果。
    g_vs_total_result_flag = True  # True表示最新一次G比对通过
    vs_time_g = str(int(time.time()))#比对时间
    data["vs_time_g"] = vs_time_g#比对时间存入字典
    data["job_id"] = job_id


    #取到临时目录
    temp_path = RunConfig.temp_path_base + "_" + str(job_id) + "_" + vs_time_g
    temp_gerber_path = os.path.join(temp_path, 'gerber')
    temp_ep_path = os.path.join(temp_path, 'ep')
    temp_g_path = os.path.join(temp_path, 'g')

    #下载并解压原始gerber文件
    DMS().get_file_from_dms_db(temp_path, job_id, field='file_compressed', decompress='rar')

    # 悦谱转图
    job_name_ep = os.listdir(temp_gerber_path)[0] + '_ep'
    file_path_gerber = os.path.join(temp_gerber_path, os.listdir(temp_gerber_path)[0])
    out_path = os.path.join(temp_path, 'ep')
    #先清空同名料号
    epcam_api.close_job(job_name_ep)
    EpGerberToODB().ep_gerber_to_odb_pytest(job_name_ep, 'orig', file_path_gerber, out_path, job_id)

    #下载G转图tgz，并解压好
    DMS().get_file_from_dms_db(temp_path, job_id, field='file_odb_g', decompress='tgz')

    # 打开job_ep
    job_ep_name = os.listdir(temp_ep_path)[0]
    res = job_operation.open_job(temp_ep_path, job_ep_name)
    print("open ep result:", res)
    all_layer_ep=job_operation.get_all_layers(job_ep_name)
    if len(all_layer_ep) == 0:
        g_vs_total_result_flag = False
        print("最新-EP-ODB++打开失败！！！！！")
    else:
        print('悦谱软件tgz中的层信息：', all_layer_ep)

    # 打开job_g
    job_g_name = os.listdir(temp_g_path)[0]
    job_operation.open_job(temp_g_path, job_g_name)
    print("open g result:", res)
    all_layer_g=job_operation.get_all_layers(job_g_name)
    if len(all_layer_g) == 0:
        g_vs_total_result_flag = False
        print("G-ODB++打开失败！！！！！")
    else:
        print('G软件tgz中的层信息：', all_layer_g)

    #以G转图为主来比对
    job1 = os.listdir(os.path.join(temp_path, 'g'))[0]
    jobpath1 = r'\\vmware-host\Shared Folders\share/{}/g/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job1)
    step1 = 'orig'

    job2 = os.listdir(os.path.join(temp_path, 'ep'))[0]
    jobpath2 = r'\\vmware-host\Shared Folders\share/{}/ep/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job2)
    step2 = 'orig'
    layer2_ext = '_copy'

    # 读取配置文件
    with open(r'C:\EPSemicon\cc\config.json', encoding='utf-8') as f:
        cfg = json.load(f)
    tol = cfg['job_manage']['vs']['vs_tol_g']
    print("tol:", tol)
    map_layer_res = 200

    print("job1:", job1, "job2:", job2)

    # 先删除同名料号
    asw.delete_job(job1)
    asw.delete_job(job2)

    # 导入要比图的资料
    asw.import_odb_folder(jobpath1)
    asw.import_odb_folder(jobpath2)
    #G打开要比图的2个料号
    asw.layer_compare_g_open_2_job(jobpath1=jobpath1, step='orig',jobpath2=jobpath2)
    step = "orig"
    for layer in all_layer_g:
        print("g_layer:", layer)
        print("比对参数:", job_g_name, step, layer, job_ep_name, step, layer)
        if layer in all_layer_ep:
            map_layer = layer + '-com'
            result = asw.layer_compare_do_compare(jobpath1, step1, layer, jobpath2, step2, layer, layer2_ext, tol,
                                                  map_layer, map_layer_res)
            if result == 'inner error':
                pass
                print(layer, "比对异常！")
        else:
            pass
            print("悦谱转图中没有此层")

    asw.save_job(job1)
    asw.save_job(job2)

    asw.layer_compare_close_job(jobpath1=jobpath1, jobpath2=jobpath2)

    temp_path_g_export = r'//vmware-host/Shared Folders/share/{}/ze'.format(
        'temp' + "_" + str(job_id) + "_" + vs_time_g)

    if not os.path.exists(os.path.join(temp_path, 'ze')):
        os.mkdir(os.path.join(temp_path, 'ze'))
    # asw.g_export(job1, r'Z:/share/temp')
    asw.g_export(job1, temp_path_g_export)
    # asw.delete_job(job1)
    # asw.delete_job(job2)




    # 开始查看比对结果
    # 获取原始层文件信息，最全的
    ans = DMS().get_job_layer_fields_from_dms_db_pandas(job_id, field='layer_org')
    all_layer_from_org = [each for each in ans]
    print("all_layer_from_org:", all_layer_from_org)
    # 先解压
    temp_path_ze = r'C:\cc\share\{}\ze'.format('temp' + "_" + str(job_id) + "_" + vs_time_g)
    job_operation.untgz(os.path.join(temp_path_ze, os.listdir(temp_path_ze)[0]), temp_path)
    all_result = {}
    for layer in all_layer_g:
        pass
        print('each layer of all_layer_g:',layer)
        layer_result = asw.layer_compare_analysis_temp_path(jobpath1, step, layer, layer2_ext, layer + '-com', temp_path)
        all_result[layer] = layer_result
        for each in all_layer_from_org:
            if layer == str(each).lower().replace(" ", "-").replace("(", "-").replace(")", "-"):
                print("I find it!!!!!!!!!!!!!!")
                print(layer_result, type(layer_result))
                try:
                    if layer_result == "正常":
                        print(layer, "比对通过！")
                    elif layer_result == "错误":
                        print(layer, "未通过！")
                        g_vs_total_result_flag = False
                    elif layer_result == "未比对":
                        print(layer, "未比对！")
                        g_vs_total_result_flag = False
                    else:
                        print("异常，状态异常！！！")

                except:
                    pass
                    print("异常！")

    print("*" * 100)
    print(all_result)
    print("*" * 100)

    if g_vs_total_result_flag == True:
        pass
        print("恭喜您！料号比对通过！")
    if g_vs_total_result_flag == False:
        pass
        print("Sorry！料号比对未通过，请人工检查！")

    print("*" * 100)
    if os.path.exists(r'C:\EPSemicon\cc\result.json'):
        os.remove(r'C:\EPSemicon\cc\result.json')

    with open(r'C:\EPSemicon\cc\result.json', 'w') as f:
        json.dump(all_result, f, indent=4, ensure_ascii=False)

    # 删除temp_path
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


    data = {}
    data["vs_time_g"] = vs_time_g
    data["job_id"] = job_id
    data["all_result"] = all_result

    print(data)

    assert g_vs_total_result_flag == True

    for key in all_result:
        print(key + ':' + all_result[key])
        assert all_result[key] == "正常"
