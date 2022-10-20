import os,sys
epcam_path=os.path.dirname(os.path.realpath(__file__))+r"\epcam"
if epcam_path not in sys.path:
    sys.path.append(epcam_path)
import epcam_api as epcam_api
import json
import job_operation


def get_drill_layer_name(job):
    """获取孔层layer名

    详细描述:获取孔层layer名

    :param     job(str): 料名 \n
    :returnp   drill_list(list): 孔层名列表 \n
    :returnt   drill_list(list): list \n
    :raises    error: \n
    Usage:    
               job = 'g058c-965a' 
               get_drill_layer_name(job) -> ["drl1","drl2"]
    """
    try:
        ret = epcam_api.get_graphic(job)
        data = json.loads(ret)
        drill_list = []
        layer_info = data['paras']['info']
        for i in range(0, len(layer_info)):
            if layer_info[i]['type'] == 'drill' and layer_info[i]['context'] == 'board':
                drill_list.append(layer_info[i]['name'])
        return drill_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''


def set_attribute_filter(logic, attribute_list):
    """设置属性筛选

    详细描述：设置属性筛选

    :param     logic(int): 决定筛选器按属性筛选时，按属性列表全部满足筛选还是有其一进行筛选 \n 
                           0 ：全部满足  1：有其一 \n
    :param     attribute_list(list): 要设置的属性列表 \n
    :returns   :None \n
    :raise     error: \n

    Usage: set_attribute_filter(0,[{".fiducial_name":"cle"},{".foot_down":""}])
    """
    try:
        epcam_api.filter_set_attribute(logic, attribute_list)
    except Exception as e:
        print(e)
    return 0


def set_size_filter(symbols):
    """设置symbol大小筛选

    详细描述:设置symbol大小筛选 \n
    :param     symbols(list):symbolname 列表 \n
    :return    :None \n
    :raises    error: \n

    Usage:     set_size_filter(['r62.992','r124.016'])
    """
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        #attributes_list = []
        #for i in range(0, len(select_param['attributes_value'])):
           # for key, value in select_param['attributes_value'][i].items():
                #attributes_list.append([key,value])
        epcam_api.set_select_param(select_param['featuretypes'], True, symbols, 
                                select_param['minline'], select_param['maxline'],
                                select_param['dcode'], select_param['attributes_flag'],
                                select_param['attributes_value'], select_param['profile_value'],
                                select_param['use_selection'])
    except Exception as e:
        print(e)
    return 0

def set_include_symbol_filter(symbol_list):
    """设置include symbol筛选\n
    详细描述：   只有pad,line, arc有symbolname\n
    :param     symbol_list(list):设置筛选include_symbol的列表\n 
    :returns   :None \n
    :raises    error:
    Usage：    layer_info.set_include_symbol_filter(['r39.370','r92.520'])
    """
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        featuretype = select_param['featuretypes']
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        if symbol_list == '':
            epcam_api.set_select_param(featuretype, False, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)
        else :
            epcam_api.set_select_param(featuretype, True, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)

    except Exception as e:
        print(e)
    return 0

def select_features_by_attributes(job, step, layers, logic, attribute_list):
    """选中attributes属性的features

    详细描述：

    :param     job(str): 料名 \n
    :param     step(str): step \n
    :param     layers(list): 层列表 \n
    :param     logic(int): 决定筛选器按属性筛选时，按属性列表全部满足筛选还是有其一进行筛选 \t
                           0 ：全部满足  1：有其一 \n
    :param     attribute_list(list): 要设置的属性列表 \n
    :returns   :None \n
    :raises    error: \n
    Usage:     select_features_by_attributes('','',[], 0, [{".fiducial_name":"cle"},{".drill":"plated"}])    
    """
    try:
        epcam_api.filter_set_attribute(logic, attribute_list)
        e = epcam_api.get_select_param()
        epcam_api.select_features_by_filter(job, step, layers)
    except Exception as e:
        print(e)
    return 0


def select_features_by_filter(job, step, layers):
    """根据筛选条件选择

    详细描述：\n
    :param     job(str): 料名 \n
    :param     step(str): \n
    :param     layers(list): 筛选器作用的layer列表 \n
    :returns   :None \n
    :raises    error: \n
    Usage:     layer_info.select_features_by_filter(job,'out',['comp']) \n

    """
    try:
        epcam_api.select_features_by_filter(job, step, layers)
    except Exception as e:
        print(e)
    return 0


def get_all_drill_symbolname(job, step, layer):
    """获取孔层的所有feature的symbolname \n
    详细描述：\n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :returns   symbol_list(list): 当前层中pad的name和size
    :raises    error:
    Usage:     job = 'g058c-965a'
               get_all_drill_symbolname(job,'out','comp')-> ["",""] \n 
    """
    try:
        global _size
        epcam_api.open_layer(job, step, layer)
        ret = epcam_api.get_all_features_report(job, step, layer)
        data = json.loads(ret)
        drill_list = data['paras']['pad_list']
        symbol_list = []
        for i in range(0, len(drill_list)):
            if drill_list[i]['symbolname'] not in symbol_list:
                if drill_list[i]['symbolname'][0] == 'o':
                    str = drill_list[i]['symbolname']
                    str1 = str[4:]
                    index_x = str1.index('x')
                    number_1 = float(str1[:(index_x)])
                    number_2 = float(str1[(index_x+1):])
                    if number_1 >= number_2:
                        _size = number_2* 25400
                    else:
                        _size = number_1* 25400
                else:
                    _size = drill_list[i]['symbol_width']
            symbol_list.append([drill_list[i]['symbolname'], _size])
        return symbol_list
    except Exception as e:
        print(e)
    return ''   

# 有问题
def get_all_features_size(job, step, layer):
    """获取当前层的所有feature的size \n
    详细描述：\n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :returns   size_list(list): 获取当前层的所有drill的size的列表 \n
    :raises    error: \n
    Usage：    get_all_features_size(job,'out','comp')-> [] \n   

    """
    try:
        global _size
        epcam_api.open_layer(job, step, layer)
        ret =epcam_api.get_all_features_report(job, step, layer)
        data = json.loads(ret)
        drill_list = data['paras']['pad_list']
        size_list = []

        for i in range(0, len(drill_list)):
            if drill_list[i][0] == 'o':
                str = pad_list[i]['symbolname']
                str1 = str[4:]
                index_x = str1.index('x')
                number_1 = float(str1[:(index_x)])
                number_2 = float(str1[(index_x+1):])
                if number_1 >= number_2:
                    _size = number_2* 25400
                else:
                    _size = number_1* 25400
            else:
                _size = drill_list[i]['symbol_width']
            if _size not in size_list:
                size_list.append(_size)
        return size_list
    except Exception as e:
        print(e)
    return ''


def reset_select_filter():
    """清空筛选条件\n
    详细描述：将筛选参数设置为默认状态。\n
    :param     :\n
    :returns   :None \n
    :raises    error:\n
    Usage：    layer_info.reset_select_filter()
    """
    try:
        epcam_api.set_select_param(0x7F, False, [], 0, 0, -1, -1, [], 0, True)
    except Exception as e:
        print(e)
    return 0


def clear_select(job, step, layer):
    """清空选择 \n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :returns   :None \n
    :raises    error: \n
    Usage：    layer_info.clear_select(job,'out','board')
    """
    try:
        epcam_api.clear_selected_features(job, step, layer)
    except Exception as e:
        print(e)
    return 0

  
def get_inner_layer_list(job):
    """获取内层layer_list\n
    详细描述： \n
    :param     job(str):料名 \n
    :returns   inner_layer_list(list):内层layername列表 \n
    :raises    error: \n
    Usage：    layer_info.get_inner_layer_list(job)
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])
        
        if len(board_layer_list) <= 2:
            print('no inner layer!')
            return []
        else:
            board_layer_list.pop(-1)
            board_layer_list.pop(0)
            inner_layer_list = board_layer_list
        return inner_layer_list
    except Exception as e:
        print(e)
    return ''


def set_featuretype_filter(featuretype):
    """设置feature type筛选 \n
    详细描述：  按postive,negative,text,surface,arc,line,pad从右到左顺序对应二进制的2的相应次方，转成十进制求和->64/32/16/8/4/2/1\n
    :param     featuretype(int): 代表筛选features的类型,featuretype最大值是：127,表示选择全部feature类型 \n
               featuretype = math.pow(2,0)* pad + math.pow(2,1)*line + math.pow(2,2)*arc +...+math.pow(2,6)*postive \n
    :returns   :None \n
    :raises    error: \n
    Usage：    layer_info.set_featuretype_filter(127)

    """ 
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        #print(data)  
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        symbols = select_param['symbols']
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        has_symbol = select_param['has_symbols']
        epcam_api.set_select_param(featuretype, has_symbol, symbols,minline, maxline,dcode, flag,value, pr_value,sele)
    except Exception as e:
        print(e)
    return 0


def select_features_by_featuretype(job, step, layers, featuretype):
    """选中指定featuretype的features\n
    详细描述： \n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :param     featuretype(int): 代表筛选features的类型。(同上)\n
    :returns   :None \n
    :raises    error:
    Usage：    layer_info.select_features_by_featuretype(job,'out',['drl+1'],65)
    """
    try:
        set_featuretype_filter(featuretype)
        epcam_api.select_features_by_filter(job, step, layers)
    except Exception as e:
        print(e)
    return 0


def set_include_symbol_filter(symbol_list):
    """设置include symbol筛选\n
    详细描述：   只有pad,line, arc有symbolname\n
    :param     symbol_list(list):设置筛选include_symbol的列表\n 
    :returns   :None \n
    :raises    error:
    Usage：    layer_info.set_include_symbol_filter(['r39.370','r92.520'])
    """
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        featuretype = select_param['featuretypes']
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        if symbol_list == '':
            epcam_api.set_select_param(featuretype, False, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)
        else :
            epcam_api.set_select_param(featuretype, True, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)

    except Exception as e:
        print(e)
    return 0


def get_drillpad_symbolname(jobname, step, layer, min_size, drill_symbol, drill_name):
    """拿到当前层小于min_size的孔盘的symbolname list\n
    详细描述：  选择孔层为参考层，当前层对应位置的孔盘中孔环的尺寸小于min_size的symbolname list\n
    :param     jobname(str):料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :param     min_size(int): 最小润环值 \n
    :param     drill_symbol(list): 孔symbol列表 \n
    :param     drill_name(str): 孔层名 \n
    :returns   drillpad_list(list): 孔pad列表 \n 
    :raises    error:
    """
    try:
        reference_layers = []
        reference_layers.append(drill_name)
        #恢复筛选条件
        set_include_symbol_filter('')
        set_featuretype_filter(65)
        include_symbol= []
        include_symbol.append(drill_symbol[0])
        epcam_api.filter_by_mode(jobname, step, layer, reference_layers, 0, 127, 0 ,include_symbol)
        #获取选中PAD的symbol信息
        global _size
        ret = epcam_api.get_selected_features_report(jobname, step, layer)
        data = json.loads(ret)
        pad_list = data['paras']['pad_list']
        symbol_list = []
        if pad_list == None:
            drillpad_list = []
            return drillpad_list
        else:
            for i in range(0, len(pad_list)):
                if pad_list[i]['symbolname'] not in symbol_list:
                    if pad_list[i]['symbolname'][0] == 'o' :
                        str = pad_list[i]['symbolname']
                        str1 = str[4:]
                        index_x = str1.index('x')
                        number_1 = float(str1[:(index_x)])
                        number_2 = float(str1[(index_x+1):])
                        if number_1 >= number_2:
                            _size = number_2 * 25400
                        else:
                            _size = number_1 * 25400
                    else:
                        _size = pad_list[i]['symbol_width']
                symbol_list.append([pad_list[i]['symbolname'], _size])

            drillpad_list=[]
            if symbol_list == []:
                return drillpad_list
            else:
                for j in range(0,len(symbol_list)):
                    ann_ring = (symbol_list[j][1] - drill_symbol[1])/2
                    if ann_ring < min_size  and  symbol_list[j] not in drillpad_list:
                        drillpad_list.append(symbol_list[j])
        return drillpad_list

    except Exception as e:
        print(e)
    return 0


def filter_set_include_syms(has_symbols, symbols):
    """添加symbol筛选 \n
    详细描述：\n
    :param     has_symbols(bool): 筛选条件上是否加上symbol名。True:加上,False:不加上\n
    :param     symbols(list): 筛选的symbol的名列表 \n
    :returns   :None \n
    :raises    error:
    Usage:     layer_info.filter_set_include_syms(True,['r124.016'])
    """
    try:
        epcam_api.filter_set_include_syms(has_symbols, symbols)
    except Exception as e:
        print(e)
    return 0


def change_layer_context(jobname, layer, context):
    """改变layer的context
    详细描述：\n
    :param     jobname(str): 料名 \n
    :param     layer(str): 层名 \n
    :param     context(str): 'misc'/'board'
    :returns   :None \n
    :raises    error:
    Usage:     layer_info.change_layer_context(job,'cmask','misc')
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
                if layer_infos[i]['name'] == layer:
                    layer_index = i + 1
                    layer_infos[i]['context'] = context
        epcam_api.change_matrix(jobname, -1, layer_index, '', layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0


def delete_feature(job, step, layers):
    """删除选中的feature\n
    详细描述：\n
    :param     job(str): 料名 \n
    :param     layers(list): 层列表 \n
    :returns   :None \n
    :raises    error: \n
    Usage:     layer_info.delete_feature(job,'out',['cmask+1'])
    """
    try:
        epcam_api.sel_delete(job, step, layers)
    except Exception as e:
        print(e)
    return 0


def reverse_select(job, step, layer):
    """ 反选 \n
    详细描述：  选中除现在选中的范围内的所有部分。取补集的意思 \n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :returns   :None \n
    :raises    error: \n
    Usage:     layer_info.reverse_select(job,'out','cmask+1')
    """
    try:
        epcam_api.counter_election(job, step, layer)
    except Exception as e:
        print(e)
    return 0


def select_feature(job, step, layer, selectpolygon, featureInfo, margin, clear):
    """  选中feature \n
    详细描述：  通过框选去选中feature,单选模式下只需选择框与feature有交点便选中，\n
               全选模式下只选中完全在选择框内的所有的feature \n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :param     selectpolygon(list): 坐标组成的选择框（需首尾闭合且单位是纳米）：points_location = [[0,0],[1,0],[1,1],[0,1],[0,0]]
    :param     featureInfo(dict): {}
    :param     margin(int): 0:单选 1：多选
    :param     clear(bool): 是否清除当前所有已被选中的feature的选中状态
    :returns   : None \n
    :raises    error:
    Usage:     layer_info.select_feature(job,'out',fin_layer,points_location, {}, 1, True)
    """
    try:
        epcam_api.select_feature(job, step, layer, selectpolygon, featureInfo, margin, clear)
    except Exception as e:
        print(e)
    return 0


def change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror):
    """修改文字 \n
    详细描述：   修改影响层文字（如果有选中的文字，则修改选中的文字。否则修改影响层所有文字）\n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layers(list): 层列表 \n
    :param     text(str): 修改后的文字 \n
    :param     font(str): 修改后的字体 \n
    :param     x_size（int）: 修改后字宽（纳米）\n
    :param     y_size（int）:修改后字高 （纳米）\n
    :param     width（int）:修改后文字的线宽（纳米）\n
    :param     polarity（int): -1：将文字极性修改为负极性 \n
                              0：不修改文字极性 \n
                              1：将文字极性修改为正极性 \n
    :param     mirror(int):   -1：将文字修改为非镜像 \n
                              0：不修改文字镜像 \n
                              1：将文字修改为镜像 \n
    :returns   :None \n
    :raises    error: \n
    Usage:     layer_info.change_text(job, 'test', ['gto'], 'Z.Z.X', 'standard', 5080*1000, 5080*1000, 700*1000, 1, 1)
    """
    try:
        epcam_api.change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror)
    except Exception as e:
        print(e)
    return 0


def sel_break(job, step, layers, sel_type):
    """打散feature \n
    详细描述：   打散feature,有选中的feature则打散选中的feature，无则打散所有的feature \n
                组合物件->较低物件(text->line)
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layers(list): 层列表 \n
    :param     sel_type: 0:break选中的feature \n
                         1：break影响层所有的feature \n
    :returns   :None \n
    :raises    error:
    Usage:     layer_info.sel_break(job,'out',['cmask'], 0 )
    """
    try:
        epcam_api.sel_break(job, step, layers, sel_type)
    except Exception as e:
            print(e)
    return 0


def layer_compare_bmp(jobname1, stepname1, layername1, jobname2, stepname2,layername2, tolerance, grid_size, savepath, suffix, bmp_width, bmp_height):
    """ 比图结果保存bmp
    详细描述： \n
    :param     jobname1(str): 第一个料名 \n
    :param     stepname1(str): 第一个step \n
    :param     layername1(str): 第一个层名 \n
    :param     jobname2(str): 第二个料名 \n
    :param     stepname2(str): 第二个step \n
    :param     layername2(str): 第二个层名 \n
    :param     tolerance（int）: 比图精度(纳米单位）\n
    :param     grid_size（int）: 网格大小(纳米单位）\n
    :param     savepath（str）: bmp存放路径 \n
    :param     suffix（str）: bmp文件的后缀名 \n
    :param     bmp_width（int）: bmp宽度尺寸 \n
    :param     bmp_height（int） bmp高度尺寸 \n
    :returns   :None \n
    :raises    error: \n
    Usage: 
    """
    try:
        epcam_api.layer_compare_bmp(jobname1, stepname1, layername1, jobname2, stepname2,layername2, tolerance, grid_size, savepath, suffix, bmp_width, bmp_height)
    except Exception as e:
        print(e)
    return 0



def step_repeat(job, parentstep, childsteps):
    """拼板 \n
    详细描述： \n
    :param     job（str）: 料名
    :param     parentstep(str): panel \n
    :param     childsteps（str）: 拼入panel的step \n
    :returns   :None \n
    :raise     error: \n
    Usage:     layer_info.step_repeat(job,'pcb','out')
    """
    try:
        epcam_api.step_repeat(job, parentstep, childsteps)
    except Exception as e:
        print(e)
    return 0


def set_datum_point(job, stepname, point_x, point_y):
    """  设置基准点
    详细描述： \n 
    :param     job（str）: 料名 \n
    :param     stepname(str): step名 \n
    :param     point_x(int): 基准点横坐标 \n
    :param     point_y(int): 基准点纵坐标 \n
    :returns   : None \n
    :raise     error: \n
    Usage:      
    """
    try:
        epcam_api.set_datum_point(job, stepname, point_x, point_y)
    except Exception as e:
        print(e)
    return 0


def get_profile_box(job, step):
    """ 获取profile宽高 \n
    详细描述： \n 
    :param     job（str）: 料名 \n
    :param     step(str): step名 \n
    :returns   :pro（list): profile宽高的列表 \n    
    Usage:     layer_info.get_profile_box(job,'out')
    """
    try:
        ret = epcam_api.get_profile_box(job, step)
        data = json.loads(ret)
        #print(data['paras']['Xmax'])
        width = data['paras']['Xmax'] - data['paras']['Xmin']
        height = data['paras']['Ymax'] - data['paras']['Ymin']
        pro = [width, height]
        return pro
    except Exception as e:
        print(e)
    return 0


def sel_index(job, step, layers, mode):
    """ 修改feature的叠放顺序 \n
    详细描述： \n 
    :param     job（str）: 料名 \n
    :param     step(str): step名 \n
    :param     layers(list):层列表 \n
    :param     mode(bool): 
    :returns   : None \n    
    Usage:     layer_info.sel_index(job,'out',['comp'],False)
    """
    try:
        epcam_api.sel_index(job, step, layers, mode)
    except Exception as e:
        print(e)
    return 0


def create_profile(jobname, stepname, layername):
    """新建profile线 \n
    详细描述：   先选中多段线，根据此外框线转成profile线\n 
    :param     job（str）: 料名 \n
    :param     step(str): step名 \n
    :param     layername(str):层名 \n
    :returns   : None \n
    Usage:      layer_info.select_features_by_featuretype(job,'out',['out+1'],98) \n
                layer_info.create_profile(job,'out','out+1')
    """
    try:
        epcam_api.create_profile(jobname, stepname, layername)
    except Exception as e:
        print(e)
    return 0

#添加矩形(线)
def add_line_rectangle(job, step, layer, leftbottom_x, leftbottom_y, righttop_x, righttop_y):
    """添加矩形(线)
    详细描述：  四条线组成封闭的矩形\n 
    :param     job（str）: 料名 \n
    :param     step(str): step名 \n
    :param     layer(str):层名 \n
    :param     leftbottom_x(int): 左下x坐标(纳米)\n
    :param     leftbottom_y(int)：左下y坐标(纳米)\n
    :param     righttop_x(int)：左上x坐标(纳米)\n
    :param     righttop_y(int)：左上y坐标(纳米)\n
    :returns   : None \n
    Usage：    layer_info.add_line_rectangle(job, 'out', 'out+1', leftbottom_x, leftbottom_y, righttop_x, righttop_y)\n
    """
    try:
        epcam_api.add_line(job, step, [], layer, 'r10', leftbottom_x, leftbottom_y, leftbottom_x, righttop_y, 1, 0, [])
        epcam_api.add_line(job, step, [], layer, 'r10', leftbottom_x, righttop_y, righttop_x, righttop_y, 1, 0, [])
        epcam_api.add_line(job, step, [], layer, 'r10', righttop_x, righttop_y, righttop_x, leftbottom_y, 1, 0, [])
        epcam_api.add_line(job, step, [], layer, 'r10', righttop_x, leftbottom_y, leftbottom_x, leftbottom_y, 1, 0, [])
    except Exception as e:
        print(e)
    return 0

#获取所有layer名
def get_all_layer_name(job):
    """ 获取所有layer名\n
    详细描述：  \n 
    :param     job（str）: 料名 \n   
    :returns   layer_list(list): 层列表  \n
    Usage：     layer_info.get_all_layer_name(job)
    """
    try:
        ret = epcam_api.get_graphic(job)
        data = json.loads(ret)
        layer_list = []
        layer_info = data['paras']['info']
        if len(layer_info):
            for i in range(0, len(layer_info)):
                layer_list.append(layer_info[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''

#获取所有layer名
def get_all_board_name(job):
    """ 获取所有board属性的layer名 \n
    详细描述：   获取所有board类型的layer名\n 
    :param     job（str）: 料名 \n   
    :returns   layer_list(list): 层列表  \n
    Usage：    layer_info.get_all_board_name(job)
    """
    try:
        ret = epcam_api.get_graphic(job)
        data = json.loads(ret)
        layer_list = []
        layer_info = data['paras']['info']
        if len(layer_info):
            for i in range(0, len(layer_info)):
                if layer_info[i]['context'] == 'board':
                    layer_list.append(layer_info[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''


def sel_copy_other(src_job, src_step, src_layers, dst_layers, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor):
    """ 跨层复制layer \n
    详细描述：\n
    :param    src_job(str): 源料名 \n
    :param    src_step(str): 源step \n
    :param    src_layers(list): 源层列表
    :param    dst_layers(list): 目标层列表
    :param    invert（bool）：true代表极性反转，flase代表极性不反转 \n
    :param    offset_x(int): x轴方向位移 \n
    :param    offset_y(int): y轴方向位移 \n
    :param    mirror（int）: 0: None(不镜像) \n
                            1: horizontally \n
                            2: vertically \n
    :param    resize(float): 调整大小 \n
    :param    rotation(float): 旋转角度 \n
    :param    x_anchor(float): 锚点x坐标 \n
    :param    y_anchor(float): 锚点y坐标 \n
    :returns  :None \n
    Usage：    layer_info.sel_copy_other(job,'out',["board"],["comp"],False,0, 0, 0, 0.0, 0.0, 0.0, 0.0)
    """
    try:
        epcam_api.sel_copy_other(src_job, src_step, src_layers, dst_layers, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return ''

def get_soldermask_list(job):
    """获取防焊层list \n
    :param     job（str）: 料名 \n
    :returns   solder_mask_list（list）:防焊层列表 \n
    :raises    error: \n
    :returns  :None \n    
    Usage：    layer_info.get_soldermask_list(job)
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        solder_mask_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'solder_mask':
                solder_mask_list.append(layer_info[i]['name'])      
        return solder_mask_list
    except Exception as e:
        print(e)
    return ''


def get_smd_or_bga_symbolname(job, step, layer):
    """拿到选中的smd/bga pad的symbol信息 \n
    详细描述：\n
    :param     job（str）: 料名 \n
    :param     step（str）: \n
    :param     layer(str):层名 \n
    :returns   symbol_list（list）: 选中的smd/bga pad的symbol列表 \n
    :raises    error: \n
    Usage：     layer_info.reset_select_filter()\n
                layer_info.set_featuretype_filter(97)\n
                layer_info.select_features_by_filter(job,'out',['sold+1'])\n
                layer_info.get_smd_or_bga_symbolname(job,'out','sold+1')->[['ln4-sm', 7000010.0], ['rect167.874x160.024', 4064609.0],...]
    """
    try:
        #获取选中PAD的symbol信息
        global _size
        ret = epcam_api.get_selected_features_report(job, step, layer)
        data = json.loads(ret)
        pad_list = data['paras']['pad_list']
        symbol_list = []
        if pad_list == None:
            return symbol_list
        else:
            for i in range(0, len(pad_list)):
                if pad_list[i]['symbolname'] not in symbol_list:
                    try:
                        _size = 0
                        if pad_list[i]['symbol_width'] <= pad_list[i]['symbol_height']:
                            _size = pad_list[i]['symbol_width']
                        else:
                            _size = pad_list[i]['symbol_height']                            
                        symbol_list.append([pad_list[i]['symbolname'], _size])
                    except:
                        continue
        return symbol_list
    except Exception as e:
        print(e)
    return []


def get_soldermask_pad_symbol(job, step, layer, min_size, bga_or_smd_symbol):
    """拿到选中的开窗中需要resize的symbol信息 \n
    详细描述：   得到防焊层需要resize的的symbol信息\n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layer(str): 层名 \n
    :param     min_size(int): 最小公差 \n
    :param     bga_or_smd_symbol(list): smd/bga pad的symbol的列表  ->[(bga/smd)symbolname,size] \n
    :returns   soldermask_pad_list(list): 需要resize的symbol信息 ->[symbolname,size] \n
    :raises    error:\n
    Usage：    layer_info.get_soldermask_pad_symbol(job, step, layer, min_size, bga_or_smd_symbol)
    """
    try:
        symbol_list = get_smd_or_bga_symbolname(job, step, layer)

        soldermask_pad_list=[]
        if symbol_list == []:
            return soldermask_pad_list
        else:
            for j in range(0,len(symbol_list)):
                try:
                    if bga_or_smd_symbol[0][0:4] == 'rect' :
                        symbolname = bga_or_smd_symbol[0]
                        str1 = symbolname[4:]
                        if 'r' in str1: 
                            index_r = str1.index('r')
                            str1 = str1[0:index_r-1]
                        index_x = str1.index('x')
                        number_1 = float(str1[:(index_x)])
                        number_2 = float(str1[(index_x+1):])
                        kaichuangname = symbol_list[j][0]
                        if kaichuangname[0:4] != 'rect':
                            continue
                        str2 = kaichuangname[4:]
                        if 'r' in str2: 
                            index_r = str2.index('r')
                            str2 = str2[0:index_r-1]
                        index_xx = str2.index('x')
                        number_11 = float(str2[:(index_xx)])
                        number_22 = float(str2[(index_xx+1):])
                        if (number_11-number_1)<(number_22-number_2):
                            ann_ring = (number_11-number_1)/2
                        else:
                            ann_ring = (number_22-number_2)/2
                    elif bga_or_smd_symbol[0][0:4] == 'oval' :
                        symbolname = bga_or_smd_symbol[0]
                        str1 = symbolname[4:]
                        if 'r' in str1: 
                            index_r = str1.index('r')
                            str1 = str1[0:index_r-1]
                        index_x = str1.index('x')
                        number_1 = float(str1[:(index_x)])
                        number_2 = float(str1[(index_x+1):])
                        kaichuangname = symbol_list[j][0]
                        if kaichuangname[0:4] != 'oval':
                            continue
                        str2 = kaichuangname[4:]
                        if 'r' in str2: 
                            index_r = str2.index('r')
                            str2 = str2[0:index_r-1]
                        index_xx = str2.index('x')
                        number_11 = float(str2[:(index_xx)])
                        number_22 = float(str2[(index_xx+1):])
                        if (number_11-number_1)<(number_22-number_2):
                            ann_ring = (number_11-number_1)/2
                        else:
                            ann_ring = (number_22-number_2)/2
                    else:
                        ann_ring = (symbol_list[j][1] - bga_or_smd_symbol[1])/(2*25400)
                    if ann_ring < min_size  and  symbol_list[j] not in soldermask_pad_list:
                        soldermask_pad_list.append(symbol_list[j])
                except:
                    continue
        return soldermask_pad_list

    except Exception as e:
        print(e)
    return 0

def create_layer_between_profile(jobname, stepname, new_layername, child_profile_margin):
    """profile线间新建layer \n
    #详细描述：  外profile和子profile之间填充，之间空白值 \n
    :param     jobname(str): 料名 \n
    :param     stepname(str): step名 \n
    :param     new_layername(str): 新建layer名 \n
    :param     child_profile_margin(int): 避铜值 \n
    :returns   :None \n
    :raises    error: \n
    Usage：    child_profile_margin = 2*1000000
               layer_info.create_layer_between_profile(job, 'out', 'cmask+2', child_profile_margin)
    """
    try:
        epcam_api.create_layer_between_profile(jobname, stepname, new_layername, child_profile_margin)
    except Exception as e:
        print(e)
    return ''


def get_signal_layers_list(job):
    """ 获取线路层layer_list\n
    #详细描述：  外层和内层是线路层 \n
    :param     job(str): 料名 \n
    :returns   signal_layer_list(list)： 线路层的layer名列表 \n
    :raises    error: \n
    Usage：    layer_info.get_signal_layers_list(job)->['comp','l1','l2','sold']
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        signal_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and (layer_info[i]['type'] == 'signal' or layer_info[i]['type'] == 'power_ground'):
                signal_layer_list.append(layer_info[i]['name'])  
        return signal_layer_list
    except Exception as e:
        print(e)
    return []

def add_surface(job, step, layers, layer, polarity, dcode, isround, attributes, points_location):
    """添加surface \n
    #详细描述：  \n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layers(list): 层名列表 \n
    :param     layer（str）: 层名 \n
    :param     polarity（str）: 添加surface的极性 1:正极性 -1：负极性\n
    :param     dcode(int): 自定义，默认0 \n
    :param     isround(bool): false \n
    :param     attributes(list): surface的属性列表 \n
    :param     points_location(list): 多边形坐标(首尾闭合) ->points_location = [[0,0],[1,0],[1,1],[0,1],[0,0]] \n
    :returns   :None \n
    :raises    error:
    Usage：    layer_info.add_surface(job, 'out', [], last, -1, 0, False, [], points_location)
    """
    try:
       epcam_api.add_surface(job, step, layers, layer, polarity, dcode, isround, attributes, points_location)
    except Exception as e:
        print(e)
    return ''

def clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype):
    """ 区域切割(profile) \n
    #详细描述：  去除外框线和Profile线外杂物\n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layers(list): 层名列表 \n
    :param     clipinside（bool）: 切割profile线内(外) True:线内 False:线外\n
    :param     clipcontour（bool）: 是否轮廓化 ,True:轮廓化，False: 不轮廓化\n
    :param     margin（int）: 0 （纳米） \n
    :param     featuretype（int）: 筛选feature（二进制权数转成十进制数，详情参考select_featuretype_filter()),104->正负surface\n
    :returns   :None \n
    :raises    error: \n
    Usage：    layer_info.select_features_by_featuretype(job,'out',['sold+1'],104)\n
               layer_info.clip_area_use_profile(job,'out',['sold+1'], False, True, 0, 104) 
    """
    try:
       epcam_api.clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype)
    except Exception as e:
        print(e)
    return ''

def get_outter_list(job):
    """获取外层list \n
    #详细描述：\n
    :param     job（str）: 料名 \n
    :returns   outter_layer_list(list): 外层layername列表 \n
    :raises    error: \n
    Usage：     layer_info.get_outter_list(job)->['comp','sold']
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        if index_list == []:
            print("no signal layer")
            return []
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])
        outter_layer_list = []
        outter_layer_list.append(board_layer_list[0])
        if len(board_layer_list) == 1:
            return outter_layer_list
        else: 
            outter_layer_list.append(board_layer_list[-1])
        return outter_layer_list
    except Exception as e:
        print(e)
    return ''

def get_selected_pad_point(job, step, layer):
    """获取选中的中点和symbolname \n
    #详细描述：\n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layer(str): 层名 \n
    :returns   padinfo(list): pad中点列表 \n
    :raises    error: \n
    Usage：     layer_info.reset_select_filter() \n
                layer_info.select_features_by_featuretype(job,'out',['comp+1'],97) \n
                layer_info.get_selected_pad_point(job,'out','comp+1')\n
                ->[[-10924997.0, -3425011.9999999986, 'a-1'], [-10924997.0, 500425008.0000001, 'a-1'], ...]

    """ 
    try:
        ret = epcam_api.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        pad_center = []
        if data['paras'] != False:
            for i in range(len(data['paras'])):
               point_symbolname = [data['paras'][i]['X'] * 25400000, data['paras'][i]['Y'] * 25400000, data['paras'][i]['symbolname']]
               pad_center.append(point_symbolname)
        return pad_center
    except Exception as e:
        print(e)
    return []

def get_min_tol(bga_or_smd_symbol, windowing_symbol):
    """拿到选中的开窗中需要resize的symbol信息 \n
    #详细描述： \n
    :param     bga_or_smd_symbol(list): [(bga/smd)symbolname,size] \n
    :param     windowing_symbol(list):  需要开窗的symbol列表 \n
    :returns   ann_ring(int): 孔环尺寸 \n
    :raises    error: \n
    Usage：    layer_info.get_min_tol([],[])->
    """
    try:
        symbolname = bga_or_smd_symbol
        kaichuangname = windowing_symbol
        if bga_or_smd_symbol[0:4] == 'rect' or bga_or_smd_symbol[0:4] == 'oval':
            str1 = symbolname[4:]
            if 'r' in str1: 
                index_r = str1.index('r')
                str1 = str1[0:index_r-1]
            index_x = str1.index('x')
            number_1 = float(str1[:(index_x)])
            number_2 = float(str1[(index_x+1):])
            if kaichuangname[0:4] != bga_or_smd_symbol[0:4]:
                return 0
            str2 = kaichuangname[4:]
            if 'r' in str2: 
                index_r = str2.index('r')
                str2 = str2[0:index_r-1]
            index_xx = str2.index('x')
            number_11 = float(str2[:(index_xx)])
            number_22 = float(str2[(index_xx+1):])
            if (number_11-number_1)<(number_22-number_2):
                ann_ring = (number_11-number_1)/2
            else:
                ann_ring = (number_22-number_2)/2
        else:
            number_3 = float(symbolname[1:])
            number_4 = float(kaichuangname[1:])
            ann_ring = (number_3 - number_4) / 2
        return ann_ring
    except Exception as e:
        print(e)
    return 0

#整理layer
def arrange_layer(job, backup_layer):
    """ 整理layer \n
    #详细描述： \n
    :param     job（str）: 料名 \n
    :param     backup_layer(str): \n
    return:    :None \n
    :raises    error: \n
    Usage：    layer_info.arrange_layer(job,'l1')
    """    
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        board_layer_list=[]
        index_list = []
        layer_index = 0
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == '----------':
                layer_index = i 
            if layer_infos[i]['context'] == 'board' and (layer_infos[i]['type'] == 'signal' or layer_infos[i]['type'] == 'solder_mask' or layer_infos[i]['type'] == 'silk_screen'):
                index_list.append(i)
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_infos[j]['name'])

        NUM = layer_index+1
        for k in range(0, len(board_layer_list)):
            lenth = len(board_layer_list[k])
            for t in range(layer_index, len(layer_infos)):
                layername = layer_infos[t]['name']
                tt = layername[:lenth]
                if  board_layer_list[k] == layername[:lenth]:
                    if layername[lenth] == '_' or layername[lenth] == '-' or layername[lenth] == '+':
                        epcam_api.move_layer(job, t+1, NUM+1)
                        NUM = NUM + 1
                        ret2 = epcam_api.get_matrix(job)
                        data2 = json.loads(ret2)
                        layer_infos = data2['paras']['info']
        if backup_layer:
            ret3 = epcam_api.get_matrix(job)
            data3 = json.loads(ret3)
            layer_infos = data3['paras']['info']
            layer_index1 = 0
            for l in range(0, len(layer_infos)):
                if layer_infos[l]['name'] == '----------':
                    layer_index1 = l
            for m in range(layer_index1+1, len(layer_infos)):
                if "+1" not in layer_infos[m]['name']:
                    pre_layername = layer_infos[m]['name']
                    job_operation.delete_layer(job, pre_layername)
    except Exception as e:
        print(e)
    return 0 

#contour to pad
def contour2pad(job, step, layers, tol, minsize, maxsize, suffix):
    """contour to pad \n
    #详细描述：  将铜面转换成焊盘,如果所选铜面无法与已有的任何一个焊盘匹配，则会创建一个新的焊盘\n
                使用条件：surface \n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layers(list): 层名列表\n
    :param     tol(float): 默认值：0 \n
    :param     minsize(float): 转换区域的最小尺寸,范围：0.01~10 mil \n 
    :param     maxsize(float): 转换区域的最大尺寸，输入的值必须大于等于所选区域的最大边，否则不执行命令。范围：1.001~100000 mil\n
    :param     suffix（str）: 转换后该层在转换前的资料将以“xxx+后缀名”名字被复制备份，后缀名默认为：+++ \n
    return:    :None \n
    :raises    error: \n
    Usage：    layer_info.contour2pad(job,'out',['comp+1'],0, 127.00*1000000, 2539974.60*1000000, '_zzx')
    """  
    try:
        epcam_api.contour2pad(job, step, layers, tol, minsize, maxsize, suffix)
    except Exception as e:
        print(e)
    return ''


#resize_polyline
def resize_polyline(job, step, layers, size, sel_type):
    """重新设置多边形尺寸 \n
    #详细描述：    对多边形物件，通过拉伸重新设置多边形尺寸。多边形无需闭合，但边须在小于公差范围内连接，可拉伸，缩小。\n
    :param      job（str）: 料名 \n
    :param      step（str）: step \n
    :param      layers(list): 层名列表\n
    :param      size(int)： 增加或减少的值\n 
    :param      sel_type(int)：  \n
    return:     :None \n
    :raises     error: \n    
    Usage：      layer_info.select_features_by_featuretype(job,'out',['drl+1'],98) \n
                layer_info.resize_polyline(job,'out',['drl+1'],12700*1000, 98)
    """
    try:
        epcam_api.resize_polyline(job, step, layers, size, sel_type)
    except Exception as e:
        print(e)
    return ''

def get_silkscreen_layer(job):
    """获取丝印层layer_list  \n
    #详细描述：   \n
    :param     job(str): 料名 \n
    :returns   layer_list(list): 丝印层layername列表  \n
    :raises    error: \n
    Usage：    layer_info.get_silkscreen_layer(job)
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'silk_screen':
                layer_list.append(layer_info[i]['name'])
        
        if len(layer_list) < 1:
            print("can't find silk_screen-layer!")

        return layer_list
    except Exception as e:
        print(e)
    return ''

#跨层移动feature
def sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor):
    """ 跨层移动feature \n
    #详细描述：  将一个料号选中的内容拷贝（没选中则拷贝整层）到当前工作窗口中的layer中来。\n
    :param    src_job(str): 源料名 \n
    :param    src_step(str): 源step \n
    :param    src_layers(list): 源层列表
    :param    dst_job(str)： 目标料名 \n
    :param    dst_step(str)：  目标step \n
    :param    dst_layer(str): 目标层 \n
    :param    invert（bool）：true代表极性反转，flase代表极性不反转 \n
    :param    offset_x(int): x轴方向位移 \n
    :param    offset_y(int): y轴方向位移 \n
    :param    mirror（int）: 0: None(不镜像) \n
                            1: horizontally \n
                            2: vertically v
    :param    resize(float): 调整大小 \n
    :param    rotation(float): 旋转角度 \n
    :param    x_anchor(float): 锚点x坐标 \n
    :param    y_anchor(float): 锚点y坐标 \n
    return    :None \n
    :raises    error:  \n
    Usage：    layer_info.sel_move_other(job,'out',['apex_ls_tmp'],job,'out',fin_layer,False, 0, 0, 0, 0, 0, 0, 0)
    """   
    try:
        epcam_api.sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return ''

def set_display_widths(width):
    """ #设置显示模式 \n
    #详细描述：  \n
    ：param     width(int):  \n
    return     :None \n
    :raises    error:  \n
    Usage：     layer_info.set_display_widths()
    """
    try:
        epcam_api.set_display_widths(width)
    except Exception as e:
        print(e)
    return ''


def set_display_text(disp):
    """ 设置文字显示模式
    #详细描述：  \n
    ：param     disp(bool): \n
    return     :None \n
    :raises    error: \n
    Usage：    layer_info.set_display_text(True) 
    """
    try:
        epcam_api.set_display_text(disp)
    except Exception as e:
        print(e)
    return ''


def set_units(units):
    """ 设置单位 \n
    #详细描述：  \n
    ：param     units(int): 默认为0 \n
    return     :None \n
    :raises    error: \n
    Usage：    layer_info.set_units(0) \n
    """ 
    try:
        epcam_api.set_units(units)
    except Exception as e:
        print(e)
    return ''

def set_display_profile(mode):
    """ 设置是否显示profile线 \n
    #详细描述：  \n
    ：param     mode(int): 默认为0 \n
    return     :None \n
    :raises    error: \n
    Usage：    layer_info.set_display_profile(0) \n
    """ 
    try:
        epcam_api.set_display_profile(mode)
    except Exception as e:
        print(e)
    return ''


#contourize
def contourize(job, step, layers, accuracy, separate_to_islands, size, mode):
    """ 轮廓化 \n
    #详细描述：   对于所选物件轮廓化，即整合成铜面物件\n
    :param      job（str）: 料名 \n
    :param      step（str）: step \n
    :param      layers(list): 层名列表\n
    :param      accuracy(int): 定义轮廓线"整合前"和"整合后"之间的最大差值。（纳米）\n 
    :param      separate_to_islands(bool):整合后是否分离出孤岛，True:整合后，孤岛成为独立的铜面物件;False:整合后，孤岛仍保留在同一个铜面物件下\n
    :param      size(int): 清除轮廓内的洞,大于size的值的洞，保留之。（纳米）\n
    :param      mode(int):  清除洞的依据模式，X or Y: x或y轴任一尺寸小于size的值的洞，清除之。X and Y:x及y轴两尺寸都小于size的值的洞，清除之\n
    return      :None \n
    :raises      error: \n
    Usage：      layer_info.contourize(job,'out',['comp'],6350,True,76200, 1) \n
    """
    try:
        epcam_api.contourize(job, step, layers, accuracy, separate_to_islands, size, mode)
    except Exception as e:
        print(e)
    return ''


def gerber_or_odb_identify(path, type):
    """ 判断gerber或odb \n
    #详细描述：  \n
    ：param     path(str):需要列出的目录路径 \n
    ：param     type(str): 指定文件的类型 \n
    return     布尔值和data['paras']['status']：\n
    :raises    error: \n
    Usage：    layer_info.gerber_or_odb_identify(path,type) 需修改
    """ 
    try:
        if type == 'gerber':
            filelist = os.listdir(path)
            for file in filelist:
                _path = os.path.join(path, file)
                #path = path + '/' + file
                ret = epcam_api.file_identify(_path)
                data = json.loads(ret)
                file_format = data['paras']['format']
                if file_format == 'Gerber274x':
                    return True
            return False
        elif type == 'odb':
            file_path = os.path.dirname(path)
            file_name = os.path.basename(path)
            ret = epcam_api.open_job(file_path, file_name)
            data = json.loads(ret)
            return data['paras']['status']
        else:
            return False
    except Exception as e:
        print(e)
    return ''


def set_selection(is_standard, is_clear, all_layers, is_select, inside, exclude):
    """ 设置模式 \n
    #详细描述：  编辑时，将大量使用鼠标选取物件。此功能针对"鼠标选取"进行更细致的定义和操作\n
    ：param     is_standard(bool): 选取模式：True：单击，False：累计选取\n
    ：param     is_clear(bool)：取消模式：True：选中的物件编辑后取消选取；False：仍保持选中状态。\n
    ：param     all_layers(bool)：True：工作层为所有层；False：当前演示层 \n
    ：param     is_select(bool)：框选设定：True：框住则选取；False：框住则取消选取 \n
    ：param     inside(bool)：被选区域：True：框内部执行动作；False：框外部执行动作 \n
    ：param     exclude(bool)：True：完全匡住则选取；False：部分匡住就可选取 \n
    return     :None \n
    :raises    error: \n
    Usage：    layer_info.set_selection(False,True,False,True,True,True) \n
    """     
    try:
        epcam_api.set_selection(is_standard, is_clear, all_layers, is_select, inside, exclude)
    except Exception as e:
        print(e)
    return 0


def reset_selection():
    """重置设置模式
    #详细描述： \n
    return     :None \n
    :raises    error: \n
    Usage：    layer_info.reset_selection()
    """
    try:
        epcam_api.set_selection(True, True, True, True, True, True)
    except Exception as e:
        print(e)
    return 0


def get_drillsize_by_symbolname(symbolname):
    """ 通过symbolname获得孔的大小 \n
    #详细描述： \n
    ：param     symbolname(str): symbol \n
    return     :None \n
    :raises    error: \n
    Usage：     layer_info.select_features_by_featuretype(job,'out',['drl+1'],97) \n
                symbolname = 'oval33.744x5.907_225'\n
                layer_info.get_drillsize_by_symbolname(symbolname) ->150043.515 \n
    """    
    try:
        _size = 0
        if symbolname[0:4] == 'oval':
            str1 = symbolname[4:]
            index_x = str1.index('x')
            number_1 = float(str1[:(index_x)])
            number_2 = float(str1[(index_x + 1):])
            if number_1 >= number_2:
                _size = number_2 * 25400
            else:
                _size = number_1 * 25400
        else:
            _size = float(symbolname[1:]) * 25400
        return _size
    except Exception as e:
        print(e)
    return 0

def add_oval_pad(job, step, layer, width, height, location_x, location_y, polarity, dcode, orient, attributes):
    """ 添指定宽高的槽孔 
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layer(str): 层名 \n
    :param     width(str):  槽孔的宽 (mil)\n 
    :param     height(str):  槽孔的高 (mil)\n
    :param     location_x(int): x坐标 (纳米)\n
    :param     location_y(int): y坐标 (纳米)\n
    :param     polarity:1:正极性    其他：负极性 \n
    :param     dcode: 默认为0 \n
    :param     orient:  0-3: 0°，90°，180°，270°顺时针旋转; \n
                        4-7: 0°，90°，180°，270°顺时针旋转+MIRROR; \n
                        8:no mirror+specialangle(0-360); \n
                        9:mirror+specialangle(0-360) \n
    :param     attributes：pad的attributes的list 例如：[{".drill":"via"},{".fiducial_name":"plated"}] \n
    Usage：    layer_info.add_oval_pad(job,'out','drl+1',33.744, 5.907_315,location_x, location_y, 1, 0, 0, [])
    """    
    try:
        symbol = 'oval' + str(width) + 'x' + str(height)
        epcam_api.add_pad(job, step, [], layer, symbol, location_x, location_y, polarity, dcode, orient, attributes)
    except Exception as e:
        print(e)
    return 0


def get_oval_width_and_height(symbolname):
    """ 通过symbolname获取槽孔宽高\n
    #详细描述： \n
    ：param     symbolname(str): symbol \n
    return     [number_1, number_2]:槽孔宽高列表 \n
    :raises    error: \n
    Usage：     layer_info.select_features_by_featuretype(job,'out',['drl+1'],97) \n
                symbolname = 'oval33.744x5.907_225' \n
                layer_info.get_oval_width_and_height(symbolname) -> [33.744, 5.907225]
    """
    try:
        if symbolname[0] == 'o':
            str1 = symbolname[4:]
            index_x = str1.index('x')
            number_1 = float(str1[:(index_x)])
            number_2 = float(str1[(index_x + 1):])
            return [number_1, number_2]
    except Exception as e:
        print(e)
    return [] 


def get_features_infos(job, step, layer):
    """ 获取选中feature的所有信息 \n
    #详细描述：  获取选中feature的坐标，symbolname,极性, 角度, 是否镜像 \n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layer(str): 层名 \n
    :returns   featureinfo(list): feature信息 \n
    :raises    error: \n
    Usage：     layer_info.select_features_by_featuretype(job,'out',['drl+1'],97) \n
                layer_info.get_features_infos(job, 'out', 'smask+1')->\n
                [[417000004.0000001, -4999990.0, 'r100.472', 'POS', 0.0, False, 0.0, 0.0, 0.0, ...],[162000006.00000003, -4999990.0, 'r100.472', 'POS', 0.0, False, 0.0, 0.0, 0.0, ...],,,]
    """ 
    try:
        ret = epcam_api.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        featureinfos = []
        if data['paras'] != False:
            for i in range(len(data['paras'])):
               featureinfo = [data['paras'][i]['X'] * 25400000, data['paras'][i]['Y'] * 25400000, data['paras'][i]['symbolname'],
                              data['paras'][i]['polarity'], data['paras'][i]['angle'], data['paras'][i]['mirror'],
                              data['paras'][i]['XS'], data['paras'][i]['YS'], data['paras'][i]['XE'], data['paras'][i]['YE'],
                              data['paras'][i]['feature_index'], data['paras'][i]['attributes'], data['paras'][i]['xsize'],
                              data['paras'][i]['ysize']]
               featureinfos.append(featureinfo)
        return featureinfos
    except Exception as e:
        print(e)
    return []

#获取选中feature的所有信息
def get_selected_features_infos(job, step, layer):
    """ 获取选中feature的所有信息\n
    #详细描述：  获取选中feature的坐标，symbolname,极性, 角度, 是否镜像 \n 
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layer(str): 层名 \n
    :returns   data['paras']: feature信息 \n
    :raises    error: \n
    Usage：    layer_info.get_selected_feature_infos(job, 'out', 'smask+1')
    """ 
    try:
        ret = epcam_api.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        featureinfos = []
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return []


def unselect_features(job, step, layer):
    """ 取消选中\n
    #详细描述：   配合筛选器使用\n 
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layer(str): 层名 \n
    :returns   None \n
    :raises    error: \n
    Usage：     layer_info.select_features_by_featuretype(job,'out',['drl+1'],97) \n
                layer_info.unselect_features(job, 'out', 'drl+1')
    """     
    try:
        epcam_api.unselect_features(job, step, layer)
    except Exception as e:
        print(e)
    return 0


def get_all_features_num(job, step, layer):
    """ 获取该层所有feature数量\n
    #详细描述：   \n 
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layer(str): 层名 \n
    :returns   num(int): 所有feature数量\n 
    :raises    error:
    Usage：    layer_info.get_all_features_num(job, 'out', 'drl+1')->int
    """    
    try:
        num = 0
        epcam_api.load_layer(job, step, layer)
        ret = epcam_api.get_all_features_report(job, step, layer)
        data = json.loads(ret)
        if data['paras']['lines_list'] != None:
            if len(data['paras']['lines_list']):
                for i in range(len(data['paras']['lines_list'])):
                    num += data['paras']['lines_list'][i]['count']
        if data['paras']['pad_list'] != None:
            if len(data['paras']['pad_list']):
                for j in range(len(data['paras']['pad_list'])):
                    num += data['paras']['pad_list'][j]['count']
        if data['paras']['surface_list'] != None:
            if len(data['paras']['surface_list']):
                for k in range(len(data['paras']['surface_list'])):
                    num += data['paras']['surface_list'][k]['count']
        if data['paras']['arc_list'] != None:
            if len(data['paras']['arc_list']):
                for v in range(len(data['paras']['arc_list'])):
                    num += data['paras']['arc_list'][v]['count']
        if data['paras']['text_list'] != None:
            if len(data['paras']['text_list']):
                for t in range(len(data['paras']['text_list'])):
                    num += data['paras']['text_list'][t]['count']
        return num
    except Exception as e:
        print(e)
    return 0


def change_feature_symbols(job, step, layers, symbol):
    """ 修改选中的symbolname\n
    #详细描述：   \n 
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :param     layers(list): 层名列表 \n
    :param     symbol(str): symbolname \n
    :returns   None \n
    :raises    error:
    Usage：     layer_info.filter_set_include_syms(True,['r124.016']) \n
                layer_info.select_features_by_filter(job, 'out',['board']) \n
                layer_info.change_feature_symbols(job, 'out',['board'],'r116.141')
    """        

    try:
        epcam_api.change_feature_symbols(job, step, layers, symbol, False)
    except Exception as e:
        print(e)
    return 0
  

def get_profile(job, step):
    """ 获取layer profile polygon \n
    #详细描述：   profile坐标(首尾闭合)\n 
    :param     job（str）: 料名 \n
    :param     step（str）: step \n
    :returns    points_location(list): profile坐标(首尾闭合)\n
    :raises     error: \n
    Usage：     layer_info.get_profile(job,'out')-> \n
                [{'ix': -17500000, 'iy': -10000000}, 
                {'ix': -17500000, 'iy': 507000000},
                {'ix': 601500000, 'iy': 507000000}, 
                {'ix': 601500000, 'iy': -10000000},
                {'ix': -17500000, 'iy': -10000000}]

    """
    try:
        ret = epcam_api.get_profile(job, step)
        data = json.loads(ret)
        points_location = data["points"]
        return points_location
    except Exception as e:
        print(e)
    return 0

#获取内外层 layer 名
def get_signal_layer_list(job):
    """获取内外层layer 名 \n
    #详细描述：
    :param     job: 料名 \n
    :returns   inner_layer_list(list):内层layername列表 \n
    :raises    error: \n
    Usage：     layer_info.get_signal_layer_list(job) ->['comp', 'l2', 'l3', 'sold']
    """
    try:
        ret = epcam_api.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])

        inner_layer_list = board_layer_list
        return inner_layer_list
    except Exception as e:
        print(e)
    return ''

#将一个料号中某一layer的信息拷贝至另一料号中
def copy_layer_features(src_job, src_step, src_layers, dst_job, dst_step, dst_layers, mode, invert):
    """将一个料号中某一layer的信息拷贝至另一料号中 \n
    #详细描述：
    :param    src_job(str): 源料名 \n
    :param    src_step(str): 源step \n
    :param    src_layers(list): 源层列表
    :param    dst_job(str)： 目标料名 \n
    :param    dst_step(str)：  目标step \n
    :param    dst_layers(list): 目标层列表\n 
    :param     mode(bool)：true代表替换，flase代表追加 \n
    :param     invert(bool)：true代表极性反转，flase代表极性不反转 \n
    :returns   None \n
    :raises    error:
    Usage：     layer_info.copy_layer_features(job,'pcb',['board'],job1,'out','comp',True, True)
    """
    try:
        epcam_api.copy_layer_features(src_job, src_step, src_layers, dst_job, dst_step, dst_layers, mode, invert)
    except Exception as e:
        print(e)
    return ''

#依据polygon 建profile
def create_profile_by_polygon(job, step, layer, poly):
    """依据polygon 建profile \n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n 
    :param     layer(str): 层名 \n
    :param     poly(list): 多段线坐标列表
    :returns   None \n
    :raises    error: \n
    Usage：    poly =[[-17500000,-10000000],[-17500000,507000000],[601500000,507000000],[601500000,-10000000],[-17500000,-10000000]]
               layer_info.create_profile_by_polygon(job,'out','comp',poly)
    """
    try:
        for i in range(len(poly)-1):
            epcam_api.add_line(job, step, [], layer, 'r1', poly[i][0], poly[i][1], poly[i+1][0], poly[i+1][1], 1, 0, [])
        select_features_by_filter(job, step, [layer])
        create_profile(job, step, layer)
        select_features_by_filter(job, step, [layer])
        delete_feature(job, step, [layer])
    except Exception as e:
        print(e)
    return ''

#反选
def counter_election(job, step, layer):
    """反选
    :param     job（str）: 料名 \n
    :param     step（str）: step \n 
    :param     layer(str): 层名 \n
    :returns   None \n
    :raises    error: \n
    Usage：     layer_info.counter_election(job,'out','cmask')
    """
    try:
        epcam_api.counter_election(job, step, layer)
    except Exception as e:
        print(e)
    return ''


def create_flip(job,step):
    """创建阴阳step：
    :param     job（str）: 料名 \n
    :param     step（str）: step \n 
    :returns   None \n
    :raises    error: \n
    Usage：     layer_info.create_flip(job,'out')
    """
    try:
        siglayer=get_signal_layer_list(job)
        smlayer=get_soldermask_list(job)
        drllayer=get_drill_layer_name(job)
        screenlayer=get_silkscreen_layer(job)
        splayer=[]
        allboard=get_all_board_name(job)
        for layer in allboard:
            if (layer not in siglayer) and (layer not in smlayer) and (layer not in drllayer) and (layer not in screenlayer):
                splayer.append(layer)
        stepname=step+'_flip'
        job_operation.create_step(job,stepname)
        poly=get_profile(job,step)
        poly  = json.loads(poly)
        poly = poly["points"]
        orig_poly = []      #左下角pcs profile polygon
        for i in range(len(poly)):
            per_point = []
            per_point.append(-poly[i]["ix"])
            per_point.append(poly[i]["iy"])
            orig_poly.append(per_point)
        create_profile_by_polygon(job, stepname,siglayer[0], orig_poly)
        
        for i in range(len(siglayer)):
            epcam_api.copy_layer_features(job, step, [siglayer[i]], job, stepname, [siglayer[len(siglayer)-1-i]], False, False)
        for i in range(len(smlayer)):
            epcam_api.copy_layer_features(job, step, [smlayer[i]], job, stepname, [smlayer[len(smlayer)-1-i]], False, False)
        for i in range(len(screenlayer)):
            epcam_api.copy_layer_features(job, step, [screenlayer[i]], job, stepname, [screenlayer[len(screenlayer)-1-i]], False, False)   
        for i in range(len(splayer)):
            epcam_api.copy_layer_features(job, step, [splayer[i]], job, stepname, [splayer[len(splayer)-1-i]], False, False)
        for drl in drllayer:    
            num1=drl[3:]
            g=num1.find('-')
            first=int(num1[0:g])
            second=int(num1[g+1:])
            if first==1 and second ==len(siglayer):
                epcam_api.copy_layer_features(job, step, [drl], job, stepname, [drl], False, False)
            else:
                newdrl='drl'+str(len(siglayer)-second+1)+'-'+str(len(siglayer)-first+1)
                if newdrl not in drllayer:
                    job_operation.create_layer(job, newdrl)
                    allboard.append(newdrl)
                    epcam_api.copy_layer_features(job, step, [drl], job, stepname, [newdrl], False, False)
                else:
                    epcam_api.copy_layer_features(job, step, [drl], job, stepname, [newdrl], False, False)

        for layer in allboard:
            epcam_api.transform(job,stepname,layer,0,False,False,True,False,False,{'ix':0,'iy':0},0,1,1,0,0)
    except Exception as e:
        print(e)
    return ''

#改变Matrix
def change_layer_matrix(jobname, layer, context,Type,layname):
    """改变layer的context \n
    :param     jobname(str):  料名 \n
    :param     layer(str): 层名 \n
    :param     context(str): 层范围 \n
    :param     Type(str): 层类型 \n
    :param     layname(str): 层名 \n
    :returns   :None
    :raises    error:
    Usage：     layer_info.change_layer_matrix(job,'alm-m','misc','drill','alm-m')
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
                if layer_infos[i]['name'] == layer:
                    layer_index = i + 1
                    layer_infos[i]['context'] = context
                    layer_infos[i]['type'] = Type
                    layer_infos[i]['name']=layname 
        epcam_api.change_matrix(jobname, -1, layer_index, '', layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0

#获取料号的usersymbol列表
def get_usersymbol_list(job):
    """获取料号的usersymbol列表 \n
    :param     job(str):  料名 \n
    :returns   user_list(list): usersymbol列表 \n
    :raises    error:
    Usage：    layer_info.get_usersymbol_list(job)
    """    
    try:
        ret = epcam_api.get_special_symbol_names(job)
        data = json.loads(ret)
        user_list = data['paras']
        return user_list
    except Exception as e:
        print(e)
    return []



def get_curlayer_min_pad_diam(job, step, layer):
    """ 获取当前层最小via孔的直径 \n
    详细描述：   单位：um \n
    :param     job（str）: 料名 \n
    :param     step（str）: step \n 
    :param     layer(str): 层名 \n
    :returns   r_diam(int): via孔的直径 \n
    :raises    error: \n
    Usage：    layer_info.get_curlayer_min_pad_diam(job, step, layer)
    """
    try:
        min_diam = -1
        r_diam = -1
        epcam_api.set_select_param(0x41, False, [], 0, 0, -1, 1, [{".drill":"via"}], 0, False)
        epcam_api.select_features_by_filter(job, step, [layer])
        ret = epcam_api.get_selected_features_report(job, step, layer)
        data = json.loads(ret)
        pad_list = data['paras']['pad_list']
        if pad_list is not None:
            for pad in pad_list:
                if min_diam == -1:
                    min_diam = pad['symbol_height']
                elif min_diam > pad['symbol_height']:
                    min_diam = pad['symbol_height']
            r_diam = round(min_diam/1000)
        return r_diam
    except Exception as e:
        print(e)
        return -1
        
def check_whether_features_is_selected(job, step, layer,layers,has_symbols,symbols):
    """使用筛选器顺序 \n
    详细描述： 根据筛选器选择features,首先要重新设置筛选器,清空选择,设置筛选器指定的symbol,根据筛选器设置选择features。\n
              如果有选中，返回值为True,否则为False。\n

    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :param     layers(list): 层列表 \n
    :param     has_symbols(bool): 筛选条件上是否加上symbol名。True:加上, False:不加上\n
    :param     symbols(list): 筛选的symbol的名列表 \n
    :returns   count(bool): 是否选中指定的features,True:选中,False:未选中 \n
    :raises    error: \n
    Usage：    layer_info.check_whether_features_is_selected(job,'out','board',['board'],True,'r124.016')
    """
    try:
        reset_select_filter()
        clear_select(job, step, layer)
        filter_set_include_syms(has_symbols, symbols)
        select_features_by_filter(job, step, layers)
        comans = epcam_api.is_selected(job, step, layer)
        count = json.loads(comans)['result']
        return count
    except Exception as e:
        print(e)
    return '' 


def save_layer(job, step, layers, suffix):
    """
    备份多层（备份后的layer已存在将覆盖,需备份层无选中feature）
    :param     job:job名
    :param     step:stepming
    :param     layers:要备份的layer列表
    :param     suffix:备份的新layer后缀
    :returns   :
    :raises    error:
    Usage：    layer_info.save_layer(job, step, ['l1','l2'], '-bak')
    """
    try:
        layer_list = get_all_layer_name(job)
        for layer in layers:
            new_layer = layer + suffix
            if new_layer not in layer_list:
                job_operation.create_layer(job, new_layer)
            else:
                epcam_api.clear_selected_features(job, step, new_layer)
                counter_election(job, step, new_layer) 
                delete_feature(job, step, new_layer)  
                epcam_api.clear_selected_features(job, step, new_layer)
            sel_copy_other(job, step, [layer], [new_layer], False, 0, 0, 0, 0, 0, 0, 0)
    except Exception as e:
        print(e)
        return -1

def set_filter_by_inprofile(is_inprofile):#0:all 1:in 2:out
    """
    筛选器设置profile_value
    :param     is_inprofile:#0:all 1:in 2:out
    :returns   :
    :raises    error:
    Usage：    layer_info.set_filter_by_inprofile(1)
    """
    try:
        ret = epcam_api.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        epcam_api.set_select_param(select_param['featuretypes'], select_param['has_symbols'], select_param['symbols'], 
                                select_param['minline'], select_param['maxline'],
                                select_param['dcode'], select_param['attributes_flag'],
                                select_param['attributes_value'], is_inprofile,
                                select_param['use_selection'])
    except Exception as e:
        print(e)
    return 0

#改变Matrix孔层孔带
def change_drill_matrix(jobname, layer, start_name, end_name):
    """
    #改变layer的context
    :param     jobname:job名
    :param     layer:layer名
    :param     start_name:孔带起始层名
    :param     end_name:孔带结束层名
    :returns   :
    :raises    error:
    Usage：    layer_info.change_drill_matrix(job,'drl1-6','l1','l6')
    """
    try:
        ret = epcam_api.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
                if layer_infos[i]['name'] == layer:
                    layer_index = i + 1
                    layer_infos[i]['start_name'] = start_name
                    layer_infos[i]['end_name'] = end_name
        epcam_api.change_matrix(jobname, -1, layer_index, '', layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0


def add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, orient, attributes):
    """添加pad \n
    详细描述： 在当前层和影响层的对应位置添加一个pad\n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :param     layers(list): 层列表 \n
    :param     symbol(str): 添加的pad的symbol名（可以是usersymbol） \n
    :param     location_x(int): x坐标 (纳米)\n
    :param     location_y(int): y坐标 (纳米)\n
    :param     polarity:1:正极性    其他：负极性 \n
    :param     dcode: 默认为0 \n
    :param     orient:  0-3: 0°，90°，180°，270°顺时针旋转; \n
                        4-7: 0°，90°，180°，270°顺时针旋转+MIRROR; \n
                        8:no mirror+specialangle(0-360); \n
                        9:mirror+specialangle(0-360) \n
    :param     attributes：pad的attributes的list 例如：[{".drill":"via"},{".fiducial_name":"plated"}] \n
    Usage：    layer_info.add_pad(job,'out',[],'drl+1',‘r10',location_x, location_y, 1,  0, [])
    """
    try:
        dcode = -1
        epcam_api.add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, dcode, orient, attributes)
        pass
    except Exception as e:
        print(e)
        return False

#Layer.add_pad
def Layer_add_pad(job, step, layers, symbol, location_x, location_y, polarity, orient, attributes):
    """添加pad \n
    详细描述： 在当前层和影响层的对应位置添加一个pad\n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layers(list): 层列表 \n
    :param     symbol(str): 添加的pad的symbol名（可以是usersymbol） \n
    :param     location_x(int): x坐标 (纳米)\n
    :param     location_y(int): y坐标 (纳米)\n
    :param     polarity:1:正极性    其他：负极性 \n
    :param     dcode: 默认为0 \n
    :param     orient:  0-3: 0°，90°，180°，270°顺时针旋转; \n
                        4-7: 0°，90°，180°，270°顺时针旋转+MIRROR; \n
                        8:no mirror+specialangle(0-360); \n
                        9:mirror+specialangle(0-360) \n
    :param     attributes：pad的attributes的list 例如：[{".drill":"via"},{".fiducial_name":"plated"}] \n
    Usage：    layer_info.add_pad(job,'out',[],'drl+1',‘r10',location_x, location_y, 1,  0, [])
    """
    try:
        dcode = 0
        layer = ''
        if len(layers) > 0:
            layer = layers[0]
        epcam_api.add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, dcode, orient, attributes)
        pass
    except Exception as e:
        print(e)
        return False


def get_step_repeat(job, step):
    """获取拼板信息 \n
    详细描述： 拿到所有拼成当前step的所有拼版信息\n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    return      [{'NAME':'pcb','NX':5,'NY':5,'X':0,'Y':0,'DX':1000,'DY':1000,'ANGLE':'','MIRROR':'',},{},...]
    Usage：    layer_info.get_step_repeat(job,'out')
    """
    try:
        ret = epcam_api.get_step_repeat(job,step)
        data = json.loads(ret)
        return data['result']
    except Exception as e:
        print(e)
        return []



def select_all(job, step, layer):
    """ 全选 \n
    详细描述：  选中当前层中所有feature \n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :returns   :None \n
    :raises    error: \n
    Usage:     layer_info.select_all(job,'out','cmask+1')
    """
    try:
        epcam_api.clear_selected_features(job, step, layer)
        epcam_api.counter_election(job, step, layer)
    except Exception as e:
        print(e)
    return 0


def get_all_feature_infos(job, step, layer):
    """ 全选 \n
    详细描述：  获取当前层中所有feature信息 \n
    :param     job(str): 料名 \n
    :param     step(str): step名 \n
    :param     layer(str): 层名 \n
    :returns   :None \n
    :raises    error: \n
    Usage:     layer_info.select_all(job,'out','cmask+1')
    """
    try:
        select_all(job, step, layer)
        ret = epcam_api.is_selected(job, step, layer)
        data = json.loads(ret)
        # 没有被选中返回空数组
        if data['result'] == False:
            return []
        ret = epcam_api.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        return data['paras']
    except Exception as e:
        print(e)
    return 0
