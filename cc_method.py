import os
import pandas as pd
import urllib
import time
import psycopg2
import rarfile
from sqlalchemy import create_engine
import pandas as pd

class GetTestData():
    pass
    def get_job_id(self,fun):
        pd_1=pd.read_excel(io=os.path.join(os.getcwd(),r"config.xlsx"),sheet_name="test_data")
        return [ each2 for each1 in pd_1[(pd_1["测试功能"]==fun) & (pd_1["是否执行"] == 1)][['测试料号']].values.tolist() for each2 in each1]


class DMS():
    pass

    # 下载文件
    def file_downloand(self,need_file_path, save_path):  #######文件下载
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
                filename = os.path.join(file_path, os.path.basename(need_file_path))
                urllib.request.urlretrieve(file_url, filename=filename)
                print("成功下载文件")
            except IOError as exception_first:  # 设置抛出异常
                print(1, exception_first)

            except Exception as exception_second:  # 设置抛出异常
                print(2, exception_second)
        else:
            print("文件已经存在！")

    def get_data_from_dms_db_sql(self,sql):
        pass
        conn = psycopg2.connect(database="dms", user="readonly", password="123456", host="10.97.80.147", port="5432")
        cursor = conn.cursor()
        sql = sql
        print('sql:', sql)
        cursor.execute(sql)
        conn.commit()
        ans = cursor.fetchall()
        conn.close()
        return ans

    def get_data_from_dms_db_pandas(self, job_id,*args, **kw):
        sql = '''SELECT a.* from job a
                where a.id = {}
                '''.format(job_id)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.147/dms')
        pd_job_current = pd.read_sql(sql=sql, con=engine).loc[0]
        if 'field' in kw:
            return pd_job_current[kw['field']]
        else:
            return pd_job_current


    def get_file_compressed_from_dms_db(self,need_file_path, save_path,decompress_bool):
        pass
        self.file_downloand(need_file_path, save_path)
        if decompress_bool == True:
            pass
            # time.sleep(0.1)
            # file_compressed_file_path = os.listdir(temp_gerber_path)[0]
            # print("file_compressed_file_path:", file_compressed_file_path)
            # temp_compressed = os.path.join(temp_gerber_path, file_gerber_name)
            # rf = rarfile.RarFile(temp_compressed)
            # rf.extractall(temp_gerber_path)
            # # 删除gerber压缩包
            # if os.path.exists(temp_compressed):
            #     os.remove(temp_compressed)


if __name__ == "__main__":
    print("我是main()")
    cc=GetTestData().get_job_id('Input')
    print(cc)
