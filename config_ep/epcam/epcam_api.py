import os,sys
import epcam as epcam
import json



#获取step, layer信息
def get_graphic(job):
    data = {
        'func': 'GET_GRAPHICS',
        'paras': {'job': job}
    }
    return epcam.process(json.dumps(data))

#设置属性筛选
def filter_set_attribute(logic, attribute_list):
    data = {
        'func': 'FILTER_SET_ATR',
        'paras': [{'logic': logic},
                  {'attributes_value': attribute_list}]
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#根据筛选选择feature
def select_features_by_filter(job, step, layers):
    data = {
            'func': 'SELECT_FEATURES_BY_FILTER',
            'paras': [{'job': job},
                      {'step': step},
                      {'layer': layers}]
        }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#feature涨缩
#sel_type : 0 selected 1 all
def resize_global(job, step, layers, sel_type, size):
    data = {
            'func': 'GLOBAL_RESIZE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'sel_type': sel_type},
                      {'size': size},
                      {'corner': False}]
        }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#打开料号
def open_job(path, job):
    data = {
        'func': 'OPEN_JOB',
        'paras': [{'path': path},
                  {'job': job}]
    }
    # print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#关闭料号
def close_job(job):
    data = {
        'func': 'CLOSE_JOB',
        'paras':
                  {'job': job}
    }
    # print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#保存料号
def save_job(job):
    data = {
        'func': 'JOB_SAVE',
        'paras': [{'job': job}]
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#获取当前层所有的feature的symbol信息
def get_all_features_report(job, step, layer):
    data = {
        'func': 'GET_ALL_FEATURES_REPORT',
        'paras': {'job': job,
                  'step': step,
                  'layer': layer}
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#获取当前的筛选条件
def get_select_param():
    data = {
        'func': 'GET_SELECT_PARAM',
        'paras': {}
    }
    return epcam.process(json.dumps(data))

#设置新的筛选条件    profile_value//0: all 1: in  2: out
def set_select_param(featuretypes, has_symbols, symbols, minline, maxline, dcode, attributes_flag, attributes_value,
                        profile_value, use_selection):
    data = {
        'func': 'SET_SELECT_PARAM',
        'paras': {'param':{
                  'featuretypes': featuretypes,
                  'has_symbols': has_symbols,
                  'symbols': symbols,
                  'minline': minline,
                  'maxline': maxline,
                  'dcode': dcode,
                  'attributes_flag': attributes_flag,
                  'attributes_value': attributes_value,
                  'profile_value': profile_value,
                  'use_selection': use_selection}
                  }
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#创建新层
def create_new_layer(job, step, layer, index):
    data = {
        'func': 'CREATE_NEW_LAYER',
        'paras': {'job': job,
                  'step': step,
                  'layer': layer,
                  'index': index}
    }
    epcam.process(json.dumps(data))

#创建新step
def create_step(jobname, stepname, index):
    data = {
        'func': 'CREATE_STEP',
        'paras': {'jobname': jobname,
                  'stepname': stepname,
                  'index': index}
    }
    epcam.process(json.dumps(data))

#修改job名
def job_rename(src_jobname, dst_jobname):
    data = {
        'func': 'JOB_RENAME',
        'paras': {'src_jobname': src_jobname,
                  'dst_jobname': dst_jobname }
    }
    epcam.process(json.dumps(data))

#修改matrix信息
def change_matrix(jobname, old_step_index, old_layer_index, new_step_name, new_layer_info):
    data = {
        'func': 'CHANGE_MATRIX',
        'paras': {'jobname': jobname,
                  'old_step_index': old_step_index,
                  'old_layer_index': old_layer_index,
                  'new_step_name': new_step_name,
                  'new_layer_info': new_layer_info}
    }
    epcam.process(json.dumps(data))

#获取matrix信息
def get_matrix(job):
    data = {
        'func': 'GET_MATRIX',
        'paras': {'job': job}
    }
    # print(json.dumps(data))
    return epcam.process(json.dumps(data))

#加载layer
def open_layer(job, step, layer):
    data = {
        'func': 'OPEN_LAYER',
        'paras': {'jobname': job,
                  'step': step,
                  'layer': layer}
    }
    epcam.process(json.dumps(data))
    return epcam.process(json.dumps(data))

#copy layer
def copy_layer(jobname, org_layer_index, dst_layer, poi_layer_index):
    data = {
        'func': 'COPY_LAYER',
        'paras': {'jobname': jobname,
                  'org_layer_index': org_layer_index,
                  'dst_layer': dst_layer,
                  'poi_layer_index': poi_layer_index }
    }
    return epcam.process(json.dumps(data))

#删除料号
def job_delete(jobname):
    data = {
        'func': 'JOB_DELETE',
        'paras': {'src_jobname': jobname}
    }
    epcam.process(json.dumps(data))

#删除feature
def sel_delete(job, step, layers):
    data = {
            'func': 'SEL_DELETE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers}]
    }
    epcam.process(json.dumps(data))

#清空选择
def clear_selected_features(job, step, layer):
    data = {
            'func': 'CLEAR_SELECTED_FEATURES',
            'paras': {'job': job,
                      'step': step,
                      'layer': layer}
    }
    #print(json.dumps(data))
    epcam.process(json.dumps(data))

#获取当前层所有选中的feature的symbol信息
def get_selected_features_report(job, step, layer):
    data = {
        'func': 'GET_SELECTED_FEATURES_REPORT',
        'paras': {'job': job,
                  'step': step,
                  'layer': layer}
    }
    ret = epcam.process(json.dumps(data))
    return ret

def filter_by_mode(jobname, step, layer, reference_layers, mode, feature_type_ref, symbolflag , symbolnames, attrflag = -1,
                    attrlogic = 0, attributes = []):
    data = {
        'func': 'FILTER_BY_MODE',
        'paras': {'jobname': jobname,
                  'step': step,
                  'layer': layer,
                  'reference_layers': reference_layers,
                  'mode': mode,
                  'feature_type_ref': feature_type_ref,
                  'symbolflag': symbolflag,
                  'symbolnames': symbolnames,
                  'attrflag': attrflag,
                  'attrlogic': attrlogic,
                  'attributes': attributes
                  }
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#孔分析
def drill_check(job, step, layers, erf, rout_distance, hole_size, extra_holes, hole_seperation, power_ground_short, missing_hole,
                npth_to_rout, use_pth, use_npth, use_via, compensated_rout, ranges):
    data = {
        'func': 'DRILL_CHECK',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'rout_distance': rout_distance},
                  {'hole_size': hole_size},
                  {'extra_holes': extra_holes},
                  {'hole_seperation': hole_seperation},
                  {'power_ground_short': power_ground_short},
                  {'missing_hole': missing_hole},
                  {'npth_to_rout': npth_to_rout},
                  {'use_pth': use_pth},
                  {'use_npth': use_npth},
                  {'use_via': use_via},
                  {'compensated_rout': compensated_rout},
                  {'ranges':ranges}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#插入layer
def insert_layer(job, poi_layer_index):
    data = {
            'func': 'LAYER_INSERT',
            'paras': [{'job': job},
                      {'poi_layer_index': poi_layer_index}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#添加symbol筛选
def filter_set_include_syms(has_symbols, symbols):
    data = {
            'func': 'FILTER_SET_INCLUDE_SYMS',
            'paras': [{'has_symbols': True},
                      {'symbols': symbols}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#反选
def counter_election(job, step, layer):
    data = {
            'func': 'COUNTER_ELECTION',
            'paras': [{'job': job},
                      {'step': step},
                      {'layer': layer}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#选中feature
"""selectpolygon :eg.[[0,0],[1,1]]"""
def select_feature(job, step, layer, selectpolygon, featureInfo, margin, clear):
    data = {
            'func': 'SELECT_FEATURE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layer': layer},
                      {'selectpolygon': selectpolygon},
                      {'featureInfo': featureInfo},
                      {'type': margin},#0:单选          1：框选
                      {'clear': clear}
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#修改文字
def change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror, angle = 0):
    data = {
            'func': 'TEXT_CHANGE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'text': text},
                      {'font': font},
                      {'x_size': x_size},
                      {'y_size': y_size},
                      {'width': width},
                      {'polarity': polarity},
                      {'mirror': mirror},
                      {'angle': angle}
                      ]
        }
    print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
#内外层分析
def signal_layer_check(job, step, layers, erf, pp_spacing, drill2cu, rout2cu, sliver_min, min_pad_overlap, spacing, stubs,
                        drill, center, rout, smd, size, bottleneck, sliver, pad_connection_check,
                        apply_to, check_missing, use_compensated_rout, sort_spacing, ranges):
    data = {
        'func': 'SIGNAL_LAYER_CHECK',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'erf': erf},
                  {'pp_spacing': pp_spacing},
                  {'drill2cu': drill2cu},
                  {'rout2cu': rout2cu},
                  {'sliver_min': sliver_min},
                  {'min_pad_overlap': min_pad_overlap},
                  {'spacing': spacing},
                  {'stubs': stubs},
                  {'drill': drill},
                  {'center': center},
                  {'rout': rout},
                  {'smd': smd},
                  {'size': size},
                  {'bottleneck': bottleneck},
                  {'sliver': sliver},
                  {'pad_connection_check': pad_connection_check},
                  {'apply_to': apply_to},
                  {'check_missing': check_missing},
                  {'use_compensated_rout': use_compensated_rout},
                  {'sort_spacing': sort_spacing},
                  {'ranges': ranges}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#内外层优化
def signal_layer_DFM(job, step, layers, erf, pth_ar_min, pth_ar_opt, via_ar_min, via_ar_opt, mvia_ar_min, mvia_ar_opt, spacing_min, spacing_opt,
				pad_to_pad_spacing_min, pad_to_pad_spacing_opt, lre_range_fr, lre_range_to, reduction, abs_min, drill_to_cu,
			    apply_to, pads, smds, drills, padup, shave, paddn, rerout, linedn, reshape, padup_can_touch_pad, cut_pad_touch_pad, laser_ar_min,
                laser_ar_opt, buried_min, buried_opt, ranges):
    data = {
        'func': 'SIGNAL_LAYER_DFM',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'erf': erf},
                  {'pth_ar_min': pth_ar_min},
                  {'pth_ar_opt': pth_ar_opt},
                  {'via_ar_min': via_ar_min},
                  {'via_ar_opt': via_ar_opt},
                  {'mvia_ar_min': mvia_ar_min},
                  {'mvia_ar_opt': mvia_ar_opt},
                  {'spacing_min': spacing_min},
                  {'spacing_opt': spacing_opt},
                  {'pad_to_pad_spacing_min': pad_to_pad_spacing_min},
                  {'pad_to_pad_spacing_opt': pad_to_pad_spacing_opt},
                  {'lre_range_fr': lre_range_fr},
                  {'lre_range_to': lre_range_to},
                  {'reduction': reduction},
                  {'abs_min': abs_min},
                  {'drill_to_cu': drill_to_cu},
                  {'apply_to': apply_to},
                  {'pads': pads},
                  {'smds': smds},
                  {'drills': drills},
                  {'padup': padup},
                  {'shave': shave},
                  {'paddn': paddn},
                  {'rerout': rerout},
                  {'linedn': linedn},
                  {'reshape': reshape},
                  {'padup_can_touch_pad': padup_can_touch_pad},
                  {'cut_pad_touch_pad': cut_pad_touch_pad},
                  {'laser_ar_min': laser_ar_min},
                  {'laser_ar_opt': laser_ar_opt},
                  {'buried_ar_min': buried_min},
                  {'buried_ar_opt': buried_opt},
                  {'ranges': ranges}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#打散feature
def sel_break(job, step, layers, sel_type):
    data = {
            'func': 'SEL_BREAK',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'sel_type': sel_type}
                      ]
        }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#复制Step
def copy_step(job, org_step_index, dst_step, poi_step_index):
    data = {
            'func': 'COPY_STEP',
            'paras': {'jobname': job,
                      'org_step_index': org_step_index,
                      'dst_step': dst_step,
                      'poi_step_index': poi_step_index}
        }
    ret = epcam.process(json.dumps(data))
    return ret

#插入step
def insert_step(job, poi_step_index):
    data = {
            'func': 'INSERT_STEP',
            'paras': {'jobname': job,
                      'poi_step_index': poi_step_index}
    }
    ret = epcam.process(json.dumps(data))

#layer_compare_bmp
def layer_compare_bmp(jobname1, stepname1, layername1, jobname2, stepname2,layername2, tolerance, grid_size, savepath, suffix, bmp_width, bmp_height):
    data = {
                'func': 'LAYER_COMPARE_BMP',
                'paras': {  'jobname1': jobname1,
                            'stepname1': stepname1,
                            'layername1': layername1,
                            'jobname2': jobname2,
                            'stepname2': stepname2,
                            'layername2': layername2,
                            'tolerance': tolerance,
                            'grid_size': grid_size,
                            'savepath': savepath,
                            'suffix': suffix,
                            'bmp_width': bmp_width,
                            'bmp_height': bmp_height}
           }
    ret = epcam.process(json.dumps(data))
    return ret

#泪滴优化
def teardrop_create_DFM(job, step, layers, erf, sel_type, drilled_pads, undrilled_pads, ann_ring_min, drill_size_min, drill_size_max,
                        cu_spacing, drill_spacing, delete_old_teardrops, apply_to, work_mode, use_arc_tear, arc_angle, bga_pads,
                        tear_line_width_ratio, ranges):
    data = {
        'func': 'TEARDROP_CREATE_DFM',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'erf': erf},
                  {'type': sel_type},
                  {'drilled_pads': drilled_pads},
                  {'undrilled_pads': undrilled_pads},
                  {'ann_ring_min': ann_ring_min},
                  {'drill_size_min': drill_size_min},
                  {'drill_size_max': drill_size_max},
                  {'cu_spacing': cu_spacing},
                  {'drill_spacing': drill_spacing},
                  {'delete_old_teardrops': delete_old_teardrops},
                  {'apply_to': apply_to},
                  {'work_mode': work_mode},
                  {'use_arc_tear': use_arc_tear},
                  {'arc_angle': arc_angle},
                  {'bga_pads': bga_pads},
                  {'tear_line_width_ratio': tear_line_width_ratio},
                  {'ranges': ranges}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#拼板
def step_repeat(job, parentstep, childsteps):
    data = {
            'func': 'STEP_REPEAT',
            'paras': {'jobname': job,
                      'parentstep': parentstep,
                      'childsteps': childsteps}
    }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#设置基准点
def set_datum_point(job, stepname, point_x, point_y):
    data = {
            'func': 'SET_DATUM_POINT',
            'paras': {'jobname': job,
                      'stepname': stepname,
                      'point': {'ix': point_x, 'iy': point_y}}
    }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#获取profile box
def get_profile_box(job, step):
    data = {
            'func': 'PROFILE_BOX',
            'paras': {'job': job,
                      'step': step}
    }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#修改feature的叠放顺序
def sel_index(job, step, layers, mode):
    data = {
            'func': 'SEL_INDEX',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'mode': mode}]
    }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#新建profile线
def create_profile(jobname, stepname, layername):
    data = {
        'func': 'CREATE_PROFILE',
        'paras': {'jobname': jobname,
                  'stepname': stepname,
                  'layername': layername}
    }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#添加线
# polarity:1 P 0 N
def add_line(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, polarity, dcode, attributes):
    data = {
        'func': 'ADD_LINE',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'start_x': start_x},
                  {'start_y': start_y},
                  {'end_x': end_x},
                  {'end_y': end_y},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'attributes': attributes}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#跨层复制feature
def sel_copy_other(src_job, src_step, src_layers, dst_layers, invert, offset_x, offset_y,
                    mirror, resize, rotation, x_anchor, y_anchor):
    data = {
        'func': 'SEL_COPY_OTHER',
        'paras': [{'src_job': src_job},
                  {'src_step': src_step},
                  {'src_layers': src_layers},
                  {'dst_layers': dst_layers},
                  {'invert': invert},
                  {'offset_x': offset_x},
                  {'offset_y': offset_y},
                  {'mirror': mirror},
                  {'resize': resize},
                  {'rotation': rotation},
                  {'x_anchor': x_anchor},
                  {'y_anchor': y_anchor}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

"""
#删除layer
:param     job:
:param     layer_index:
:returns   :
:raises    error:
"""
def delete_layer(job, layer_index):
    data = {
            'func': 'DELETE_LAYER',
            'paras': {'jobname': job,
                      'layer_index': layer_index}
        }
    ret = epcam.process(json.dumps(data))

#profile线间新建layer
def create_layer_between_profile(jobname, stepname, new_layername, child_profile_margin):
    data = {
        'func': 'CREATE_LAYER_BETWEEN_PROFILE',
        'paras':  {'jobname': jobname,
                   'stepname': stepname,
                   'new_layername': new_layername,
                   'child_profile_margin': child_profile_margin}
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#添加surface
def add_surface(job, step, layers, layer, polarity, dcode, isround, attributes, points_location):
    data = {
        'func': 'ADD_SURFACE',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'isround': isround},
                  {'attributes': attributes},
                  {'points_location': points_location}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#区域切割(profile)
def clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype):
    data = {
            'func': 'CLIP_AREA_USE_PROFILE',
            'paras': {'job': job,
                      'step': step,
                      'layer': layers,
                      'clipinside': clipinside,
                      'clipcontour': clipcontour,
                      'margin': margin,
                      'featuretype': featuretype,}
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#避铜
def avoid_conductor_DFM_op(jobname, stepname, layernames, erf, coverage_min, coverage_opt, radius_opt, mending_copper_wire,
                            is_fast, use_global, viadrill2cu, pthdrill2cu):
    data = {
            'func': 'AVOID_CONDUCTOR_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'coverage_min': coverage_min},
                      {'coverage_opt': coverage_opt},
                      {'radius_opt': radius_opt},
                      {'mending_copper_wire': mending_copper_wire},
                      {'is_fast': is_fast},
                      {'use_global': use_global},
                      {'pthdrill2cu': pthdrill2cu},
                      {'viadrill2cu': viadrill2cu}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#去尖角
def remove_sharp_angle(job, step, layers, scope, radius, remove_type, is_round):
    data = {
            'func': 'REMOVE_SHARP_ANGLE',
            'paras': {'para':
                     {'job': job,
                      'step': step,
                      'layers': layers,
                      'scope': scope,
                      'radius': radius,
                      'type': remove_type,
                      'is_round': is_round}
                      }
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#获取当前层所有选中的feature的symbol信息
"""
featureinfo:
type:   1        pad
            2       line
            4       surface
            8       arc
            16      text
            32      barcode
            64      text_plus
            0       unknow
"""
def get_selected_feature_infos(job, step, layer):
    data = {
        'func': 'GET_SELECTED_FEATURE_INFOS',
        'paras': {'jobname': job,
                  'stepname': step,
                  'layername': layer}
    }
    ret = epcam.process(json.dumps(data))
    return ret

# #获取当前层所有feature的symbol信息
# def get_all_feature_infos(job, step, layer):
#     data = {
#         'func': 'GET_ALL_FEATURE_INFOS',
#         'paras': {'jobname': job,
#                   'stepname': step,
#                   'layername': layer}
#     }
#     ret = epcam.process(json.dumps(data))
#     return ret

#防焊层优化
def solder_mask_DFM(job, step, layers, erf, clearance_min, clearance_opt, coverage_min, coverage_opt, bridge_size,
                    apply_to, use_existing_mask, use_shaves, do_resize, max_oversized_clearance, intersect_width,
                    cut_surplus_width, cut_surplus_height, is_round, fan_shaved, prevent_vertical_flow_add_sm,
                    prevent_vertical_flow_del_sm,
                    drill_clearance_min , drill_clearance_opt , smd_clearance_min,
				    smd_clearance_opt , bga_clearance_min, bga_clearance_opt, add_outline, outline_width,
                    he_hong_resize_sm_in_surface, resize_gas_sm_no_drill, resize_gas_sm_has_drill,
                    add_v_cut_sm_size, resize_sm_surface_size, pth_fan_shave, pad_covered_clearance, ranges):
    data = {
            'func': 'SOLDER_MASK_DFM',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'erf': erf},
                      {'clearance_min': clearance_min},
                      {'clearance_opt': clearance_opt},
                      {'coverage_min': coverage_min},
                      {'coverage_opt': coverage_opt},
                      {'bridge_size': bridge_size},
                      {'apply_to': apply_to},
                      {'use_existing_mask': use_existing_mask},
                      {'use_shaves': use_shaves},
                      {'do_resize': do_resize},
                      {'max_oversized_clearance': max_oversized_clearance},
                      {'intersect_width': intersect_width},
                      {'cut_surplus_width': cut_surplus_width},
                      {'cut_surplus_height': cut_surplus_height},
                      {'is_round': is_round},
                      {'fan_shaved': fan_shaved},
                      {'prevent_vertical_flow_add_sm': prevent_vertical_flow_add_sm},
                      {'prevent_vertical_flow_del_sm': prevent_vertical_flow_del_sm},
                      {'drill_clearance_min': drill_clearance_min},
                      {'drill_clearance_opt': drill_clearance_opt},
                      {'smd_clearance_min': smd_clearance_min},
                      {'smd_clearance_opt': smd_clearance_opt},
                      {'bga_clearance_min': bga_clearance_min},
                      {'bga_clearance_opt': bga_clearance_opt},
                      {'add_outline': add_outline},
                      {'outline_width': outline_width},
                      {'he_hong_resize_sm_in_surface': he_hong_resize_sm_in_surface},
                      {'resize_gas_sm_no_drill': resize_gas_sm_no_drill},
                      {'resize_gas_sm_has_drill': resize_gas_sm_has_drill},
                      {'add_v_cut_sm_size': add_v_cut_sm_size},
                      {'resize_sm_surface_size': resize_sm_surface_size},
                      {'pth_fan_shave': pth_fan_shave},
                      {'pad_covered_clearance': pad_covered_clearance},
                      {'ranges': ranges}
                     ]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#求一个范围内最小距离
def get_selected_feature_min_spacing(jobname, stepname, layername, search_radium, min_spacing):
    data = {
            'func': 'GET_SELECTED_FEATURE_MIN_SPACING',
            'paras': {
                      'jobname': jobname,
                      'stepname': stepname,
                      'layername': layername,
                      'search_radium': search_radium,
                      'min_spacing': min_spacing
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#移动layer
def move_layer(jobname, org_layer_index, dst_layer_index):
    data = {
            'func': 'MOVE_LAYER_POI',
            'paras': {
                      'jobname': jobname,
                      'org_layer_index': org_layer_index,
                      'dst_layer_index': dst_layer_index,
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#contour to pad
def contour2pad(job, step, layers, tol, minsize, maxsize, suffix):
    data = {
            'func': 'CONTOUR2PAD',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'tol': tol},
                      {'minsize': minsize},
                      {'maxsize': maxsize},
                      {'suffix': suffix}
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#resize_polyline
def resize_polyline(job, step, layers, size, sel_type):
    data = {
            'func': 'POLYLINE_RESIZE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'size': size},
                      {'sel_type': sel_type},
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#求最小公差
def get_min_tolerance(jobname, stepname, layername1, layername2, selectbox):
    data = {
            'func': 'GET_MIN_TOLERANCE',
            'paras': {
                      'jobname': jobname,
                      'stepname': stepname,
                      'layername1': layername1,
                      'layername2': layername2,
                      'selectbox': selectbox
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

"""
#删除step
:param     job:
:param     step_index:
:returns   :
:raises    error:
"""
def delete_step(job, step_index):
    data = {
            'func': 'DELETE_STEP',
            'paras': {'jobname': job,
                      'step_index': step_index}
        }
    ret = epcam.process(json.dumps(data))
#跨层移动feature
def sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y,
                    mirror, resize, rotation, x_anchor, y_anchor):
    data = {
        'func': 'SEL_MOVE_OTHER',
        'paras': [{'src_job': src_job},
                  {'src_step': src_step},
                  {'src_layers': src_layers},
                  {'dst_job': dst_job},
                  {'dst_step': dst_step},
                  {'dst_layer': dst_layer},
                  {'invert': invert},
                  {'offset_x': offset_x},
                  {'offset_y': offset_y},
                  {'mirror': mirror},
                  {'resize': resize},
                  {'rotation': rotation},
                  {'x_anchor': x_anchor},
                  {'y_anchor': y_anchor}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#smd_bga pad 优化
def smd_bga_DFM_op(jobname, stepname, layernames, erf, smd_bga_spacing_opt, max_padup_value):
    data = {
            'func': 'SMD_BGA_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'smd_bga_spacing_opt': smd_bga_spacing_opt},
                      {'max_padup_value': max_padup_value}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#load layer
def load_layer(jobname, stepname, layername):
    data = {
            'func': 'LOAD_LAYER',
            'paras': {'jobname': jobname,
                      'stepname': stepname,
                      'layername': layername}
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置显示模式
def set_display_widths(width):
    data = {
            'func': 'SET_DISPLAY_WIDTHS',
            'paras': [{'width': width}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置文字显示模式
def set_display_text(disp):
    data = {
            'func': 'SET_DISPLAY_TEXT',
            'paras': [{'disp': disp}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置单位
def set_units(units):
    data = {
            'func': 'SET_UNITS',
            'paras': [{'units': units}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#设置是否显示profile线
def set_display_profile(mode):
    data = {
            'func': 'SET_DISPLAY_PROFILE',
            'paras': [{'mode': mode}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#获取显示参数
def get_show_para(mode):
    data = {
            'func': 'SET_DISPLAY_PROFILE',
            'paras': [{'mode': mode}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#避npth孔和profile线 优化
def avoid_features_DFM_op(jobname, stepname, layernames, erf, avoid_profile, avoid_profile_size, avoid_npth, avoid_npth_size,
                            avoid_alone_drill, avoid_alone_drill_size, npth_add_solder_mask, npth_add_solder_mask_size, avoid_v_cut):
    data = {
            'func': 'AVOID_FEATURES_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'avoid_profile': avoid_profile},
                      {'avoid_profile_size': avoid_profile_size},
                      {'avoid_npth': avoid_npth},
                      {'avoid_npth_size': avoid_npth_size},
                      {'avoid_alone_drill': avoid_alone_drill},
                      {'avoid_alone_drill_size': avoid_alone_drill_size},
                      {'npth_add_solder_mask': npth_add_solder_mask},
                      {'npth_add_solder_mask_size': npth_add_solder_mask_size},
                      {'avoid_v_cut_size': avoid_v_cut}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#sliver 优化
def sliver_DFM_op(jobname, stepname, layernames, erf, max_width, max_height):
    data = {
            'func': 'SLIVER_DFM_OP',
            'paras': [{'jobname': jobname},
                      {'stepname': stepname},
                      {'layernames': layernames},
                      {'erf': erf},
                      {'max_width': max_width},
                      {'max_height': max_height}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#contourize
def contourize(job, step, layers, accuracy, separate_to_islands, size, mode):
    data = {
            'func': 'CONTOURIZE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'accuracy': accuracy},
                      {'separate_to_islands': separate_to_islands},
                      {'size': size},
                      {'mode': mode},]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#identify
def file_identify(path):
    data = {
            'func': 'FILE_IDENTIFY',
            'paras': {'pathname': path}
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

def set_selection(is_standard, is_clear, all_layers, is_select, inside, exclude):
    data = {
            'func': 'SET_SELECTION',
            'paras': {'sels': {
                      'is_standard': is_standard,
                      'is_clear': is_clear,
                      'all_layers': all_layers,
                      'is_select': is_select,
                      'inside': inside,
                      'exclude': exclude}
                      }
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#去除独立pad优化
def NFP_removal_DFM(job, step, layers, erf, isolated, drill_over, duplicate, covered, work_on, pth, pth_pressfit, npth,
                    via_laser, via, via_photo, remove_undrilled_pads, apply_to, remove_mark_NFP, ranges):
    data = {
            'func': 'NFP_REMOVAL_DFM',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'erf': erf},
                      {'isolated': isolated},
                      {'drill_over': drill_over},
                      {'duplicate': duplicate},
                      {'covered': covered},
                      {'work_on': work_on},
                      {'pth': pth},
                      {'pth_pressfit': pth_pressfit},
                      {'npth': npth},
                      {'via_laser': via_laser},
                      {'via': via},
                      {'via_photo': via_photo},
                      {'remove_undrilled_pads': remove_undrilled_pads},
                      {'apply_to': apply_to},
                      {'remove_mark_NFP': remove_mark_NFP},
                      {'ranges': ranges}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#neo削PAD
def New_signal_layer_DFM(job, step, layers, erf, cut_pad_touch_pad, drill_to_cu):
    data = {
        'func': 'NEW_SIGNAL_LAYER_DFM',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'erf': erf},
                  {'cut_pad_touch_pad': cut_pad_touch_pad},
                  {'drill_to_cu': drill_to_cu}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#设置梯形图relationship
def setRelationship(colname, rowname, relation_value, relation_ratio):
    data = {
        'func': 'SETRELATIONSHIP',
        'paras': [{'colname': colname},
                  {'rowname': rowname},
                  {'relation_value': relation_value},
                  {'relation_ratio': relation_ratio}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#获取梯形图relationship
def getRelationship():
    data = {
        'func': 'GETRELATIONSHIP',
        'paras': []
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#设置梯形图Introduction
def setIntroduction(attributename, min_resize, min_ring, opt_resize, opt_ring, is_shave):
    data = {
        'func': 'SETINTRODUCTION',
        'paras': [{'attributename': attributename},
                  {'min_resize': min_resize},
                  {'min_ring': min_ring},
                  {'opt_resize': opt_resize},
                  {'opt_ring': opt_ring},
                  {'is_shave': is_shave}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#获取梯形图Introduction
def getIntroduction():
    data = {
        'func': 'GETINTRODUCTION',
        'paras': []
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret


#料号另存为
def save_job_as(job, path):
    data = {
            'func': 'SAVE_JOB_AS',
            'paras': {
                      'job': job,
                      'path': path
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#添加pad
def add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, dcode, orient, attributes, special_angle = 0):
    if symbol=="":
        return
    aa = identify_symbol(symbol)
    ret=json.loads(identify_symbol(symbol))['result']
    if not ret:
        aa=json.loads(is_job_open('eplib'))['paras']['status']
        if aa:
            copy_usersymbol_to_other_job('eplib',job, symbol, symbol)
    data = {
        'func': 'ADD_PAD',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'location_x': location_x},
                  {'location_y': location_y},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'orient': orient},
                  {'attributes': attributes},
                  {'special_angle' : special_angle}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))


#取消选中
def unselect_features(job, step, layer):
    data = {
            'func': 'UNSELECT_FEATURES',
            'paras': {
                      'job': job,
                      'step': step,
                      'layer': layer
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#根据筛选器取消选中
def unselect_features_by_filter(job, step, layer):
    data = {
            'func': 'UNSELECT_FEATURES_BY_FILTER',
            'paras': {
                      'job': job,
                      'step': step,
                      'layer': layer
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#dms create job
def DMS_create_job(job):
    data = {
        'func': 'DMS_CREATE_JOB',
        'paras': {'job': job}

        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

def load_job_from_db(job_id, odb_jobname, db_jobname):
    data = {
        'func': 'LOADJOBFROMDB',
        'paras': {'job_id': job_id,
                    'odb_jobname': odb_jobname,
                    'db_jobname': db_jobname }

        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

def login(username, password):
    data = {
        'func': 'LOGIN',
        'paras': {'name': username,
                    'pwd': password }
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

# #设置机器人参数
# def setParameter(layer, pa, value):
#     data = {
#         'func': 'SETPARAMETER',
#         'paras': [{'layer': layer},
#                   {'pa': pa},
#                   {'value': value}]
#     }
#     #print(json.dumps(data))
#     ret = epcam.process(json.dumps(data))

#设置机器人参数
def setParameter(rules):
    data = {
        'func': 'SETPARAMETER',
        'paras': [{'rules': rules}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))
    return ret

#设置参数(整个料)
def setJobParameter(jobName,rules):
    data = {
        'func': 'SETJOBPARAMETER',
        'paras': {
                      'rules': rules,
                      'jobName': jobName
                      }
    }
    ret = epcam.process(json.dumps(data))
    return ret

#设置参数(整个料)
def getJobParameter(jobName):
    data = {
        'func': 'GETJOBPARAMETER',
        'paras': {
                      'job': jobName
                      }
    }
    ret = epcam.process(json.dumps(data))
    return ret

#获取机器人参数
def getParameter():
    data = {
        'func': 'GETPARAMETER',
        'paras': []
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#打开eps文件
def open_eps(job, path):
    data = {
        'func': 'OPEN_EPS',
        'paras': {
                      'job': job,
                      'path': path
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#设置分析结果
def set_layer_checklist(jobName, stepName,layerName,checkList):
    data = {
        'func': 'SET_LAYER_CHECKLIST',
        'paras': {
                      'jobName': jobName,
                      'stepName': stepName,
                      'layerName':layerName,
                      'checkList':checkList
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#translate
def file_translate(path, job, step, layer, parameters, start_time, end_time, assigned_dcodes, defect_reports):
    data = {
        'func': 'FILE_TRANSLATE',
        'paras': {
                    'path': path,
                    'job': job,
                    'step': step,
                    'layer': layer,
                    'parameters': parameters,
                    'start_time': start_time,
                    'end_time': end_time,
                    'assigned_dcodes': assigned_dcodes,
                    'defect_reports': defect_reports
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#创建料号（无路径）
def job_create(job):
    data = {
        'func': 'JOB_CREATE',
        'paras': {
                    'job': job
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#translate init
def file_translate_init(job):
    data = {
        'func': 'FILE_TRANSLATE_INIT',
        'paras': {
                    'job': job
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#创建料号（有路径）
def create_job(path, job):
    data = {
        'func': 'CREATE_JOB',
        'paras': {
                    'path': path,
                    'job': job
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#删除料号
def delete_job(job):
    data = {
            'func': 'JOB_DELETE',
            'paras': {
                      'src_jobname': job
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

#identify eps
def identify_eps(job, path):
    data = {
            'func': 'IDENTIFY_EPS',
            'paras': {
                      'job': job,
                      'path': path
                      }
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))
    return ret

def add_outline_drill(job, step, outerline_layer, drill_layer, add_drill_symbolname, move_offset_in_corner, angle_tolerance):
    data = {
        'func': 'ADD_OUTLINE_DRILL',
        'paras': [{'job': job},
                  {'step': step},
                  {'outerline_layer': outerline_layer},
                  {'drill_layer': drill_layer},
                  {'add_drill_symbolname': add_drill_symbolname},
                  {'move_offset_in_corner': move_offset_in_corner},
                  {'angle_tolerance': angle_tolerance}]
    }
    #print(json.dumps(data))
    ret = epcam.process(json.dumps(data))

#get_coupon_single_end_drill_positions
def get_coupon_single_end_drill_positions(xmin, ymin, xmax, ymax, x_margin, y_margin, npth_size, pth_size, pth_ring, avoid_cu_global, clearance,
                                        pth_to_gnd_drill, min_cu_width, single_lines, differential_lines):
    data = {
        'func': 'GET_COUPON_SINGLE_END_DRILL_POSITIONS',
        'paras': {
                    'xmin': xmin,
                    'ymin': ymin,
                    'xmax': xmax,
                    'ymax': ymax,
                    'x_margin': x_margin,
                    'y_margin': y_margin,
                    'npth_size': npth_size,
                    'pth_size': pth_size,
                    'pth_ring': pth_ring,
                    'avoid_cu_global': avoid_cu_global,
                    'clearance': clearance,
                    'pth_to_gnd_drill': pth_to_gnd_drill,
                    'min_cu_width': min_cu_width,
                    'single_lines': single_lines,
                    'differential_lines': differential_lines
                    }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#index筛选
def select_feature_by_id(job, step, layer, ids):
    data = {
        'func': 'SELECT_FEATURE_BY_ID',
        'paras': {
                    'job': job,
                    'step': step,
                    'layer': layer,
                    'ids': ids
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#设置profile
def set_step_profile(job, step, points):
    data = {
        'func': 'SET_STEP_PROFILE',
        'paras': {
                    'job': job,
                    'step': step,
                    'points': points
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#change symbol
def change_feature_symbols(job, step, layers, symbol, pad_angle):
    data = {
        'func': 'CHANGE_FEATURE_SYMBOLS',
        'paras': {
                    'job': job,
                    'step': step,
                    'layers': layers,
                    'symbol': symbol,
                    'pad_angle': pad_angle
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#clip_area_use_reference
def clip_area_use_reference(jobname, stepname, work_layers, reference_layer, margin, clipcontour, featuretype):
    data = {
        'func': 'CLIP_AREA_USE_REFERENCE',
        'paras': {
                    'jobname': jobname,
                    'stepname': stepname,
                    'work_layer': work_layers,
                    'reference_layer': reference_layer,
                    'margin': margin,
                    'clipcontour': clipcontour,
                    'featuretype': featuretype
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#clip_area_use_manual
def clip_area_use_manual(jobname, stepname, layers, points, margin, clipcontour,clipinside, featuretype):
    data = {
        'func': 'CLIP_AREA_USE_MANUAL',
        'paras': {
                    'job': jobname,
                    'step': stepname,
                    'layers': layers,
                    'points': points,
                    'margin': margin,
                    'clipcontour': clipcontour,
                    'clipinside': clipinside,
                    'featuretype': featuretype
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#line2pad_new
def line2pad_new(job, step, layers):
    data = {
        'func': 'RESHAPE_LINE_TO_PAD_NEW',
        'paras': {
                    'job': job,
                    'step': step,
                    'layers': layers
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))


#pth npth开窗
def npth_and_pth_prepare_op(job, step, sm_clearance, sm_np_clearance, add_sm_pads, add_signal_pads):
    data = {
        'func': 'NPTH_AND_PTH_PREPARE_OP',
        'paras': {
                    'job': job,
                    'step': step,
                    'sm_clearance': sm_clearance,
                    'sm_np_clearance': sm_np_clearance,
                    'add_sm_pads': add_sm_pads,
                    'add_signal_pads': add_signal_pads
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#修改属性
def modify_attributes(job, step, layers, mode, attributes):
    data = {
        'func': 'MODIFY_ATTRIBUTES',
        'paras': {
                    'jobname': job,
                    'stepname': step,
                    'layernames': layers,
                    'mode': mode,
                    'attributes': attributes
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#coupon获取线的坐标
def get_coupon_drill_line_relations(xmin, ymin, xmax, ymax, x_margin, y_margin, npth_size, pth_size, pth_ring, avoid_cu_global, clearance,
                                        pth_to_gnd_drill, min_cu_width, single_lines, differential_lines, single_group_count, diff_group_count,drill_positions):
    data = {
        'func': 'GET_COUPON_DRILL_LINE_RELATIONS',
        'paras': {
                    'xmin': xmin,
                    'ymin': ymin,
                    'xmax': xmax,
                    'ymax': ymax,
                    'x_margin': x_margin,
                    'y_margin': y_margin,
                    'npth_size': npth_size,
                    'pth_size': pth_size,
                    'pth_ring': pth_ring,
                    'avoid_cu_global': avoid_cu_global,
                    'clearance': clearance,
                    'pth_to_gnd_drill': pth_to_gnd_drill,
                    'min_cu_width': min_cu_width,
                    'single_lines': single_lines,
                    'differential_lines': differential_lines,
                    'single_group_count':single_group_count,
                    'diff_group_count':diff_group_count,
                    'drill_positions': drill_positions
                    }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#添加文字
def add_text(job, step, layer, symbol, fontname, text, xsize, ysize, linewidth, location_x, location_y, polarity,
            orient, version, layers, attributes,special_angle=0):
    data = {
        'func': 'ADD_TEXT',
        'paras': [{'job': job},
                  {'step': step},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'fontname': fontname},
                  {'text': text},
                  {'xsize': xsize},
                  {'ysize': ysize},
                  {'linewidth': linewidth},
                  {'location_x': location_x},
                  {'location_y': location_y},
                  {'polarity': polarity},
                  {'orient': orient},
                  {'version': version},
                  {'layers': layers},
                  {'attributes': attributes},
                  {'special_angle':special_angle}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#surface2outline
def surface2outline(job, step, layers, width):
    data = {
            'func': 'SURFACE2OUTLINE',
            'paras': [{'job': job},
                      {'step': step},
                      {'layers': layers},
                      {'width': width}
                      ]
        }
    js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#层别比对
def layer_compare_point(jobname1, stepname1, layername1, jobname2, stepname2, layername2):
    data = {
            'func': 'LAYER_COMPARE_POINT',
            'paras': {
                        'jobname1': jobname1,
                        'stepname1': stepname1,
                        'layername1': layername1,
                        'jobname2': jobname2,
                        'stepname2': stepname2,
                        'layername2': layername2
                      }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#获取选中features的box
def get_selected_features_box(job, step, layers):
    data = {
            'func': 'GET_SELECTED_FEATURES_BOX',
            'paras': {
                        'job': job,
                        'step': step,
                        'layers': layers
                      }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#导出
def layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL=2,numberFormatR=6,
                    zeros=2,unit=0):
    data = {
            'func': 'LAYER_EXPORT',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        'type': _type,
                        'filename': filename,
                        'gdsdbu': gdsdbu,
                        'resize': resize,
                        'angle': angle,
                        'scalingX': scalingX,
                        'scalingY': scalingY,
                        'isReverse': isReverse,
                        'mirror': mirror,
                        'rotate': rotate,
                        'scale': scale,
                        'profiletop': profiletop,
                        'cw': cw,
                        'cutprofile': cutprofile,
                        'mirrorpointX': mirrorpointX,
                        'mirrorpointY': mirrorpointY,
                        'rotatepointX': rotatepointX,
                        'rotatepointY': rotatepointY,
                        'scalepointX': scalepointX,
                        'scalepointY': scalepointY,
                        'mirrordirection': mirrordirection,
                        'cut_polygon': cut_polygon,
                        'numberFormatL': numberFormatL,
                        'numberFormatR': numberFormatR,
                        'zeros': zeros,
                        'unit': unit
                      }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

# def layer_export(job, step, layer, _type, filename):
#     data = {
#             'func': 'LAYER_EXPORT',
#             'paras': {
#                         'job': job,
#                         'step': step,
#                         'layer': layer,
#                         'type': _type,
#                         'filename': filename
#                       }
#             }
#     js = json.dumps(data)
#     print(js)
#     return epcam.process(json.dumps(data))

#获取profile polygon
def get_profile(job, step):
    data = {
            'func': 'GET_PROFILE',
            'paras': {
                        'jobname': job,
                        'stepname': step
                      }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#将一个料号中某一layer的信息拷贝至另一料号中
def copy_layer_features(src_job, src_step, src_layers, dst_job, dst_step, dst_layers, mode, invert):
    data = {
            'func': 'COPY_LAYER_FEATURES',
            'paras': {
                        'src_job': src_job,
                        'src_step': src_step,
                        'src_layer': src_layers,
                        'dst_job': dst_job,
                        'dst_step': dst_step,
                        'dst_layer': dst_layers,
                        'mode': mode,
                        'invert': invert
                      }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#层别比对
def layer_compare(jobname1, stepname1, layername1, jobname2, stepname2, layername2, tolerance, mode, consider_SR,
                    comparison_map_layername, map_layer_resolution):
    data = {
            'func': 'LAYER_COMPARE',
            'paras': {
                        'jobname1': jobname1,
                        'stepname1': stepname1,
                        'layername1': layername1,
                        'jobname2': jobname2,
                        'stepname2': stepname2,
                        'layername2': layername2,
                        'tolerance': tolerance,
                        'global': mode,
                        'consider_SR': consider_SR,
                        'comparison_map_layername': comparison_map_layername,
                        'map_layer_resolution': map_layer_resolution,
                      }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#图形变换
def transform(jobname,stepname,layernames,mode,rotate,scale,mirror_X,mirror_Y,duplicate,datumPoint,angle,xscale,yscale,xoffset,yoffset):
    data = {
            'func': 'TRANSFORM',
            'paras': {
                        'jobname': jobname,
                        'stepname': stepname,
                        'layernames': layernames,
                        'mode': mode,
                        'rotate': rotate,
                        'scale': scale,
                        'mirror_X': mirror_X,
                        'mirror_Y': mirror_Y,
                        'duplicate': duplicate,
                        'datumPoint': datumPoint,
                        'angle': angle,
                        'xscale': xscale,
                        'yscale': yscale,
                        'xoffset': xoffset,
                        'yoffset': yoffset
                     }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#自动定属性
def auto_classify_attribute(job, step, layers):
    data = {
            'func': 'AUTO_CLASSIFY_ATTRIBUTE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layers': layers
                     }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#自动定属性
def outline2surface(job, step, layers, can_to_pad):
    data = {
            'func': 'RESHAPE_OUTLINE_TO_SURFACE',
            'paras': {
                        'jobname': job,
                        'stepname': step,
                        'layernames': layers,
                        'can_to_pad': can_to_pad,
                     }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#获取料号的usersymbol列表
def get_usersymbol_list(job):
    data = {
            'func': 'RESHAPE_OUTLINE_TO_SURFACE',
            'paras': {
                        'jobname': job
                     }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#ok_step_check
def ok_step_check(result):
    data = {
            'func': 'OK_STEP_CHECK',
            'paras': [{
                        'result': result
                     }]
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def silk_screen_check(job, step, layers, erf, spacing, sm_clearance, rout_clearance, smd_clearance, line_width, pad_clearance,
                copper_coverage, hole_clearance, apply_to, use_compensated_rout):
    """
    docstring
    """
    data = {
        'func': 'DRILL_CHECK',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'erf': erf},
                  {'spacing': spacing},
                  {'sm_clearance': sm_clearance},
                  {'rout_clearance': rout_clearance},
                  {'smd_clearance': smd_clearance},
                  {'line_width': line_width},
                  {'pad_clearance': pad_clearance},
                  {'copper_coverage': copper_coverage},
                  {'hole_clearance': hole_clearance},
                  {'apply_to': apply_to},
                  {'use_compensated_rout': use_compensated_rout}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

# #get_step_repeat
# def get_step_repeat(job,step):
#     data = {
#             'func':'GET_STEP_REPEAT',
#             'paras':{
#                 'job':job,
#                 'step':step
#             }
#     }
#     js = json.dumps(data)
#     #print(js)
#     return epcam.process(json.dumps(data))

#get_rest_cu//残铜无孔开窗                      单位nm²
def get_rest_cu(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_REST_CU',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

    #get_rest_cu_with_drill//残铜有孔                     单位nm²
def get_rest_cu_with_drill(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_REST_CU_WITH_DRILL',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_cu_solder_drill//残铜有孔开窗                     单位nm²
def get_cu_solder_drill(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_CU_SOLDER_DRILL',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_rest_cu_solder//残铜无孔开窗                     单位nm²
def get_rest_cu_solder(job,step,layer,resolution_define,thickness):
    data = {
            'func':'GET_REST_CU_SOLDER',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_outlayer_cu//外层残铜有孔开窗                     单位nm²
def get_outlayer_cu(job,step,resolution_define,thickness):
    data = {
            'func':'GET_OUTLAYER_CU',
            'paras':{
                'job':job,
                'step':step,
                'layer':'',
                'or_and':'or',
                'resolution_define':resolution_define,
                'thickness':thickness,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #get_total_square//计算总面积                    单位nm²
def get_total_square(job,step):
    data = {
            'func':'GET_TOTAL_SQUARE',
            'paras':{
                'job':job,
                'step':step,
                'layer':'',
                'or_and':'or',
                'resolution_define':0,
                'thickness':0,
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True
            }
    }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

    #计算选中的feature的面积                     单位nm²
def get_selected_feature_areas(job,step,layer):
    data = {
            'func':'GET_SELECTED_FEATURE_AREAS',
            'paras':{
                'job':job,
                'step':step,
                'layer':layer,
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

    #
def resize_polygon(input_poly,resize_value):
    data = {
            'func':'RESIZE_POLYGON',
            'paras':{
                'input_polygon':input_poly,
                'resize_value':resize_value
            }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def get_sr_coupon_plan(Panel_Height, Panel_Width, x_margin, y_margin, pannel_left, pannel_bottom,pannel_top,pannel_right,job,pcs_step,
panel_step,coupon_x_margin,coupon_y_margin,coupon_to_set_margin,npth_size,pth_size,pth_ring,avoid_cu_global,clearance,pth_to_gnd_drill,min_cu_width,single_lines,differential_lines):
    data = {
            'func': 'GET_SR_COUPON_PLAN',
            'paras': {
                        'Panel_Height': Panel_Height,
                        'Panel_Width': Panel_Width,
                        'x_margin': x_margin,
                        'y_margin': y_margin,
                        'pannel_left': pannel_left,
                        'pannel_bottom': pannel_bottom,
                        'pannel_top': pannel_top,
                        'pannel_right': pannel_right,
                        'job': job,
                        'pcs_step': pcs_step,
                        'panel_step': panel_step,
                        'coupon_x_margin': coupon_x_margin,
                        'coupon_y_margin': coupon_y_margin,
                        'coupon_to_set_margin': coupon_to_set_margin,
                        'npth_size': npth_size,
                        'pth_size': pth_size,
                        'pth_ring': pth_ring,
                        'avoid_cu_global': avoid_cu_global,
                        'clearance': clearance,
                        'pth_to_gnd_drill': pth_to_gnd_drill,
                        'min_cu_width': min_cu_width,
                        'single_lines': single_lines,
                        'differential_lines': differential_lines
                        }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def get_step_repeat(job,step):
    data = {
            'func': 'GET_STEP_REPEAT',
            'paras': {
                        'job': job,
                        'step': step
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def draw_panel_picture(job,step,layer,path):
    data = {
            'func': 'DRAW_PANEL_PICTURE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        'path': path
                        }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def get_all_step_repeat_steps(job,step):
    data = {
            'func': 'GET_ALL_STEP_REPEAT_STEPS',
            'paras': {
                        'job': job,
                        'step': step
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def fill_profile(job,step,layer,profile_resize,child_profile_resize,avoid_drill_size,fill_by_pattern,symbolname,dx,dy,avoid_drill=True):
    data = {
            'func': 'FILL_PROFILE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer':layer,
                        'profile_resize':profile_resize,
                        'child_profile_resize':child_profile_resize,
                        'avoid_drill_size':avoid_drill_size,
                        'fill_by_pattern':fill_by_pattern,  #是否选择自己的symbol填充profile true or false
                        'symbolname':symbolname,            #fill_by_pattern为false，symbolname填空
                        'dx':dx,
                        'dy':dy,
                        'avoid_drill':avoid_drill
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def use_pattern_fill_contours(jobname,stepname,layername,symbolname,dx,dy,break_partial,cut_primitive,origin_point,outline,outlinewidth,outline_invert,odd_offset = 0,even_offset = 0):
    data = {
            'func': 'USE_PATTERN_FILL_CONTOURS',
            'paras': {
                        'jobname': jobname,
                        'stepname': stepname,
                        'layername':layername,
                        'symbolname':symbolname,
                        'dx':dx,
                        'dy':dy,
                        'break_partial':break_partial,
                        'cut_primitive':cut_primitive,
                        'origin_point':origin_point,
                        'outline':outline,
                        'outlinewidth':outlinewidth,
                        'outline_invert':outline_invert,
                        'odd_offset':odd_offset,
                        'even_offset':even_offset
                        }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def SL_panel_banding(job):
    data = {
        'func': 'SL_PANEL_BANDING',
        'paras': {
                    'job': job
                    }
        }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def negative_layer_to_positive(jobname,stepname,layernames):
    data = {
        'func': 'NEGATIVE_LAYER_TO_POSITIVE',
        'paras': {
                'jobname': jobname,
                'stepname': stepname,
                'layernames': layernames
                }
    }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def translate_lines(job,step,layer,op_type,type1,select_edge):
    data = {
        'func': 'TRANSLATE_LINES',
        'paras': {
                'job': job,
                'step': step,
                'layer': layer,
                'op_type': op_type,
                'type': type1,
                'select_edge': select_edge
                }
    }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

def is_selected(job,step,layer):
    data = {
        'func': 'IS_SELECTED',
        'paras': {
                'job': job,
                'step': step,
                'layer': layer
                }
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#contourize
def reshape_contourize(jobname, stepname, layernames, accuracy, separate_to_islands,max_size, clear_mode):
    data = {
        'func': 'RESHAPE_CONTOURIZE',
        'paras': {
                    'jobname': jobname,
                    'stepname': stepname,
                    '_layernames': layernames,
                    'accuracy': accuracy, #mil 0-2.5
                    'separate_to_islands': separate_to_islands,
                    'max_size': max_size,
                    'clear_mode': clear_mode #int 0
                }
    }
    return epcam.process(json.dumps(data))

#Guide map
#sub_kind:sub map 需添加的类型
#panel_kind:panel map 需添加的类型
def run_map(jobname,layername,run_sub,run_panel,sub_kind,panel_kind):
    data = {
        'func': 'RUN_MAP',
        'paras': {
                    'jobname': jobname,
                    'layername': layername,
                    'run_sub': run_sub,
                    'run_panel': run_panel,
                    'sub_kind': sub_kind,
                    'panel_kind': panel_kind
                }
    }
    return epcam.process(json.dumps(data))

def add_sub_jobname_arrow(jobname,step,layername):
    data = {
        'func': 'ADD_SUB_JOBNAME_ARROW',
        'paras': {
                    'jobname': jobname,
                    'layername': layername,
                    'step': step
                }
    }
    return epcam.process(json.dumps(data))

def move_select_feature_to_other_step(jobname,stepname,layername,dest_stepname,delete_org):
    data = {
        'func': 'MOVE_SELECT_FEATURE_TO_OTHER_STEP',
        'paras': {
                    'jobname': jobname,
                    'layername': layername,
                    'stepname': stepname,
                    'dest_stepname':dest_stepname,
                    'delete_org':delete_org
                }
    }
    return epcam.process(json.dumps(data))

def run_edge(job,step,maplayer,is_ol1_top,is_ol2_top,is_smt_top,is_srd_top,is_psa_top,is_laser_top,is_et_top,is_fi_top):
    data = {
        'func': 'RUN_EDGE',
        'paras': {
                    'job': job,
                    'step': step,
                    'maplayer': maplayer,
                    'is_ol1_top':is_ol1_top,
                    'is_ol2_top':is_ol2_top,
                    'is_smt_top':is_smt_top,
                    'is_srd_top':is_srd_top,
                    'is_psa_top':is_psa_top,
                    'is_laser_top':is_laser_top,
                    'is_et_top':is_et_top,
                    'is_fi_top':is_fi_top
                }
    }
    return epcam.process(json.dumps(data))

#拷贝usersymbol至另一个料号
def copy_usersymbol_to_other_job(job1, job2, symbol1, symbol2):
    data = {
            'func': 'COPY_USERSYMBOL_TO_OTHER_JOB',
            'paras': {
                        'job1': job1,
                        'job2': job2,
                        'symbol1':symbol1,
                        'symbol2':symbol2
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#网格铜
	# int dx = 0;//横向骨架线距离
	# int dy = 0;//纵向
	# int linewidth = 0;
	# int x_offset = 0;//第一条线的横向偏移
	# int y_offset = 0;//纵向
	# int angle = 0;//(0-45)
def fill_select_feature_by_grid(job,step,layer,dx,dy,linewidth,x_offset,y_offset,angle):
    data = {
            'func': 'FILL_SELECT_FEATURE_BY_GRID',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer':layer,
                        'dx':dx,
                        'dy': dy,
                        'linewidth': linewidth,
                        'x_offset':x_offset,
                        'y_offset':y_offset,
                        'angle':angle
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def move_selected_features_index(job,step,layers,put_last):
    data = {
            'func': 'MOVE_SELECTED_FEATURES_INDEX',
            'paras': {
                        'jobname': job,
                        'step': step,
                        'layers':layers,
                        'put_last':put_last
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#添加弧
def add_arc(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, center_x, center_y,cw,polarity, dcode, attributes):
    data = {
        'func': 'ADD_ARC',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'layer': layer},
                  {'symbol': symbol},
                  {'start_x': start_x},
                  {'start_y': start_y},
                  {'end_x': end_x},
                  {'end_y': end_y},
                  {'center_x': center_x},
                  {'center_y': center_y},
                  {'cw': cw},
                  {'polarity': polarity},
                  {'dcode': dcode},
                  {'attributes': attributes}]
        }
    js = json.dumps(data)
    #print(js)
    epcam.process(json.dumps(data))

#整体移动目标层的features jobname, stepname, layername, offset_x, offset_y
def move_same_layer(jobname, stepname, layernames, offset_x, offset_y):
    data = {
            'func': 'MOVE_SAME_LAYER',
            'paras': {
                        'jobname': jobname,
                        'stepname': stepname,
                        'layername':layernames,
                        'offset_x':offset_x,
                        'offset_y':offset_y
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#获取step拼板信息
def get_step_header_infos(job, step):
    data = {
            'func': 'GET_STEP_HEADER_INFOS',
            'paras': {
                        'job': job,
                        'step': step
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#分类层中的polygon
def classify_polyline(job,step,layer):
    data = {
            'func': 'CLASSIFY_POLYLINE',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

def sel_polarity(job,step,layers,polarity,sel_type):
    data = {
        'func': 'SEL_POLARITY',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'polarity': polarity},
                  {'sel_type': sel_type}]
    }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

#Prepare分析
def Prepare_check(job, ranges):
    data = {
        'func': 'PREPARE_CHECK',
        'paras': [{'job': job},
                  {'ranges': ranges}]
    }
    #js = json.dumps(data)
    #print(js)
    ret = epcam.process(json.dumps(data))

#根据profile创建outline
    """
    layers:[]
    linewidth: 线宽nm
    """
def profile_to_outerline(job, step, layers, linewidth):
    data = {
        'func': 'PROFILE_TO_OUTERLINE',
        'paras': {'job': job,
                  'step': step,
                  'layernames': layers,
                  'linewidth': linewidth}

        }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))


#防焊分析
def solder_mask_check(job, step, layers, erf, sm_ar, sm_coverage, sm_to_rout, sliver_min, spacing_min, bridge_min, overlap,
                        drill, silver, pads, missing, coverage, spacing, rout, clearance_connection, bridge, apply_to,
                        use_compensated_rout, min_sliver_len, dist2sliver_ratio, apply_range, classify_pad_ar, ranges):
    data = {
        'func': 'SOLDER_MASK_CHECK',
        'paras': [{'job': job},
                  {'step': step},
                  {'layers': layers},
                  {'erf': erf},
                  {'sm_ar': sm_ar},
                  {'sm_coverage': sm_coverage},
                  {'sm_to_rout': sm_to_rout},
                  {'sliver_min': sliver_min},
                  {'spacing_min': spacing_min},
                  {'bridge_min': bridge_min},
                  {'overlap': overlap},
                  {'drill': drill},
                  {'silver': silver},
                  {'pads': pads},
                  {'missing': missing},
                  {'coverage': coverage},
                  {'spacing': spacing},
                  {'rout': rout},
                  {'clearance_connection': clearance_connection},
                  {'bridge': bridge},
                  {'apply_to': apply_to},
                  {'use_compensated_rout': use_compensated_rout},
                  {'min_sliver_len': min_sliver_len},
                  {'dist2sliver_ratio': dist2sliver_ratio},
                  {'apply_range': apply_range},
                  {'classify_pad_ar': classify_pad_ar},
                  {'ranges' : ranges}]
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#select_polyline
    """
    selectpolygon:[{'ix':0,'iy':0}]
    """
def select_polyline(job, step, layer, selectpolygon):
    data = {
        'func': 'SELECT_POLYLINE',
        'paras': {'job': job,
                  'step': step,
                  'layer': layer,
                  'selectpolygon': selectpolygon}
        }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

##flatten_step
def flatten_step(job, step, flatten_layer, dst_layer):
    data = {
        'func': 'FLATTEN_STEP',
        'paras': {'job': job,
                  'step': step,
                  'flatten_layer': flatten_layer,
                  'dst_layer': dst_layer}

        }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

# 钻孔信息
def get_drill_info(job,step,drllayer):
    data = {
        'func': 'GET_DRILL_INFO',
        'paras': {'jobname': job,
                  'stepname': step,
                  'layername': drllayer
                  }

    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#清空撤销堆栈
def clear_all_options(job,step):
    data = {
        'func': 'CLEAR_ALL_OPTIONS',
        'paras': {'job': job,
                  'step': step
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#identify symbol

def identify_symbol(symbolname):
    data = {
        'func': 'IDENTIFY_SYMBOL',
        'paras': {'content': symbolname
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def is_job_open(job):
    data = {
        'func': 'IS_JOB_OPENED',
        'paras': {'jobname': job }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def use_solid_fill_contours(jobname, stepname, layernames, solid_type, min_brush, use_arcs):
    data = {
            "func": "USE_SOLID_FILL_CONTOURS",
            "paras":{
                        "jobname":jobname,
                        "stepname":stepname,
                        "layernames":layernames,
                        "solid_type":solid_type,
                        "min_brush":min_brush,
                        "use_arcs":use_arcs
                        }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

#存储为eps文件
def save_eps(job, path):
    data = {
        'func': 'SAVE_EPS',
        'paras': {
                      'job': job,
                      'path': path
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#导角
def rounding_line_corner(job, step,layers,radius):
    data = {
        'func': 'ROUNDING_LINE_CORNER',
        'paras': {
                      'job': job,
                      'step': step,
                      'layers': layers,
                      'radius': radius
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

def get_rest_cu_rate(job,step,layer,resolution_define,thickness):
    data = {
        'func':'GET_REST_CU_RATE',
        'paras':{
                'job':job,
                'step':step,
                'layer':layer,
                'or_and':'or',
                'holes_slots':True,
                'include_soldermask':True,
                'include_drill':True,
                'resolution_define':resolution_define,
                'thickness':thickness
                }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

#配置config path
def set_config_path(path):
    data = {
        'func': 'SET_CONFIG_PATH',
        'paras': {
                      'path': path
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#获取layer最小线宽线距的信息
def get_quote_price_info(job,step,layer):
    data = {
        'func': 'GET_QUOTE_PRICE_INFO',
        'paras': {
                    'job': job,
                    'step': step,
                    'layer': layer
                }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#制作分孔图
def drillmap_output(job,step,drilllayer,outlinelayer,outputlayer,unit):
    data = {
        'func': 'DRILLMAP_OUTPUT',
        'paras': {
                    'job': job,
                    'step': step,
                    'drilllayer': drilllayer,
                    'outlinelayer': outlinelayer,
                    'outputlayer': outputlayer,
                    'unit': unit
                }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

#获取job内的usersymbol names
def get_special_symbol_names(jobname):
    data = {
        'func': 'GET_SPECIAL_SYMBOL_NAMES',
        'paras': {
                    'jobname': jobname
    }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

def layer_export2(job, step, layer, _type, filename):
    data = {
            'func': 'LAYER_EXPORT',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer,
                        'type': _type,
                        'filename': filename
                      }
            }
    js = json.dumps(data)
    print(js)
    return epcam.process(json.dumps(data))

# 合并铜与轮廓线
def merge_cu_edge_lines(jobname, stepname, layernames):
    data = {
        'func': 'MERGE_CU_EDGE_LINES',
        'paras': {
            'jobname': jobname,
            'stepname': stepname,
            'layernames': layernames
        }
    }
    return epcam.process(json.dumps(data))

# 输出drill
def drill2file(job, step, layer,path,isMetric,number_format_l=2,number_format_r=4,
                    zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, manufacator = '', tools_order = []):
    data = {
        'func': 'DRILL2FILE',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer,
            'path': path,
            'isMetric': isMetric,
            'number_format_l': number_format_l,
            'number_format_r': number_format_r,
            'zeroes': zeroes,
            'unit': unit,
            'tool_unit': tool_unit,
            'x_scale': x_scale,
            'y_scale': y_scale,
            'x_anchor': x_anchor,
            'y_anchor': y_anchor,
            'manufacator': manufacator,
            'tools_order': tools_order
        }
    }
    return epcam.process(json.dumps(data))

#分类层中的net
def classify_layer_net(job,step,layer):
    data = {
            'func': 'CLASSIFY_LAYER_NET',
            'paras': {
                        'job': job,
                        'step': step,
                        'layer': layer
                        }
            }
    js = json.dumps(data)
    #print(js)
    return epcam.process(json.dumps(data))

# 设置钻孔信息
def set_drill_info(job,step,drllayer,vecDrillTools):
    data = {
        'func': 'SET_DRILL_INFO',
        'paras': {'jobname': job,
                  'stepname': step,
                  'layername': drllayer,
                  'vecDrillTools':vecDrillTools
                  }

    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def add_text_by_drill(jobname, stepname, layername, drill_name, textsize, clear_org_features, toolID_to_text):
    data = {
        'func': 'ADD_TEXT_BY_DRILL',
        'paras': {'jobname': jobname,
                  'stepname': stepname,
                  'layername': layername,
                  'drill_name': drill_name,
                  'textsize': textsize,
                  'clear_org_features': clear_org_features,
                  'toolID_to_text':toolID_to_text
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#
def create_table(jobname, stepname, layername, clear_org_features, ix, iy, linewidth, rows):
    data = {
        'func': 'CREATE_TABLE',
        'paras': {'jobname': jobname,
                  'stepname': stepname,
                  'layername': layername,
                  'clear_org_features':clear_org_features,
                  'ix': ix,
                  'iy': iy,
                  'linewidth': linewidth,
                  'rows': rows
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def output_image(job,step,layers,size,xmin,ymin,xmax,ymax,picpath,picname,backcolor,layercolors):
    data = {
        'func': 'OUTPUT_PICTURE',
        'paras': {'job': job,
                  'step': step,
                  'layers':layers,
                  'size':size,
                  'xmin':xmin,
                  'ymin':ymin,
                  'xmax':xmax,
                  'ymax':ymax,
                  'picpath':picpath,
                  'picname':picname,
                  'backcolor':backcolor,
                  'layercolors':layercolors
                  }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def polygon_is_interacts(polygon1,polygon2):
    data = {
        'func': 'POLYGON_IS_INTERACTS',
        'paras': {
                 'polygon1': polygon1,
                 'polygon2': polygon2
                 }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#pad2line
def pad2line(job, step, layers):
    data = {
        'func': 'RESHAPE_PAD_TO_LINE',
        'paras': {
                    'job': job,
                    'step': step,
                    'layers': layers
                      }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))
    return epcam.process(js)

def auto_move_drill_pad(job,step, move_sm_via, laser_min_ring, via_pad_min_ring, line_conpensation, \
    smd_conpensation, bga_conpensation, other_conpensation, np2laser, rout2laser, np2via, rout2via, pth2via, \
        pth2laser, via2laser, via2via, laser2laser, consider_net, include_all, drill2signalP, drill2signalS, \
            user_classify_same_net_drill, same_net_via2laser, same_net_via2via, same_net_laser2laser, vcut2laser, \
                vcut2via):
    data = {
        'func': 'AUTO_MOVE_DRILL_PAD',
        'paras': {
                 'job': job,
                 'step': step,
                 'move_sm_via': move_sm_via,
                 'laser_min_ring': laser_min_ring,
                 'via_pad_min_ring': via_pad_min_ring,
                 'line_conpensation': line_conpensation,
                 'smd_conpensation': smd_conpensation,
                 'bga_conpensation': bga_conpensation,
                 'other_conpensation': other_conpensation,
                 'np2laser': np2laser,
                 'rout2laser': rout2laser,
                 'np2via': np2via,
                 'rout2via': rout2via,
                 'pth2via': pth2via,
                 'pth2laser': pth2laser,
                 'via2laser': via2laser,
                 'via2via': via2via,
                 'laser2laser': laser2laser,
                 'consider_net': consider_net,
                 'include_all': include_all,
                 'drill2signalP': drill2signalP,
                 'drill2signalS': drill2signalS,
                 'user_classify_same_net_drill': user_classify_same_net_drill,
                 'same_net_via2laser': same_net_via2laser,
                 'same_net_via2via': same_net_via2via,
                 'same_net_laser2laser': same_net_laser2laser,
                 'vcut2laser': vcut2laser,
                 'vcut2via': vcut2via
                 }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

def teardrop_attribute_classify(jobname, stepname, layernames, line_arc, pad, surface, max_td_length, \
trace_pad_trace_connection_tol, delete_previous_attribute):
    data = {
        'func': 'TEARDROP_ATTRIBUTE_CLASSIFY',
        'paras': {
                 'jobname': jobname,
                 'stepname': stepname,
                 'layernames': layernames,
                 'line_arc': line_arc,
                 'pad': pad,
                 'surface': surface,
                 'max_td_length': max_td_length,
                 'trace_pad_trace_connection_tol': trace_pad_trace_connection_tol,
                 'delete_previous_attribute': delete_previous_attribute
                 }
    }
    js = json.dumps(data)
    # print(js)
    return epcam.process(js)

#获取旋转角度pad信息
def get_feature_rotated_box(job, step, layer, featureID):
    data = {
        'func': 'GET_FEATURE_ROTATED_BOX',
        'paras': {
                      'job': job,
                      'step': step,
                      'layer': layer,
                      'featureID': featureID
                      }
    }
    return epcam.process(json.dumps(data))

# 输出rout
def rout2file(job, step, layer,path,number_format_l=2,number_format_r=4,
                    zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, partial_order = 0
                    , num_in_x = 0, num_in_y = 0, order_type = 0, serial_no = 0, break_arcs = False):
    data = {
        'func': 'ROUT2FILE',
        'paras': {
            'job': job,
            'step': step,
            'layer': layer,
            'path': path,
            'number_format_l': number_format_l,
            'number_format_r': number_format_r,
            'zeroes': zeroes,
            'unit': unit,
            'tool_unit': tool_unit,
            'x_scale': x_scale,
            'y_scale': y_scale,
            'x_anchor': x_anchor,
            'y_anchor': y_anchor,
            'partial_order': partial_order,
            'num_in_x': num_in_x,
            'num_in_y': num_in_y,
            'order_type': order_type,
            'serial_no': serial_no,
            'break_arcs': break_arcs
        }
    }
    return epcam.process(json.dumps(data))

# 多步操作绑定
def bind_editop_count(job, step, count):
    data = {
        'func': 'BIND_EDITOP_COUNT',
        'paras': {
            'job': job,
            'step': step,
            'count': count
        }
    }
    return epcam.process(json.dumps(data))

# 获取op数量
def get_editop_count(job, step):
    data = {
        'func': 'GET_EDITOP_COUNT',
        'paras': {
            'job': job,
            'step': step
        }
    }
    return epcam.process(json.dumps(data))

#制作分孔图
def create_drill_map_by_info(job,step,drilllayer,outlinelayer,outputlayer,unit,vecDrillTools):
    data = {
        'func': 'CREATE_DRILL_MAP_BY_INFO',
        'paras': {
                    'job': job,
                    'step': step,
                    'drilllayer': drilllayer,
                    'outlinelayer': outlinelayer,
                    'outputlayer': outputlayer,
                    'unit': unit,
                    'vecDrillTools': vecDrillTools
                }
    }
    #print(json.dumps(data))
    return epcam.process(json.dumps(data))

