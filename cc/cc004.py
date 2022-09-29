import time
from config import RunConfig
from cc_method import DMS

job_id = 2015
vs_time_g = str(int(time.time()))#比对时间
temp_path = RunConfig.temp_path_base + "_" + str(job_id) + "_" + vs_time_g

cc=DMS().get_job_fields_from_dms_db_pandas(job_id)
# print(cc)


cc=DMS().get_job_fields_from_dms_db_pandas(job_id,field='file_compressed')
# print(cc)



cc2=DMS().get_file_from_dms_db(temp_path,2015,field='file_compressed',decompress='rar')
print(cc2)