import os,sys,shutil,time,math
epcam_path=os.path.dirname(os.path.realpath(__file__))+r"\epcam"
if epcam_path not in sys.path:
    sys.path.append(epcam_path)
import epcam_api as epcam_api
import epcam
import json
import tarfile as tf
#import rarfile as rf
import zipfile as zf


def open_job(path, job):
    """打开料号
    :param     path(str): 料号路径
    :param     job(str): 料号名 
    :returns   :None 
    :raises    error:
    """
    try:
       return  epcam_api.open_job(path, job)
        
    except Exception as e:
        print(e)


def save_job(job):
    """保存料号
    :param     job(str): 料号名 
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.save_job(job)
    except Exception as e:
        print(e)


def create_step(job, step):
    """创建step
    :param     job(str): 料号名 
    :param     step(str): step名 
    :returns   :None 
    :raises    error:
    """
    try:
        index = -1                  #默认创建在末尾
        epcam_api.create_step(job, step, index)
    except Exception as e:
        print(e)


def create_layer(job, layer):
    """创建层
    :param     job(str): 料号名 
    :param     layer(str): 层名 
    :returns   :None 
    :raises    error:
    """
    try:
        index = -1                  #默认创建在末尾
        step = ''                   #在所有层创建
        epcam_api.create_new_layer(job, step, layer, index)
    except Exception as e:
        print(e)


def rename_job(old_jobname, new_jobname):
    """job重命名
    :param     old_jobname(str): 原料号名 
    :param     new_jobname(str): 新料号名 
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.job_rename(old_jobname, new_jobname)
    except Exception as e:
        print(e)


def rename_step(jobname, old_step_name, new_step_name):
    """step重命名
    :param     jobname(str): 料号名 
    :param     old_step_name(str): 原step名 
    :param     new_step_name(str): 新step名 
    :returns   :None 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        old_step_index = step_infos.index(old_step_name) + 1
        old_layer_index = -1
        new_layer_info = ''
        epcam_api.change_matrix(jobname, old_step_index, old_layer_index, new_step_name, new_layer_info)
    except Exception as e:
        print(e)


def rename_layer(jobname, old_layer_name, new_layer_name, context = ''):
    """layer重命名
    :param     jobname(str): 料号名 
    :param     old_layer_name(str): 原layer名 
    :param     new_layer_name(str): 新layer名 
    :param     context(str): context值（board或misc)
    :returns   :None 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        new_step_name = ''
        old_step_index = -1
        old_layer_info = {}
        old_layer_index = -1
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == old_layer_name:
                old_layer_info = layer_infos[i]
                old_layer_index = i + 1
            if layer_infos[i]['start_name'] == old_layer_name:
                new_info = layer_infos[i]
                new_info['start_name'] = new_layer_name
                epcam_api.change_matrix(jobname, old_step_index, i+1, new_step_name, new_info)  
            if layer_infos[i]['end_name'] == old_layer_name:
                new_info = layer_infos[i]
                new_info['end_name'] = new_layer_name
                epcam_api.change_matrix(jobname, old_step_index, i+1, new_step_name, new_info)  
        old_layer_info['name']  = new_layer_name
        if context != '':
            old_layer_info['context'] = context
        new_layer_info = old_layer_info
        epcam_api.change_matrix(jobname, old_step_index, old_layer_index, new_step_name, new_layer_info)   
        
    except Exception as e:
        print(e)


def open_layer(job, step, layer):
    """打开layer
    :param     job(str): 料号名 
    :param     step(str): step名 
    :param     layer(str): layer名 
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.open_layer(job, step, layer)
    except Exception as e:
        print(e)
        return 0


def copy_layer(jobname, old_layer_name):#jobname, org_layer_index, dst_layer, poi_layer_index
    """拷贝layer
    :param     jobname(str): 料号名 
    :param     old_layer_name(str): 原layer名 
    :returns   :None 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == old_layer_name:
                old_layer_index = i + 1
        dst_layer = ''
        #新建空layer
        create_layer(jobname, 'jbz')
        ret2 = epcam_api.copy_layer(jobname, old_layer_index, dst_layer, len(layer_infos) + 1)
        data2 = json.loads(ret2)
        new_layer = data2['paras']['newname']
        #删除新层
        delete_layer(jobname, 'jbz')
        return new_layer
    except Exception as e:
        print(e)
        print('123456')
    return ''


def delete_job(jobname):
    """删除料号
    :param     jobname(str): 料号名 
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.job_delete(jobname)
    except Exception as e:
        print(e)


def load_json(path):
    """读json文件
    :param     path(str): 路径
    :returns   json_data(str):文件内容 
    :raises    error:
    """
    try:
        with open(path, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
            return json_data
    except Exception as e:
        print(e)
    return ""


def transform_range_data(json_data):
    """读到的range值转为float
    :param     json_data(str)
    :returns   :None 
    :raises    error:
    """
    try:
        data = json_data['rangesList']
        for i in range(len(data)):
            data[i]['RedLv'] = float(data[i]['RedLv'])
            data[i]['YellowLv'] = float(data[i]['YellowLv'])
            data[i]['GreenLv'] = float(data[i]['GreenLv'])
        return json.dumps(data)
    except Exception as e:
        print(e)
    return ""


def insert_layer(job, poi_layer_index):
    """插入layer(matrix)
    :param     job(str):料号名
    :param     poi_layer_index(int):插入层的序号
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.insert_layer(job, poi_layer_index)
    except Exception as e:
        print(e)
    return 0  


def delete_Z_file(path, job):
    """删除copy之后的layer文件夹下的.Z文件
    :param     path(str):路径
    :param     job(str):料号名
    :returns   :None 
    :raises    error:
    """
    layers_path = path + '\\' + job + r'\steps\pcb\layers'
    filelist = os.listdir(layers_path)
    for file in filelist:
        _path = layers_path + '\\' + file + '\\features.Z'
        if os.path.isfile(_path):
            os.remove(_path)
  

def copy_step(job, old_step_name):
    """复制Step
    :param     job(str):料号名
    :param     old_step_name(str):原step名
    :returns   new_step(str):新step名 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        
        for i in range(0, len(step_infos)):
            if step_infos[i] == old_step_name:
                old_step_index = i + 1
        epcam_api.insert_step(job, old_step_index+1)
        dst_step = ''
        #新建空
        create_step(job, 'jbz')
        ret2 = epcam_api.copy_step(job, old_step_index, dst_step, len(step_infos) + 1)
        data2 = json.loads(ret2)
        new_step = data2['paras']['newname']
        #删除新层
        delete_step(job, 'jbz')
        # ret2 = epcam_api.copy_step(job, old_step_index, dst_step, old_step_index+1)
        # data2 = json.loads(ret2)
        # new_step = data2['paras']['newname']
        return new_step
    except Exception as e:
        print(e)
    return ''


def insert_step(job, poi_step_index):
    """插入step(matrix)
    :param     job(str):料号名
    :param     poi_step_index(int):新增step的序号
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.insert_step(job, poi_step_index)
    except Exception as e:
        print(e)
    return 0 


def maketgz(ifn, out_path, file_name):
    """压缩文件夹为tgz
    :param     ifn(str):导入路径
    :param     out_path(str):导出路径
    :param     file_name(str):文件名
    :returns   :None 
    :raises    error:
    """
    try:
        ifn = ifn.split(sep = '"')[1]
    except:
        pass
    file_real_name = file_name.split('.')[0]
    ofn = out_path + '\\' + file_name #+ '.tgz'
    #最外层后缀也为tar, 然后再rename为tgz
    out_ofn = out_path + '\\' + file_real_name + '.tar'
    #with tf.open(ofn, 'w:gz') as tar:
    print("*" * 100, "out_ofn:", out_ofn, "ifn:", ifn)
    with tf.open(out_ofn, 'w:gz') as tar:
        tar.add(ifn, arcname = os.path.basename(ifn))
    if os.path.exists(ofn):
        os.remove(ofn)
    os.rename(out_ofn, ofn)
    print('compress success!')
        #os.system('pause')

    return 0 


def delete_layer(job, layername):
    """删除layer
    :param     job(str):料号名
    :param     layername(str):层名
    :returns   :None 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layername:
                layer_index = i + 1
                epcam_api.delete_layer(job, layer_index)
                break
    except Exception as e:
        print(e)
    return 0 


def untgz(ifn, untgz_path):
    """解压tgz文件到指定目录
    :param     ifn(str):解压导入路径
    :param     untgz_path(str):解压后存放路径
    :returns   :None 
    :raises    error:
    """
    try:
        ifn = ifn.split(sep = '"')[1]
    except:
        pass
    ofn = untgz_path
    #with tf.open(ifn, 'r:gz') as tar:
    tar = tf.open(ifn)
    for tarinfo in tar:
        if os.path.exists(os.path.join(ofn, tarinfo.name)):
            for root, dirs, files in os.walk(os.path.join(ofn, tarinfo.name), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        tar.extract(tarinfo.name, ofn)
    print('uncompress success!')
    return os.path.dirname(tarinfo.name)
    #os.system('pause')
    return 


def traverse_dirs(ifn):
    """查看文件夹下所有子文件夹和文件
    :param     ifn(str):遍历路径
    :returns   dirs(list):路径下的所有文件夹和文件名 
    :raises    error:
    """
    try:
        dirs = os.listdir(ifn)
        return dirs
    except Exception as e:
        print(e)
    return 0 



def traverse_files(ifn, filetype):
    """遍历文件夹下指定文件类型文件名
    :param     ifn(str):遍历文件夹的路径
    :param     filetype(str):文件类型
    :returns   :None 
    :raises    error:
    """
    try:
        file_name = []
        for root, dirs, files in os.walk(ifn):
            for name in files:
                if filetype in name:
                    file_name.append(name)
        return file_name
    except Exception as e:
        print(e)
    return 0 


def delete_step(job, stepname):
    """删除step
    :param     job(str):job名
    :param     stepname(str):step名
    :returns   :None 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        for i in range(0, len(step_infos)):
            if step_infos[i] == stepname:
                step_index = i + 1
        epcam_api.delete_step(job, step_index)
    except Exception as e:
        print(e)
    return 0 


def job_delete(ofn, jobname):
    """删除指定目录下的指定文件名的料
    :param     ofn(str):路径
    :param     jobname(str):job名
    :returns   :None 
    :raises    error:
    """
    try:
        if os.path.exists(os.path.join(ofn, jobname)):
            for root, dirs, files in os.walk(os.path.join(ofn, jobname), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(os.path.join(ofn, jobname))
    except Exception as e:
        print(e)
    return 0 


def load_layer(jobname, stepname, layername):
    """加载层
    :param     jobname(str):job名
    :param     stepname(str):step名
    :param     layername(str):layer名
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.load_layer(jobname, stepname, layername)
    except Exception as e:
        print(e)
    return 0 


def get_all_steps(job):
    """获取step列表
    :param     job(str):job名
    :returns   steps(list):所有step名 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        steps = data['paras']['steps']
        return steps
    except Exception as e:
        print(e)
    return []


def get_all_layers(job):
    """获取layer列表
    :param     job(str):job名
    :returns   layers(list):所有layer名 
    :raises    error:
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_infos)):
            layer_list.append(layer_infos[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
    return []


def file_identify(path):
    """识别文件
    :param     path(str):路径
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.file_identify(path)
    except Exception as e:
        print(e)

#料号另存为     有问题
def file_identify(path):
    """打开料号
    :param     path(str):路径
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.file_identify(path)
    except Exception as e:
        print(e)


def open_eps(job, path):
    """打开eps
    :param     job(str):job名
    :param     path(str)：打开路径
    :returns   :None 
    :raises    error:
    """
    try:
        return epcam_api.open_eps(job, path)
    except Exception as e:
        print(e)

# #解压rar文件
# def unrar(file_path, dest_path):
#     try:
#         rar_file = rf.RarFile(file_path)
#         rar_file.extractall(dest_path)
#         #rar_file.close()
#     except Exception as e:
#         print(e)


def unzip(file_path, dest_path):
    """解压zip文件
    :param     file_path(str):压缩包路径
    :param     dest_path(str)：解压后存放路径
    :returns   :None 
    :raises    error:
    """
    try:
        zip_file = zf.ZipFile(file_path)
        zip_file.extractall(dest_path)
        zip_file.close()
    except Exception as e:
        print(e)


def job_create(job):
    """创建料号（无路径）
    :param     job(str):料号名
    :returns   :None 
    :raises    error:
    """
    try:
        epcam_api.job_create(job)
    except Exception as e:
        print(e)


def identify_eps(job, path):
    """识别eps
    :param     job(str):料号名
    :param     path(str):路径
    :returns   result(str):结果 
    :raises    error:
    """
    try:
        return epcam_api.identify_eps(job, path)
    except Exception as e:
        print(e)

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
    """转为Gerber文件
    :param     job(str):job名
    :param     step(str):step名
    :param     file_path(str):文件路径
    :param     index(int):序号
    :returns   :None
    :raises    error:
    """
    for root, dirs, files in os.walk(file_path):
        epcam_api.file_translate_init(job)
        for file in files:
            if is_chinese(file):
                os.rename(file_path+r'/'+file,file_path+r'/''unknow'+str(index))
                file='unknow'+str(index)
                index=index+1
            ret = epcam_api.file_identify(os.path.join(root, file))
            data = json.loads(ret)
            file_format = data['paras']['format']
            file_param = data['paras']['parameters']
            #file_param['text_line_width'] = '{:.2f}'.format(file_param['text_line_width'])
            if file_format == 'Gerber274x' or file_format == 'Excellon2' or file_format == 'DXF':
                print(file)
                re = epcam_api.file_translate(os.path.join(root, file), job, step, file, file_param, '', '', '', [])    #translate
                
                # job_operation.save_job(job)
        for dir_name in dirs:
            Traverse_Gerber(job, step, os.path.join(root,dir_name),index)


def job_save_by_num(job,path,num):
    """按步骤保存job
    :param     job(str):job名
    :param     path(str):文件路径
    :param     num(int):
    :returns   :None
    :raises    error:
    """
    num=str(num)
    filepath=path+'/'+num
    if os.path.exists(filepath):
        shutil.rmtree(filepath)
        os.makedirs(filepath)
        epcam_api.save_job_as(job,filepath)
    else:
        os.makedirs(filepath)
        epcam_api.save_job_as(job,filepath)


def open_job_by_num(job,path,currentnum,backnum):
    """打开回退步骤的job
    :param     job(str):job名
    :param     path(str):文件路径
    :param     currentnum(int):当前步骤
    :param     currentnum(int):回退后步骤
    :returns   :None
    :raises    error:
    """
    for i in range(backnum+1,currentnum):
        filepath=path+'/'+str(i)
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
    backnum=str(backnum)
    filepath=path+'/'+backnum
    epcam_api.open_job(filepath,job)

def show_layer(job,step):
    """用脚本打开软件，默认显示第一层
    :param     job(str):job名
    :param     step(str):step名
    :returns   :None
    :raises    error:
    """
    ret = epcam_api.get_matrix(job)
    data = json.loads(ret)
    layer_list = []
    layer_info = data['paras']['info']
    if len(layer_info):#遍历获取layer_name
        for i in range(0, len(layer_info)):
            layer_list.append(layer_info[i]['name'])
    layer=layer_list[0]
    datashow = {"cmd":"show_layer", "job":job, "step": step, "layer":layer}
    js = json.dumps(datashow)
    epcam.view_cmd(js)

def get_sr_limit(job,step): #获取拼版中最小和最大坐标
    repeat_infos=epcam_api.get_step_repeat(job,step)    #获取拼板信息
    repeat_infos=json.loads(repeat_infos)
    repeat_infos=repeat_infos['result']
    xminlist=[]
    yminlist=[]
    xmaxlist=[]
    ymaxlist=[]
    for repeat_info in repeat_infos:
        repeat_infox=repeat_info['X']
        repeat_infoy=repeat_info['Y']
        set_box=epcam_api.get_profile_box(job, repeat_info['NAME'])
        set_box=json.loads(set_box)['paras']
        datum_x=json.loads(epcam_api.get_step_header_infos(job, repeat_info['NAME']))['x_datum']
        datum_y=json.loads(epcam_api.get_step_header_infos(job, repeat_info['NAME']))['y_datum']
        x_offset = repeat_infox - datum_x
        y_offset = repeat_infoy - datum_y
        pts=[]
        pts.append([set_box['Xmin']+x_offset,set_box['Ymin']+y_offset])
        pts.append([set_box['Xmin']+x_offset,set_box['Ymax']+y_offset])
        pts.append([set_box['Xmax']+x_offset,set_box['Ymax']+y_offset])
        pts.append([set_box['Xmax']+x_offset,set_box['Ymin']+y_offset])
        width=set_box['Xmax']-set_box['Xmin']
        height=set_box['Ymax']-set_box['Ymin']
        if repeat_info['MIRROR']:
            pts.clear()
            pts.append([set_box['Xmin']+x_offset-width,set_box['Ymin']+y_offset])
            pts.append([set_box['Xmin']+x_offset-width,set_box['Ymax']+y_offset])
            pts.append([set_box['Xmin']+x_offset,set_box['Ymax']+y_offset])
            pts.append([set_box['Xmin']+x_offset,set_box['Ymin']+y_offset])

        if repeat_info['ANGLE']!=0:
            value = math.acos(-1) / 180
            ratio = -1 * repeat_info['ANGLE'] * value
            if repeat_info['MIRROR']:
                ratio = -1 * (360-repeat_info['ANGLE']) * value
            for pt in pts:
                a = pt[0]
                b = pt[1]
                pt[0]=(a - repeat_infox)*math.cos(ratio) - (b - repeat_infoy)*math.sin(ratio) + repeat_infox
                pt[1]=(a - repeat_infox)*math.sin(ratio) + (b - repeat_infoy)*math.cos(ratio) + repeat_infoy
        allx=[]
        ally=[]
        for pt in pts:
            allx.append(pt[0])
            ally.append(pt[1])
        allx.sort()
        ally.sort()
        xmin=allx[0]
        ymin=ally[0]
        set_length=allx[-1]-allx[0]
        set_width=ally[-1]-ally[0]    
        length= (repeat_info['NX']-1)*repeat_info['DX']+set_length
        width = (repeat_info['NY']-1)*repeat_info['DY']+set_width
        xmax=xmin+length
        ymax=ymin+width
        xminlist.append(xmin)
        yminlist.append(ymin)
        xmaxlist.append(xmax)
        ymaxlist.append(ymax)
    xminlist.sort()
    yminlist.sort()
    xmaxlist.sort(reverse=True)
    ymaxlist.sort(reverse=True)
    gSRxmin=xminlist[0]/1000000
    gSRymin=yminlist[0]/1000000
    gSRxmax=xmaxlist[0]/1000000
    gSRymax=ymaxlist[0]/1000000
    infos={}
    infos['gSRxmin']=gSRxmin
    infos['gSRymin']=gSRymin
    infos['gSRxmax']=gSRxmax
    infos['gSRymax']=gSRymax
    return infos

def new_show_layer(job,step):
    """用脚本打开软件，默认显示第一层
    :param     job(str):job名
    :param     step(str):step名
    :returns   :None
    :raises    error:
    """
    ret = api.get_matrix(job)
    data = json.loads(ret)
    layer_list = []
    layer_info = data['paras']['info']
    # if len(layer_info):#遍历获取layer_name
    #     for i in range(0, len(layer_info)):
    #         layer_list.append(layer_info[i]['name'])
    layer=layer_info[0]['name']
    datashow = {"cmd":"show_layer", "job":job, "step": step, "layer":layer}
    js = json.dumps(datashow)
    epcam.view_cmd(js)

def new_open_job(path, jobname):
    """打开料号 \n
    详细描述： 将ODB++类型的料号读入到内存中\n
    :param     path(str): 料名 \n
    :param     jobname(str): step名 \n
    return      True/False
    Usage：    job_operation.open_job(r'C:/job','out')
    """
    try:
        ret = epcam_api.open_job(path, jobname)
        data = json.loads(ret)
        return data['paras']['status']
    except Exception as e:
        print(e)
        return False