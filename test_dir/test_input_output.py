import os, time,json,shutil,sys
from cc import cc_method
from cc.cc_method import GetTestData,DMS,Print,getFlist
import pytest
from config_ep.epcam import job_operation,epcam_api
from config_ep.epcam_cc_method import EpGerberToODB,Information
from config_g.g_cc_method import Asw
from config import RunConfig
from pathlib import Path



@pytest.mark.parametrize("job_id", GetTestData().get_job_id('Input'))
def test_gerber_to_odb_ep_local_convert_drill_none_2_4(job_id,prepare_test_job_clean_g):
    Print.print_with_delimiter("G软件VS开始啦！")
    asw = Asw(RunConfig.gateway_path)#拿到G软件
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
    job_name = os.listdir(temp_gerber_path)[0].lower()
    file_path_gerber = os.path.join(temp_gerber_path, os.listdir(temp_gerber_path)[0])
    out_path = temp_ep_path
    EpGerberToODB().ep_gerber_to_odb_pytest(job_name_ep, 'orig', file_path_gerber, out_path, job_id)

    #下载G转图tgz，并解压好
    DMS().get_file_from_dms_db(temp_path, job_id, field='file_odb_g', decompress='tgz')

    # 打开job_ep
    job_ep_name = os.listdir(temp_ep_path)[0]
    print("job_name_ep,job_ep_name:",job_name_ep,job_ep_name)
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
    job_g_g_path = r'\\vmware-host\Shared Folders\share/{}/g/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job_g_name)
    # job_g_g_path = r'Z:/share/{}/g/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job_g_name)
    job_ep_g_path = r'\\vmware-host\Shared Folders\share/{}/ep/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g, job_ep_name)
    # job_ep_g_path = r'Z:/share/{}/ep/{}'.format('temp' + "_" + str(job_id) + "_" + vs_time_g,job_ep_name)
    # 读取配置文件
    with open(r'C:\cc\python\epwork\epcam_test_client\config_g\config.json', encoding='utf-8') as f:
        cfg = json.load(f)
    tol = cfg['job_manage']['vs']['vs_tol_g']
    print("tol:", tol)
    map_layer_res = 200
    print("job1:", job_g_name, "job2:", job_ep_name)

    # 导入要比图的资料
    print("job_g_g_path:",job_g_g_path,Path(job_g_g_path))
    asw.import_odb_folder(job_g_g_path)
    asw.import_odb_folder(job_ep_g_path)
    #G打开要比图的2个料号
    job_g_name = job_g_name.lower()
    job_ep_name = job_ep_name.lower()
    asw.layer_compare_g_open_2_job(job1=job_g_name, step='orig',job2=job_ep_name)
    g_compare_result_folder = 'g_compare_result'
    temp_g_compare_result_path = os.path.join(temp_path, g_compare_result_folder)
    if not os.path.exists(temp_g_compare_result_path):
        os.mkdir(temp_g_compare_result_path)
    temp_path_remote_g_compare_result = r'//vmware-host/Shared Folders/share/{}/{}'.format(
        'temp' + "_" + str(job_id) + "_" + vs_time_g,g_compare_result_folder)
    temp_path_local_g_compare_result = os.path.join(temp_path,g_compare_result_folder)

    all_result_g = {}
    for layer in all_layer_g:
        # print("g_layer:", layer)
        if layer in all_layer_ep:
            map_layer = layer + '-com'
            result = asw.layer_compare_one_layer(job1=job_g_name,step1='orig', layer1=layer, job2=job_ep_name, step2='orig', layer2=layer, layer2_ext='_copy', tol=tol,
                                                  map_layer=map_layer, map_layer_res=map_layer_res,result_path_remote=temp_path_remote_g_compare_result,
                                                 result_path_local=temp_path_local_g_compare_result,
                                                 temp_path=temp_path)
            all_result_g[layer] = result
            if result != "正常":
                g_vs_total_result_flag = False
        else:
            pass
            print("悦谱转图中没有此层")
    asw.save_job(job_g_name)
    asw.save_job(job_ep_name)
    asw.layer_compare_close_job(job1=job_g_name, job2=job_ep_name)

    # 开始查看比对结果
    # 获取原始层文件信息，最全的
    all_layer_from_org = [each for each in DMS().get_job_layer_fields_from_dms_db_pandas(job_id, field='layer_org')]
    all_result = {}#all_result存放原始文件中所有层的比对信息
    for layer_org in all_layer_from_org:
        layer_org_find_flag = False
        layer_org_vs_value = ''
        for each_layer_g_result in all_result_g:
            if each_layer_g_result == str(layer_org).lower().replace(" ", "-").replace("(", "-").replace(")", "-"):
                layer_org_find_flag = True
                layer_org_vs_value = all_result_g[each_layer_g_result]
        if layer_org_find_flag == True:
            all_result[layer_org] = layer_org_vs_value
        else:
            all_result[layer_org] = 'G转图中无此层'

    data["all_result_g"] = all_result_g
    data["all_result"] = all_result

    Print.print_with_delimiter("断言--看一下G转图中的层是不是都有比对结果")
    assert len(all_layer_g) == len(all_result_g)

    #----------------------------------------开始测试输出gerber功能--------------------------------------------------------
    g1_vs_total_result_flag = True
    out_put = []
    job_result = {}
    out_json = ''

    #建立output_gerber文件夹，里面用来放epcam输出的gerber。
    temp_out_put_gerber_path = os.path.join(temp_path,'output_gerber')
    if os.path.exists(temp_out_put_gerber_path):
        shutil.rmtree(temp_out_put_gerber_path)
    os.mkdir(temp_out_put_gerber_path)

    # 设置导出参数
    with open(RunConfig.config_ep_output, 'r') as cfg:
        infos_ = json.load(cfg)['paras']  # (json格式数据)字符串 转化 为字典
        _type = infos_['type']
        resize = infos_['resize']
        gdsdbu = infos_['gdsdbu']
        angle = infos_['angle']
        scalingX = infos_['scalingX']
        scalingY = infos_['scalingY']
        isReverse = infos_['isReverse']
        mirror = infos_['mirror']
        rotate = infos_['rotate']
        scale = infos_['scale']
        profiletop = infos_['profiletop']
        cw = infos_['cw']
        cutprofile = infos_['cutprofile']
        mirrorpointX = infos_['mirrorpointX']
        mirrorpointY = infos_['mirrorpointY']
        rotatepointX = infos_['rotatepointX']
        rotatepointY = infos_['rotatepointY']
        scalepointX = infos_['scalepointX']
        scalepointY = infos_['scalepointY']
        mirrordirection = infos_['mirrordirection']
        cut_polygon = infos_['cut_polygon']

    layers = Information().get_layers(job_ep_name)
    print("layers:", layers)
    steps = Information().get_steps(job_ep_name)
    print("steps:", steps)


    file_path = temp_out_put_gerber_path + '\\' + job_ep_name
    file_path_file = Path(file_path)
    print("file_path_file:", file_path_file)
    if file_path_file.exists():
        shutil.rmtree(file_path_file)  # 已存在gerber文件夹删除掉，再新建
    os.mkdir(file_path)

    # 创建料的step文件夹
    for step in steps:
        step_path = file_path + '\\' + step
        os.mkdir(step_path)

    for step in steps:
        value = {}
        # step_info={step:value}
        # 开始时间
        start_time = (int(time.time()))
        step_path = file_path + '\\' + step
        # drill_layers = Information().get_drill_layer_name(job_ep_name)#这个方法的前提是定好层别属性才行。如果没有定，可以从DMS数据库的layer表里拉信息。
        drill_layers = [each.lower() for each in DMS().get_job_layer_drill_from_dms_db_pandas_one_job(job_id)['layer'] ]
        rout_layers = [each.lower() for each in DMS().get_job_layer_rout_from_dms_db_pandas_one_job(job_id)['layer'] ]
        print("drill_layers:",drill_layers)

        other_layers = []
        layer_result = {}
        #other_layers代表是gerber
        for other_layer in layers:
            if other_layer not in drill_layers:
                other_layers.append(other_layer)
        # 输出gerber
        for layer in other_layers:
            layer_stime = (int(time.time()))
            filename = step_path + '\\' + layer  # 当前step下的每个层的gerber文件路径
            ret = epcam_api.layer_export(job_ep_name, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY,
                                         isReverse,
                                         mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY,
                                         rotatepointX,
                                         rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon)
            layer_etime = (int(time.time()))
            layer_time = layer_etime - layer_stime
            value[layer] = layer_time

        #输出excellon2
        for drill_layer in drill_layers:
            layer_stime = (int(time.time()))
            drillname = step_path + '\\' + drill_layer

            if drill_layer in rout_layers:
                Print.print_with_delimiter("我是rout")
                drill_info = epcam_api.rout2file(job_ep_name, step, drill_layer, drillname)
            else:
                drill_info = epcam_api.drill2file(job_ep_name, step, drill_layer, drillname, False)
            layer_etime = (int(time.time()))
            layer_time = layer_etime - layer_stime
            value[layer] = layer_time


    # 记录下输出step的时间
    end_time = (int(time.time()))
    time_time = end_time - start_time
    value["step_time"] = time_time
    job_result[step] = value
    print('job_result:', job_result)
    out_put.append(job_result)
    print('out_put:', out_put)
    out_path = os.path.join(temp_out_put_gerber_path, 'out_put' + '.json')
    if out_json == '':
        with open(out_path, 'w+') as f:  # 不能是a,w+会覆盖原有的，a只会追加
            f.write(json.dumps(out_put, sort_keys=True, indent=4, separators=(',', ': ')))
    else:
        with open(out_json, 'r') as h:
            ret_json = json.load(h)
            ret_json.append(job_result)
            with open(out_json, 'w+') as hh:
                hh.write(json.dumps(ret_json, sort_keys=True, indent=4, separators=(',', ': ')))
    epcam_api.close_job(job_ep_name)

    Print.print_with_delimiter('输出gerber完成')

    #-----------------------------------------开始用G软件input-------------------------------------------------
    ep_out_put_gerber_folder = os.path.join(temp_path,r'output_gerber',job_name_ep,r'orig')
    job_g2_name = job_name + '_g2'#epcam输出gerber，再用g软件input。
    step = 'orig'

    file_path = os.path.join(temp_path, ep_out_put_gerber_folder)
    print("file_path:",file_path)
    gerberList = cc_method.getFlist(file_path)
    print(gerberList)
    g_temp_path = r'//vmware-host/Shared Folders/share/temp_{}_{}'.format(job_id,vs_time_g)
    gerberList_path = []
    for each in gerberList:
        gerberList_path.append(os.path.join(g_temp_path, r'output_gerber',job_name_ep,r'orig', each))
    print(gerberList_path)

    temp_out_put_gerber_g_input_path = os.path.join(temp_path, 'g2')
    if os.path.exists(temp_out_put_gerber_g_input_path):
        shutil.rmtree(temp_out_put_gerber_g_input_path)
    os.mkdir(temp_out_put_gerber_g_input_path)
    out_path = temp_out_put_gerber_g_input_path

    asw.g_Gerber2Odb2_no_django(job_g2_name, step, gerberList_path, out_path, job_id,drill_para='epcam_default')
    # 输出tgz到指定目录
    asw.g_export(job_g2_name, os.path.join(g_temp_path,r'g2'))

    # -----------------------------------------开始用G软件比图，g1和g2-------------------------------------------------
    #再导入一个标准G转图，加个后缀1。
    job_g1_name = job_g_name + "1"
    Print.print_with_delimiter("job_g1_name")
    print(job_g1_name)
    asw.import_odb_folder(job_g_g_path,job_name=job_g1_name)
    Print.print_with_delimiter("job_g1_name2")

    g1_compare_result_folder = 'g1_compare_result'
    temp_g1_compare_result_path = os.path.join(temp_path, g1_compare_result_folder)
    if not os.path.exists(temp_g1_compare_result_path):
        os.mkdir(temp_g1_compare_result_path)
    temp_path_remote_g1_compare_result = r'//vmware-host/Shared Folders/share/{}/{}'.format(
        'temp' + "_" + str(job_id) + "_" + vs_time_g, g1_compare_result_folder)
    temp_path_local_g1_compare_result = os.path.join(temp_path, g1_compare_result_folder)

    temp_path_local_info1 = os.path.join(temp_path,'info1')
    if not os.path.exists(temp_path_local_info1):
        os.mkdir(temp_path_local_info1)

    temp_path_local_info2 = os.path.join(temp_path, 'info2')
    if not os.path.exists(temp_path_local_info2):
        os.mkdir(temp_path_local_info2)


    # 以G1转图为主来比对
    # G打开要比图的2个料号g1和g2。g1就是原始的G转图，g2是悦谱输出的gerber又input得到的
    asw.layer_compare_g_open_2_job(job1=job_g1_name, step='orig',job2=job_g2_name)
    all_result_g1 = {}
    for layer in all_layer_g:
        if layer in layers:
            map_layer = layer + '-com'
            layer_type = ""
            if layer in drill_layers:
                print("我是孔层哈！")
                layer_type = 'drill'

            #准备改一下下面这行的参数，换成job名称，不要jobpath。另外job1是已经打开了的，不需要传参数了。
            result = asw.layer_compare_one_layer(job1=job_g1_name,step1='orig', layer1=layer, job2=job_g2_name, step2='orig', layer2=layer, layer2_ext='_copy', tol=tol,
                                                  map_layer=map_layer, map_layer_res=map_layer_res,
                                                 result_path_remote=temp_path_remote_g1_compare_result,
                                                 result_path_local=temp_path_local_g1_compare_result,
                                                 layer_type=layer_type,temp_path=temp_path)
            all_result_g1[layer] = result
            if result != "正常":
                g1_vs_total_result_flag = False
        else:
            pass
            print("悦谱转图中没有此层")

    asw.save_job(job_g1_name)
    asw.save_job(job_g2_name)
    asw.layer_compare_close_job(job1=job_g1_name, job2=job_g2_name)
    data["all_result_g1"] = all_result_g1

    Print.print_with_delimiter("断言--看一下G1转图中的层是不是都有比对结果")
    assert len(all_layer_g) == len(all_result_g1)



    Print.print_with_delimiter('比对结果信息展示--开始')
    if g_vs_total_result_flag == True:
        print("恭喜您！料号导入比对通过！")
        # print("\033[1;32m 字体颜色：深黄色\033[0m")
    if g_vs_total_result_flag == False:
        print("Sorry！料号导入比对未通过，请人工检查！")
    Print.print_with_delimiter('分割线', sign='-')
    print('G转图的层：', all_result_g)
    Print.print_with_delimiter('分割线', sign='-')
    print('所有层：', all_result)
    Print.print_with_delimiter('分割线', sign='-')
    print('G1转图的层：', all_result_g1)
    Print.print_with_delimiter('比对结果信息展示--结束')


    Print.print_with_delimiter("断言--开始")
    assert g_vs_total_result_flag == True
    for key in all_result_g:
        assert all_result_g[key] == "正常"

    assert g1_vs_total_result_flag == True
    for key in all_result_g1:
        assert all_result_g1[key] == "正常"
    Print.print_with_delimiter("断言--结束")


    # 删除temp_path
    # if os.path.exists(temp_path):
    #     shutil.rmtree(temp_path)
