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



def atest_index():
    pass
    job = 'test1'
    step = 'orig'
    # file_path = r'C:\job\test\gerber\760'
    file_path = r'C:\job\test\gerber\eol80610'
    out_path = r'C:\job\test\odb'
    job_id=1772
    # EpGerberToODB().ep_vs(job, step, file_path, out_path)
    assert 1==1



@pytest.mark.parametrize("job_id",GetTestData().get_job_id('Input'))
def atest_gerber_to_odb_ep(job_id):
    pass
    print("G软件VS")
    # return HttpResponse("G软件VS" + str(job_id))
    data = {}
    g_vs_total_result_flag = True  # True表示最新一次G比对通过
    vs_time_g = str(int(time.time()))
    data["vs_time_g"]=vs_time_g
    data["job_id"]=job_id

    conn = psycopg2.connect(database="dms", user="readonly", password="123456", host="10.97.80.147", port="5432")
    cursor = conn.cursor()
    sql = '''SELECT a.file_odb_current,a.file_odb_g from job a
        where a.id = {}
            '''.format(job_id)
    cursor.execute(sql)
    conn.commit()
    ans = cursor.fetchall()
    conn.close()
    file_odb_current_name=str(ans[0][0]).split("/")[1]
    print("file_odb_current_name:", file_odb_current_name)

    file_odb_g_name = str(ans[0][1]).split("/")[1]
    print("file_odb_g_name:", file_odb_g_name)



    # 拿到job_ep和job_g
    temp_path = r'C:\cc\share\temp' + "_" + str(job_id) + "_" + vs_time_g
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    if not os.path.exists(os.path.join(temp_path, 'ep')):
        os.mkdir(os.path.join(temp_path, 'ep'))
    if not os.path.exists(os.path.join(temp_path, 'g')):
        os.mkdir(os.path.join(temp_path, 'g'))



    # 下载文件
    def file_downloand(need_file_path,save_path):  #######文件下载
        if os.path.exists(need_file_path) == False:  # 判断是否存在文件

            # 文件url
            file_url = 'http://10.97.80.147/media/files/{}'.format(os.path.basename(need_file_path))

            # 文件基准路径
            # basedir = os.path.abspath(os.path.dirname(__file__))
            # 下载到服务器的地址
            file_path = save_path

            try:
                # 如果没有这个path则直接创建
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                # file_suffix = os.path.splitext(file_url)[1]
                # filename = '{}{}'.format(file_path, file_suffix)  # 拼接文件名。
                filename=os.path.join(file_path,os.path.basename(need_file_path))
                urllib.request.urlretrieve(file_url, filename=filename)
                print("成功下载文件")
            except IOError as exception_first:  # 设置抛出异常
                print(1, exception_first)

            except Exception as exception_second:  # 设置抛出异常
                print(2, exception_second)
        else:
            print("文件已经存在！")

    temp_ep_path = os.path.join(temp_path, 'ep')
    if not os.path.exists(os.path.join(temp_ep_path,file_odb_current_name)):
        print("not have")
        file_downloand(os.path.join(temp_ep_path,file_odb_current_name),temp_ep_path)
    time.sleep(0.5)
    ep_tgz_file = os.listdir(temp_ep_path)[0]
    print("ep_tgz_file:", ep_tgz_file)
    print("os.listdir(temp_ep_path)[0]:",os.listdir(temp_ep_path)[0])
    job_operation.untgz(os.path.join(temp_ep_path,os.listdir(temp_ep_path)[0]), temp_ep_path)
    if os.path.exists(os.path.join(temp_ep_path, ep_tgz_file)):
        os.remove(os.path.join(temp_ep_path, ep_tgz_file))
    print("ep_tgz_file_now:", os.listdir(temp_ep_path)[0])



    temp_g_path = os.path.join(temp_path, 'g')
    if not os.path.exists(os.path.join(temp_g_path,file_odb_g_name)):
        print("not have")
        file_downloand(os.path.join(temp_g_path,file_odb_g_name),temp_g_path)
    time.sleep(0.2)
    g_tgz_file = os.listdir(temp_g_path)[0]
    print("g_tgz_file:", g_tgz_file)
    job_operation.untgz(os.path.join(temp_g_path,os.listdir(temp_g_path)[0]), temp_g_path)
    if os.path.exists(os.path.join(temp_g_path, g_tgz_file)):
        os.remove(os.path.join(temp_g_path, g_tgz_file))
    print("g_tgz_file_now:", os.listdir(temp_g_path)[0])



    epcam.init()

    # 打开job_ep
    # job_ep_name=str(job.file_odb_current).split('/')[-1][:-4]
    job_ep_name = os.listdir(temp_ep_path)[0]
    new_job_path_ep = os.path.join(temp_ep_path, job_ep_name)
    print("temp_ep_path:", temp_ep_path, "job_ep_name:", job_ep_name)
    res = job_operation.open_job(temp_ep_path, job_ep_name)
    print("open ep tgz:", res)
    print("job_ep_layer:", job_operation.get_all_layers(job_ep_name))
    if len(job_operation.get_all_layers(job_ep_name)) == 0:
        pass
        g_vs_total_result_flag = False
        print("最新-EP-ODB++打开失败！！！！！")

    # 打开job_g
    # job_g_name = str(job.file_odb_g).split('/')[-1][:-4]
    job_g_name = os.listdir(temp_g_path)[0]
    new_job_path_g = os.path.join(temp_g_path, job_g_name)
    print("temp_g_path:", temp_g_path, "job_g_name:", job_g_name)
    job_operation.open_job(temp_g_path, job_g_name)
    print("open gp tgz:", res)
    print("job_g_layer:", job_operation.get_all_layers(job_g_name))
    if len(job_operation.get_all_layers(job_g_name)) == 0:
        pass
        g_vs_total_result_flag = False
        print("G-ODB++打开失败！！！！！")

    all_result = {}  # 存放所有层比对结果

    step = "orig"

    # 原始层文件信息，最全的
    # all_layer_from_org = models.Layer.objects.filter(job=job)


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

    all_layer_from_org=[]
    for each in ans:
        # print(each[0])
        all_layer_from_org.append(each)







    print("all_layer_from_org:", all_layer_from_org)

    # 以G软件解析好的为主，来VS
    all_layer_g = job_operation.get_all_layers(job_g_name)
    print('G软件tgz中的层信息：', all_layer_g)

    all_layer_ep = job_operation.get_all_layers(job_ep_name)
    print('悦谱软件tgz中的层信息：', all_layer_ep)

    if len(all_layer_g) == 0:
        pass
        g_vs_total_result_flag = False

    if len(all_layer_ep) == 0:
        pass
        g_vs_total_result_flag = False

    asw = Asw(r"C:\EPSemicon\cc\gateway.exe")

    # g_temp_path = r'Z:/share/temp' + "_" + str(request.user) + "_" + str(job_id)
    g_temp_path = r'\\vmware-host\Shared Folders\share/temp'
    rets = []
    paras = {}

    job1 = os.listdir(os.path.join(temp_path, 'g'))[0]
    # jobpath1 = r'Z:/share/temp_{}_{}/g/{}'.format(str(request.user),str(job_id),job1)
    # jobpath1 = r'\\vmware-host\Shared Folders\share/temp/g/{}'.format(job1)
    jobpath1 = r'\\vmware-host\Shared Folders\share/{}/g/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job1)
    step1 = 'orig'
    layer1 = 'bottom.art'

    job2 = os.listdir(os.path.join(temp_path, 'ep'))[0]

    # jobpath2 = r'Z:/share/temp_{}_{}/ep/{}'.format(str(request.user),str(job_id),job2)
    # jobpath2 = r'\\vmware-host\Shared Folders\share/temp/ep/{}'.format(job2)
    jobpath2 = r'\\vmware-host\Shared Folders\share/{}/ep/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job2)
    step2 = 'orig'
    layer2 = 'bottom.art'

    layer2_ext = '_copy'

    # 读取配置文件
    with open(r'C:\EPSemicon\cc\config.json', encoding='utf-8') as f:
        cfg = json.load(f)
    tol = cfg['job_manage']['vs']['vs_tol_g']
    print("tol:", tol)
    map_layer = layer2 + '-com'
    map_layer_res = 200

    print("job1:", job1, "job2:", job2)

    #先删除同名料号
    asw.delete_job(job1)
    asw.delete_job(job2)



    asw.import_odb_folder(jobpath1)  # 导入要比图的资料,G的
    asw.import_odb_folder(jobpath2)  # 导入要比图的资料，悦谱的

    asw.layer_compare_g_open_2_job(jobpath1, step1, layer1, jobpath2, step2, layer1, layer2_ext, tol, map_layer,
                                   map_layer_res)
    for layer in all_layer_g:
        print("g_layer:", layer)
        print("比对参数", job_g_name, step, layer, job_ep_name, step, layer)
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



    asw.layer_compare_close_job(jobpath1, step1, layer1, jobpath2, step2, layer2, layer2_ext, tol, map_layer,
                                map_layer_res)

    temp_path_g_export = r'//vmware-host/Shared Folders/share/{}/ze'.format(
        'temp' + "_" + str(job_id) + "_" + vs_time_g)

    if not os.path.exists(os.path.join(temp_path, 'ze')):
        os.mkdir(os.path.join(temp_path, 'ze'))
    # asw.g_export(job1, r'Z:/share/temp')
    asw.g_export(job1, temp_path_g_export)
    # asw.delete_job(job1)
    # asw.delete_job(job2)

    # 开始查看比对结果
    # 先解压
    temp_path_ze = r'C:\cc\share\{}\ze'.format('temp' + "_" + str(job_id) + "_" + vs_time_g)
    job_operation.untgz(os.path.join(temp_path_ze, os.listdir(temp_path_ze)[0]), temp_path)
    all_result = {}
    for layer in all_layer_g:
        pass
        print(layer)
        layer_result = asw.layer_compare_analysis_temp_path(jobpath1, step1, layer, jobpath2, step2, layer, layer2_ext,
                                                            tol,
                                                            layer + '-com', map_layer_res, temp_path)
        # print(layer_result)

        all_result[layer] = layer_result

        for each in all_layer_from_org:
            # print("each[0]:",each[0])
            # print("layer:",layer,"str(each[0]):",str(each[0]).lower().replace(" ","-").replace("(","-").replace(")","-"))
            if layer == str(each[0]).lower().replace(" ", "-").replace("(", "-").replace(")", "-"):
                print("I find it!!!!!!!!!!!!!!")
                print(layer_result, type(layer_result))
                # layer_result_dict=json.loads(layer_result)
                # print(layer_result_dict)
                # print(len(layer_result_dict["result"]))

                try:
                    # print('layer_result_dict["result"]:',layer_result_dict["result"])
                    if layer_result == "正常":
                        print(layer,"比对通过！")
                    elif layer_result == "错误":
                        print(layer,"未通过！")
                        g_vs_total_result_flag = False
                    elif layer_result == "未比对":
                        print(layer,"未比对！")
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
        json.dump(all_result, f,indent=4, ensure_ascii=False)



    # 删除temp_path
    # if os.path.exists(temp_path):
    #     shutil.rmtree(temp_path)

    # if os.path.exists(r'C:\cc\share\temp' + "_" + str(request.user) + "_" + str(job_id)):
    #     shutil.rmtree(r'C:\cc\share\temp' + "_" + str(request.user) + "_" + str(job_id))
    data={}
    data["vs_time_g"] = vs_time_g
    data["job_id"]=job_id
    data["all_result"]=all_result

    print(data)

    assert g_vs_total_result_flag == True

    for key in all_result:
        print(key + ':' + all_result[key])
        assert all_result[key] == "正常"

@pytest.mark.parametrize("job_id",GetTestData().get_job_id('Input'))
def atest_gerber_to_odb_ep_local_convert(job_id):
    pass


    #删除所有料号
    asw = Asw(r"C:\EPSemicon\cc\gateway.exe")
    asw.clean_g_all_pre_get_job_list(r'//vmware-host/Shared Folders/share/job_list.txt')
    asw.clean_g_all_do_clean(r'C:\cc\share\job_list.txt')



    print("G软件VS")
    # return HttpResponse("G软件VS" + str(job_id))
    data = {}
    g_vs_total_result_flag = True  # True表示最新一次G比对通过
    vs_time_g = str(int(time.time()))
    data["vs_time_g"]=vs_time_g
    data["job_id"]=job_id

    conn = psycopg2.connect(database="dms", user="readonly", password="123456", host="10.97.80.147", port="5432")
    cursor = conn.cursor()
    sql = '''SELECT a.file_odb_current,a.file_odb_g,a.file_compressed from job a
        where a.id = {}
            '''.format(job_id)
    print('sql:',sql)
    cursor.execute(sql)
    conn.commit()
    ans = cursor.fetchall()
    conn.close()
    #file_odb_current_name=str(ans[0][0]).split("/")[1]
    #print("file_odb_current_name:", file_odb_current_name)

    file_odb_g_name = str(ans[0][1]).split("/")[1]
    print("file_odb_g_name:", file_odb_g_name)

    file_gerber_name = str(ans[0][2]).split("/")[1]
    print("file_gerber_name:", file_gerber_name)

    # 拿到job_ep和job_g
    temp_path = r'C:\cc\share\temp' + "_" + str(job_id) + "_" + vs_time_g
    temp_gerber_path = os.path.join(temp_path, 'gerber')
    temp_ep_path = os.path.join(temp_path, 'ep')
    temp_g_path = os.path.join(temp_path, 'g')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    if not os.path.exists(temp_gerber_path):
        os.mkdir(temp_gerber_path)
    if not os.path.exists(temp_ep_path):
        os.mkdir(temp_ep_path)
    if not os.path.exists(temp_g_path):
        os.mkdir(temp_g_path)



    # 下载文件
    def file_downloand(need_file_path,save_path):  #######文件下载
        if os.path.exists(need_file_path) == False:  # 判断是否存在文件

            # 文件url
            file_url = 'http://10.97.80.147/media/files/{}'.format(os.path.basename(need_file_path))

            # 文件基准路径
            # basedir = os.path.abspath(os.path.dirname(__file__))
            # 下载到服务器的地址
            file_path = save_path

            try:
                # 如果没有这个path则直接创建
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                # file_suffix = os.path.splitext(file_url)[1]
                # filename = '{}{}'.format(file_path, file_suffix)  # 拼接文件名。
                filename=os.path.join(file_path,os.path.basename(need_file_path))
                urllib.request.urlretrieve(file_url, filename=filename)
                print("成功下载文件")
            except IOError as exception_first:  # 设置抛出异常
                print(1, exception_first)

            except Exception as exception_second:  # 设置抛出异常
                print(2, exception_second)
        else:
            print("文件已经存在！")


    if not os.path.exists(os.path.join(temp_gerber_path, file_gerber_name)):
        print("not have")
        file_downloand(os.path.join(temp_gerber_path, file_gerber_name), temp_gerber_path)
    time.sleep(0.5)
    file_compressed_file_path = os.listdir(temp_gerber_path)[0]
    print("file_compressed_file_path:", file_compressed_file_path)

    rf = rarfile.RarFile(os.path.join(temp_gerber_path, file_gerber_name))
    rf.extractall(temp_gerber_path)
    temp_compressed = os.path.join(temp_gerber_path, file_gerber_name)
    # 删除gerber压缩包
    if os.path.exists(temp_compressed):
        os.remove(temp_compressed)



    file_path_gerber = os.listdir(temp_gerber_path)[0]
    job_name = file_path_gerber + '_ep'
    step = 'orig'
    file_path = os.path.join(temp_gerber_path, file_path_gerber)
    out_path = os.path.join(temp_path, 'ep')

    # 先清空同名料号
    # epcam_api.delete_job(job_name)
    epcam_api.close_job(job_name)

    cc = EpGerberToODB()
    print("*" * 100, job_name, step, file_path, out_path, job_id)
    cc.ep_gerber_to_odb_pytest(job_name, step, file_path, out_path, job_id)




    # temp_ep_path = os.path.join(temp_path, 'ep')
    # if not os.path.exists(os.path.join(temp_ep_path,file_odb_current_name)):
    #     print("not have")
    #     file_downloand(os.path.join(temp_ep_path,file_odb_current_name),temp_ep_path)
    # time.sleep(0.5)
    # ep_tgz_file = os.listdir(temp_ep_path)[0]
    # print("ep_tgz_file:", ep_tgz_file)
    # print("os.listdir(temp_ep_path)[0]:",os.listdir(temp_ep_path)[0])
    # job_operation.untgz(os.path.join(temp_ep_path,os.listdir(temp_ep_path)[0]), temp_ep_path)
    # if os.path.exists(os.path.join(temp_ep_path, ep_tgz_file)):
    #     os.remove(os.path.join(temp_ep_path, ep_tgz_file))
    # print("ep_tgz_file_now:", os.listdir(temp_ep_path)[0])




    if not os.path.exists(os.path.join(temp_g_path,file_odb_g_name)):
        print("not have")
        file_downloand(os.path.join(temp_g_path,file_odb_g_name),temp_g_path)
    time.sleep(0.2)
    g_tgz_file = os.listdir(temp_g_path)[0]
    print("g_tgz_file:", g_tgz_file)
    job_operation.untgz(os.path.join(temp_g_path,os.listdir(temp_g_path)[0]), temp_g_path)
    if os.path.exists(os.path.join(temp_g_path, g_tgz_file)):
        os.remove(os.path.join(temp_g_path, g_tgz_file))
    print("g_tgz_file_now:", os.listdir(temp_g_path)[0])



    epcam.init()

    # 打开job_ep
    # job_ep_name=str(job.file_odb_current).split('/')[-1][:-4]
    job_ep_name = os.listdir(temp_ep_path)[0]
    new_job_path_ep = os.path.join(temp_ep_path, job_ep_name)
    print("temp_ep_path:", temp_ep_path, "job_ep_name:", job_ep_name)
    res = job_operation.open_job(temp_ep_path, job_ep_name)
    print("open ep tgz:", res)
    print("job_ep_layer:", job_operation.get_all_layers(job_ep_name))
    if len(job_operation.get_all_layers(job_ep_name)) == 0:
        pass
        g_vs_total_result_flag = False
        print("最新-EP-ODB++打开失败！！！！！")

    # 打开job_g
    # job_g_name = str(job.file_odb_g).split('/')[-1][:-4]
    job_g_name = os.listdir(temp_g_path)[0]
    new_job_path_g = os.path.join(temp_g_path, job_g_name)
    print("temp_g_path:", temp_g_path, "job_g_name:", job_g_name)
    job_operation.open_job(temp_g_path, job_g_name)
    print("open gp tgz:", res)
    print("job_g_layer:", job_operation.get_all_layers(job_g_name))
    if len(job_operation.get_all_layers(job_g_name)) == 0:
        pass
        g_vs_total_result_flag = False
        print("G-ODB++打开失败！！！！！")

    all_result = {}  # 存放所有层比对结果

    step = "orig"

    # 原始层文件信息，最全的
    # all_layer_from_org = models.Layer.objects.filter(job=job)


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

    all_layer_from_org=[]
    for each in ans:
        # print(each[0])
        all_layer_from_org.append(each)







    print("all_layer_from_org:", all_layer_from_org)

    # 以G软件解析好的为主，来VS
    all_layer_g = job_operation.get_all_layers(job_g_name)
    print('G软件tgz中的层信息：', all_layer_g)

    all_layer_ep = job_operation.get_all_layers(job_ep_name)
    print('悦谱软件tgz中的层信息：', all_layer_ep)

    if len(all_layer_g) == 0:
        pass
        g_vs_total_result_flag = False

    if len(all_layer_ep) == 0:
        pass
        g_vs_total_result_flag = False



    # g_temp_path = r'Z:/share/temp' + "_" + str(request.user) + "_" + str(job_id)
    g_temp_path = r'\\vmware-host\Shared Folders\share/temp'
    rets = []
    paras = {}

    job1 = os.listdir(os.path.join(temp_path, 'g'))[0]
    # jobpath1 = r'Z:/share/temp_{}_{}/g/{}'.format(str(request.user),str(job_id),job1)
    # jobpath1 = r'\\vmware-host\Shared Folders\share/temp/g/{}'.format(job1)
    jobpath1 = r'\\vmware-host\Shared Folders\share/{}/g/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job1)
    step1 = 'orig'
    layer1 = 'bottom.art'

    job2 = os.listdir(os.path.join(temp_path, 'ep'))[0]

    # jobpath2 = r'Z:/share/temp_{}_{}/ep/{}'.format(str(request.user),str(job_id),job2)
    # jobpath2 = r'\\vmware-host\Shared Folders\share/temp/ep/{}'.format(job2)
    jobpath2 = r'\\vmware-host\Shared Folders\share/{}/ep/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job2)
    step2 = 'orig'
    layer2 = 'bottom.art'

    layer2_ext = '_copy'

    # 读取配置文件
    with open(r'C:\EPSemicon\cc\config.json', encoding='utf-8') as f:
        cfg = json.load(f)
    tol = cfg['job_manage']['vs']['vs_tol_g']
    print("tol:", tol)
    map_layer = layer2 + '-com'
    map_layer_res = 200

    print("job1:", job1, "job2:", job2)

    #先删除同名料号
    asw.delete_job(job1)
    asw.delete_job(job2)



    asw.import_odb_folder(jobpath1)  # 导入要比图的资料,G的
    asw.import_odb_folder(jobpath2)  # 导入要比图的资料，悦谱的

    asw.layer_compare_g_open_2_job(jobpath1, step1, layer1, jobpath2, step2, layer1, layer2_ext, tol, map_layer,
                                   map_layer_res)
    for layer in all_layer_g:
        print("g_layer:", layer)
        print("比对参数", job_g_name, step, layer, job_ep_name, step, layer)
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



    asw.layer_compare_close_job(jobpath1, step1, layer1, jobpath2, step2, layer2, layer2_ext, tol, map_layer,
                                map_layer_res)

    temp_path_g_export = r'//vmware-host/Shared Folders/share/{}/ze'.format(
        'temp' + "_" + str(job_id) + "_" + vs_time_g)

    if not os.path.exists(os.path.join(temp_path, 'ze')):
        os.mkdir(os.path.join(temp_path, 'ze'))
    # asw.g_export(job1, r'Z:/share/temp')
    asw.g_export(job1, temp_path_g_export)
    # asw.delete_job(job1)
    # asw.delete_job(job2)

    # 开始查看比对结果
    # 先解压
    temp_path_ze = r'C:\cc\share\{}\ze'.format('temp' + "_" + str(job_id) + "_" + vs_time_g)
    job_operation.untgz(os.path.join(temp_path_ze, os.listdir(temp_path_ze)[0]), temp_path)
    all_result = {}
    for layer in all_layer_g:
        pass
        print(layer)
        layer_result = asw.layer_compare_analysis_temp_path(jobpath1, step1, layer, jobpath2, step2, layer, layer2_ext,
                                                            tol,
                                                            layer + '-com', map_layer_res, temp_path)
        # print(layer_result)

        all_result[layer] = layer_result

        for each in all_layer_from_org:
            # print("each[0]:",each[0])
            # print("layer:",layer,"str(each[0]):",str(each[0]).lower().replace(" ","-").replace("(","-").replace(")","-"))
            if layer == str(each[0]).lower().replace(" ", "-").replace("(", "-").replace(")", "-"):
                print("I find it!!!!!!!!!!!!!!")
                print(layer_result, type(layer_result))
                # layer_result_dict=json.loads(layer_result)
                # print(layer_result_dict)
                # print(len(layer_result_dict["result"]))

                try:
                    # print('layer_result_dict["result"]:',layer_result_dict["result"])
                    if layer_result == "正常":
                        print(layer,"比对通过！")
                    elif layer_result == "错误":
                        print(layer,"未通过！")
                        g_vs_total_result_flag = False
                    elif layer_result == "未比对":
                        print(layer,"未比对！")
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
        json.dump(all_result, f,indent=4, ensure_ascii=False)



    # 删除temp_path
    # if os.path.exists(temp_path):
    #     shutil.rmtree(temp_path)

    # if os.path.exists(r'C:\cc\share\temp' + "_" + str(request.user) + "_" + str(job_id)):
    #     shutil.rmtree(r'C:\cc\share\temp' + "_" + str(request.user) + "_" + str(job_id))
    data={}
    data["vs_time_g"] = vs_time_g
    data["job_id"]=job_id
    data["all_result"]=all_result

    print(data)

    assert g_vs_total_result_flag == True

    for key in all_result:
        print(key + ':' + all_result[key])
        assert all_result[key] == "正常"


@pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
def test_gerber_to_odb_ep_local_convert(job_id,prepare_test_job_clean_g):
    print("G软件VS开始啦！")
    asw = Asw(r"C:\EPSemicon\cc\gateway.exe")#拿到G软件

    data = {}#存放当前测试料号的每一层的比对结果。
    g_vs_total_result_flag = True  # True表示最新一次G比对通过
    vs_time_g = str(int(time.time()))#比对时间
    data["vs_time_g"] = vs_time_g#比对时间存入字典
    data["job_id"] = job_id

    #准备好临时目录
    temp_path = RunConfig.temp_path_base + "_" + str(job_id) + "_" + vs_time_g
    temp_gerber_path = os.path.join(temp_path, 'gerber')
    temp_ep_path = os.path.join(temp_path, 'ep')
    temp_g_path = os.path.join(temp_path, 'g')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    if not os.path.exists(temp_gerber_path):
        os.mkdir(temp_gerber_path)
    if not os.path.exists(temp_ep_path):
        os.mkdir(temp_ep_path)
    if not os.path.exists(temp_g_path):
        os.mkdir(temp_g_path)

    #下载并解压原始gerber文件
    DMS().get_file_from_dms_db(temp_path, job_id, field='file_compressed', decompress='rar')

    file_path_gerber = os.listdir(temp_gerber_path)[0]
    job_name = file_path_gerber + '_ep'
    step = 'orig'
    file_path = os.path.join(temp_gerber_path, file_path_gerber)
    out_path = os.path.join(temp_path, 'ep')

    # 悦谱转图，先清空同名料号
    epcam_api.close_job(job_name)
    EpGerberToODB().ep_gerber_to_odb_pytest(job_name, step, file_path, out_path, job_id)

    #下载G转图tgz，并解压好
    DMS().get_file_from_dms_db(temp_path, job_id, field='file_odb_g', decompress='tgz')

    # 打开job_ep
    job_ep_name = os.listdir(temp_ep_path)[0]
    res = job_operation.open_job(temp_ep_path, job_ep_name)
    print("open ep result:", res)
    print("job_ep_layer:", job_operation.get_all_layers(job_ep_name))
    if len(job_operation.get_all_layers(job_ep_name)) == 0:
        g_vs_total_result_flag = False
        print("最新-EP-ODB++打开失败！！！！！")

    # 打开job_g
    job_g_name = os.listdir(temp_g_path)[0]
    print("temp_g_path:", temp_g_path, "job_g_name:", job_g_name)
    job_operation.open_job(temp_g_path, job_g_name)
    print("open g result:", res)
    print("job_g_layer:", job_operation.get_all_layers(job_g_name))
    if len(job_operation.get_all_layers(job_g_name)) == 0:
        g_vs_total_result_flag = False
        print("G-ODB++打开失败！！！！！")



    step = "orig"
    # 原始层文件信息，最全的
    ans = DMS().get_job_layer_fields_from_dms_db_pandas(job_id,field='layer_org')
    all_layer_from_org = [each for each in ans]
    print("all_layer_from_org:", all_layer_from_org)

    # 以G软件解析好的为主，来VS
    all_layer_g = job_operation.get_all_layers(job_g_name)
    print('G软件tgz中的层信息：', all_layer_g)

    all_layer_ep = job_operation.get_all_layers(job_ep_name)
    print('悦谱软件tgz中的层信息：', all_layer_ep)

    if len(all_layer_g) == 0:
        pass
        g_vs_total_result_flag = False

    if len(all_layer_ep) == 0:
        pass
        g_vs_total_result_flag = False

    # g_temp_path = r'Z:/share/temp' + "_" + str(request.user) + "_" + str(job_id)
    g_temp_path = r'\\vmware-host\Shared Folders\share/temp'
    rets = []
    paras = {}

    job1 = os.listdir(os.path.join(temp_path, 'g'))[0]
    # jobpath1 = r'Z:/share/temp_{}_{}/g/{}'.format(str(request.user),str(job_id),job1)
    # jobpath1 = r'\\vmware-host\Shared Folders\share/temp/g/{}'.format(job1)
    jobpath1 = r'\\vmware-host\Shared Folders\share/{}/g/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job1)
    step1 = 'orig'
    layer1 = 'bottom.art'

    job2 = os.listdir(os.path.join(temp_path, 'ep'))[0]

    # jobpath2 = r'Z:/share/temp_{}_{}/ep/{}'.format(str(request.user),str(job_id),job2)
    # jobpath2 = r'\\vmware-host\Shared Folders\share/temp/ep/{}'.format(job2)
    jobpath2 = r'\\vmware-host\Shared Folders\share/{}/ep/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job2)
    step2 = 'orig'
    layer2 = 'bottom.art'

    layer2_ext = '_copy'

    # 读取配置文件
    with open(r'C:\EPSemicon\cc\config.json', encoding='utf-8') as f:
        cfg = json.load(f)
    tol = cfg['job_manage']['vs']['vs_tol_g']
    print("tol:", tol)
    map_layer = layer2 + '-com'
    map_layer_res = 200

    print("job1:", job1, "job2:", job2)

    # 先删除同名料号
    asw.delete_job(job1)
    asw.delete_job(job2)

    asw.import_odb_folder(jobpath1)  # 导入要比图的资料,G的
    asw.import_odb_folder(jobpath2)  # 导入要比图的资料，悦谱的

    asw.layer_compare_g_open_2_job(jobpath1, step1, layer1, jobpath2, step2, layer1, layer2_ext, tol, map_layer,
                                   map_layer_res)
    for layer in all_layer_g:
        print("g_layer:", layer)
        print("比对参数", job_g_name, step, layer, job_ep_name, step, layer)
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

    asw.layer_compare_close_job(jobpath1, step1, layer1, jobpath2, step2, layer2, layer2_ext, tol, map_layer,
                                map_layer_res)

    temp_path_g_export = r'//vmware-host/Shared Folders/share/{}/ze'.format(
        'temp' + "_" + str(job_id) + "_" + vs_time_g)

    if not os.path.exists(os.path.join(temp_path, 'ze')):
        os.mkdir(os.path.join(temp_path, 'ze'))
    # asw.g_export(job1, r'Z:/share/temp')
    asw.g_export(job1, temp_path_g_export)
    # asw.delete_job(job1)
    # asw.delete_job(job2)

    # 开始查看比对结果
    # 先解压
    temp_path_ze = r'C:\cc\share\{}\ze'.format('temp' + "_" + str(job_id) + "_" + vs_time_g)
    job_operation.untgz(os.path.join(temp_path_ze, os.listdir(temp_path_ze)[0]), temp_path)
    all_result = {}
    for layer in all_layer_g:
        pass
        print(layer)
        layer_result = asw.layer_compare_analysis_temp_path(jobpath1, step1, layer, jobpath2, step2, layer, layer2_ext,
                                                            tol,
                                                            layer + '-com', map_layer_res, temp_path)
        # print(layer_result)

        all_result[layer] = layer_result

        for each in all_layer_from_org:
            # print("each[0]:",each[0])
            # print("layer:",layer,"str(each[0]):",str(each[0]).lower().replace(" ","-").replace("(","-").replace(")","-"))
            if layer == str(each[0]).lower().replace(" ", "-").replace("(", "-").replace(")", "-"):
                print("I find it!!!!!!!!!!!!!!")
                print(layer_result, type(layer_result))
                # layer_result_dict=json.loads(layer_result)
                # print(layer_result_dict)
                # print(len(layer_result_dict["result"]))

                try:
                    # print('layer_result_dict["result"]:',layer_result_dict["result"])
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
    # if os.path.exists(temp_path):
    #     shutil.rmtree(temp_path)

    # if os.path.exists(r'C:\cc\share\temp' + "_" + str(request.user) + "_" + str(job_id)):
    #     shutil.rmtree(r'C:\cc\share\temp' + "_" + str(request.user) + "_" + str(job_id))
    data = {}
    data["vs_time_g"] = vs_time_g
    data["job_id"] = job_id
    data["all_result"] = all_result

    print(data)

    assert g_vs_total_result_flag == True

    for key in all_result:
        print(key + ':' + all_result[key])
        assert all_result[key] == "正常"
