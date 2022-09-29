from cc_method import DMS

job_id = 2015


cc=DMS().get_data_from_dms_db_pandas(job_id)
# print(cc)


cc=DMS().get_data_from_dms_db_pandas(job_id,field='file_compressed')
print(cc)
