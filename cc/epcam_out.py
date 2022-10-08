import json
import shutil
import sys,os
import time

sys.path.append(r'C:\EPSemicon\cc\epcam')
import epcam
import job_operation,epcam_api
from epcam_cc_method_no_django import Information
from pathlib import Path

epcam.init()

if __name__ =='__main__':
    out_put = []
    job_result = {}
    out_json = ''
    #设置导出参数
    config_path = r'C:\cc\python\epwork\epcam_test_client\config_ep\outcfg.json'
    with open(config_path, 'r') as cfg:
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

    #打开料号
    temp_ep_path = r'C:\cc\share\temp_2015_1665194954\ep'
    job_ep_name = os.listdir(temp_ep_path)[0]
    job = job_ep_name
    res = job_operation.open_job(temp_ep_path, job_ep_name)
    print("open ep result:", res)
    all_layer_ep = job_operation.get_all_layers(job_ep_name)
    if len(all_layer_ep) == 0:
        g_vs_total_result_flag = False
        print("最新-EP-ODB++打开失败！！！！！")
    else:
        print('悦谱软件tgz中的层信息：', all_layer_ep)

    layers = Information().get_layers(job_ep_name)
    print("layers:", layers)
    steps = Information().get_steps(job_ep_name)
    print("steps:",steps)

    output_path = r'C:\cc\share\temp_out'
    file_path = output_path + '\\' + job_ep_name
    file_path_file = Path(file_path)
    print("file_path_file:",file_path_file)
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
        drill_layers = Information().get_drill_layer_name(job)
        other_layers = []
        layer_result = {}
        for other_layer in layers:
            if other_layer not in drill_layers:
                other_layers.append(other_layer)
        for layer in other_layers:
            layer_stime = (int(time.time()))
            ##对geber文件加.gbr后缀
            filename = step_path + '\\' + layer + '.gbr'  # 当前step下的每个层的gerber文件路径
            ret = epcam_api.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY,
                                    isReverse,
                                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY,
                                    rotatepointX,
                                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon)
            layer_etime = (int(time.time()))
            layer_time = layer_etime - layer_stime
            value[layer] = layer_time
        for drill_layer in drill_layers:
            # ，对孔文件加.drl后缀
            layer_stime = (int(time.time()))
            drillname = step_path + '\\' + drill_layer + '.drl'
            drill_info = epcam_api.drill2file(job, step, drill_layer, drillname, False)
            layer_etime = (int(time.time()))
            layer_time = layer_etime - layer_stime
            value[layer] = layer_time


    #
    # 记录下输出step的时间
    end_time = (int(time.time()))
    time_time = end_time - start_time
    value["step_time"] = time_time
    job_result[step] = value
    print('job_result:',job_result)
    out_put.append(job_result)
    print('out_put:',out_put)
    out_path = os.path.join(output_path, 'out_put' + '.json')
    if out_json == '':
        with open(out_path, 'w+') as f:  # 不能是a,w+会覆盖原有的，a只会追加
            f.write(json.dumps(out_put, sort_keys=True, indent=4, separators=(',', ': ')))
    else:
        with open(out_json, 'r') as h:
            ret_json = json.load(h)
            ret_json.append(job_result)
            with open(out_json, 'w+') as hh:
                hh.write(json.dumps(ret_json, sort_keys=True, indent=4, separators=(',', ': ')))
    epcam_api.close_job(job)

