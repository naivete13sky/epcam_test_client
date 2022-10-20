import time,os
from config import RunConfig
from cc.cc_method import DMS

job_id = 2015
vs_time_g = str(int(time.time()))#比对时间
temp_path = RunConfig.temp_path_base + "_" + str(job_id) + "_" + vs_time_g

# cc=DMS().get_job_fields_from_dms_db_pandas(job_id)
# print(cc)


# cc=DMS().get_job_fields_from_dms_db_pandas(job_id,field='file_compressed')
# print(cc)



# cc2=DMS().get_file_from_dms_db(temp_path,2015,field='file_compressed',decompress='rar')
# print(cc2)


# cc3=DMS().get_job_layer_fields_from_dms_db_pandas(job_id,field='layer_org')
# print(cc3)


# layer_all = DMS().get_job_layer_fields_from_dms_db_pandas(job_id, field='layer')
# print("layer_all", layer_all)

path=r"C:\cc\share\temp_2015_1665218506\output_gerber\eol04204_ep\orig\0420440e.bot"
layer_e2=DMS().get_job_layer_fields_from_dms_db_pandas_one_layer(job_id,filter=os.path.basename(path).replace(' ', '-').replace('(', '-').replace(')', '-'))
print('*'*50,'\n',"layer_e2:",layer_e2)
print("*"*50,'\n','layer_e2.status:',layer_e2.status.values[0],'layer_e2.layer_file_type:',layer_e2.layer_file_type.values[0])
