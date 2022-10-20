from cc.cc_method import GetTestData,DMS,Print,getFlist
import pytest
from config_ep.epcam import job_operation,epcam_api
from config_ep.epcam_cc_method_no_django import EpGerberToODB,Information
from config_g.g_cc_method_no_django import Asw
from config import RunConfig
from pathlib import Path

asw = Asw(r"C:\EPSemicon\cc\gateway.exe")#拿到G软件

temp_path_local_g_info_folder=r'C:\cc\share\temp_2201_1666251331\info'
temp_path_remote_g_info_folder = r'\\vmware-host\Shared Folders\share\temp_2201_1666251331\info'
job_1 = 'a202_g1'
step_1 = 'orig'
layer_1 = 'drl001.drl'

job_2 = 'a202-main-v03_g2'
step_2 = 'orig'
layer_2 = 'drl001.drl'

cc_1=asw.get_info_layer_features_first_coor(job=job_1,step=step_1,layer=layer_1,
    temp_path_local_g_info_folder=temp_path_local_g_info_folder,temp_path_remote_g_info_folder=temp_path_remote_g_info_folder)
print(cc_1)

cc_2=asw.get_info_layer_features_first_coor(job=job_2,step=step_2,layer=layer_2,
    temp_path_local_g_info_folder=temp_path_local_g_info_folder,temp_path_remote_g_info_folder=temp_path_remote_g_info_folder)
print(cc_2)

x1 = float(cc_1[0])
y1 = float(cc_1[1])
print(x1,y1)


x2 = float(cc_2[0])
y2 = float(cc_2[1])
print(x2,y2)

dx = x2 - x1
dy = y2 - y1

print("dx:",dx,"dy:",dy)


asw.move_one_layer_by_x_y()
