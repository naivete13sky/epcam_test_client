import json
import os,sys
import urllib  # 导入urllib库
import urllib.request
import time
import psycopg2
import rarfile
from sqlalchemy import create_engine
import pandas as pd
from config import RunConfig
print(os.path.dirname("__file__"))
sys.path.append(RunConfig.epcam_python_interface_path)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_path)
sys.path.insert(0, os.path.join(base_path,r'config_ep/epcam'))
from config_ep.epcam import epcam,job_operation,epcam_api

class GetTestData():
    pass
    def get_job_id(self,fun):
        pd_1=pd.read_excel(io=os.path.join(os.path.abspath('.'),r"config.xlsx"), sheet_name="test_data")
        return [ each2 for each1 in pd_1[(pd_1["测试功能"]==fun) & (pd_1["是否执行"] == 1)][['测试料号']].values.tolist() for each2 in each1]


class DMS():
    pass

    # 下载文件
    def file_downloand(self,need_file_path, save_path):  #######文件下载
        if os.path.exists(need_file_path) == False:  # 判断是否存在文件

            # 文件url
            file_url = 'http://10.97.80.119/media/files/{}'.format(os.path.basename(need_file_path))

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

    def get_job_fields_from_dms_db_sql(self,sql):
        pass
        conn = psycopg2.connect(database="dms", user="readonly", password="123456", host="10.97.80.119", port="5432")
        cursor = conn.cursor()
        sql = sql
        print('sql:', sql)
        cursor.execute(sql)
        conn.commit()
        ans = cursor.fetchall()
        conn.close()
        return ans

    def get_job_fields_from_dms_db_pandas(self, job_id,*args, **kwargs):
        sql = '''SELECT a.* from job a
                where a.id = {}
                '''.format(job_id)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/dms')
        pd_job_current = pd.read_sql(sql=sql, con=engine).loc[0]
        if 'field' in kwargs:
            return pd_job_current[kwargs['field']]
        else:
            return pd_job_current

    def get_job_layer_fields_from_dms_db_pandas(self, job_id,*args, **kwargs):
        sql = '''SELECT a.* from layer a
            where a.job_id = {}
                '''.format(job_id)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/dms')
        pd_job_current_layers = pd.read_sql(sql=sql, con=engine)
        if 'field' in kwargs:
            return pd_job_current_layers[kwargs['field']]
        else:
            return pd_job_current_layers

    def get_job_layer_fields_from_dms_db_pandas_one_layer(self, job_id,*args, **kwargs):
        layer=kwargs['filter']
        sql = '''SELECT a.* from layer a
            where a.job_id = {} and lower(a.layer)='{}'
                '''.format(job_id,layer)
        # print("sql:",sql)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/dms')
        pd_job_current_layer = pd.read_sql(sql=sql, con=engine)
        return pd_job_current_layer

    def get_job_layer_drill_from_dms_db_pandas_one_job(self, job_id,*args, **kwargs):

        sql = '''SELECT a.* from layer a
            where a.job_id = {} and a.status = 'published' and a.layer_file_type = 'excellon2'
                '''.format(job_id)
        # print("sql:",sql)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/dms')
        pd_job_current_layer_drill = pd.read_sql(sql=sql, con=engine)
        return pd_job_current_layer_drill

    def get_file_from_dms_db(self,temp_path,job_id,*args, **kwargs):
        job_current_all_fields = self.get_job_fields_from_dms_db_pandas(job_id)
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        #判断是要下载哪个类型的文件
        if 'field' in kwargs:
            print('field:',kwargs['field'])
            #如果下载的是整理过的gerber压缩包
            if kwargs['field'] == 'file_compressed':
                temp_gerber_path = os.path.join(temp_path, 'gerber')
                if not os.path.exists(temp_gerber_path):
                    os.mkdir(temp_gerber_path)
                temp_ep_path = os.path.join(temp_path, 'ep')
                if not os.path.exists(temp_ep_path):
                    os.mkdir(temp_ep_path)
                file_gerber_name = job_current_all_fields['file_compressed'].split("/")[1]

                # 下载并解压原始gerber文件
                if not os.path.exists(os.path.join(temp_gerber_path, file_gerber_name)):
                    print("not have")
                    self.file_downloand(os.path.join(temp_gerber_path, file_gerber_name), temp_gerber_path)

                if 'decompress' in kwargs:
                    print('decompress',kwargs['decompress'])
                    time.sleep(0.1)
                    file_compressed_file_path = os.listdir(temp_gerber_path)[0]
                    print("file_compressed_file_path:", file_compressed_file_path)
                    temp_compressed = os.path.join(temp_gerber_path, file_gerber_name)
                    rf = rarfile.RarFile(temp_compressed)
                    rf.extractall(temp_gerber_path)
                    # 删除gerber压缩包
                    if os.path.exists(temp_compressed):
                        os.remove(temp_compressed)

            # 如果下载的是G转图的tgz
            if kwargs['field'] == 'file_odb_g':
                temp_g_path = os.path.join(temp_path, 'g')
                if not os.path.exists(temp_g_path):
                    os.mkdir(temp_g_path)
                file_odb_g_name = job_current_all_fields['file_odb_g'].split("/")[1]

                # 下载并解压原始gerber文件
                if not os.path.exists(os.path.join(temp_g_path, file_odb_g_name)):
                    print("not have")
                    self.file_downloand(os.path.join(temp_g_path, file_odb_g_name), temp_g_path)

                if 'decompress' in kwargs:
                    print('decompress', kwargs['decompress'])
                    time.sleep(0.1)
                    g_tgz_file = os.listdir(temp_g_path)[0]
                    print("g_tgz_file:", g_tgz_file)
                    job_operation.untgz(os.path.join(temp_g_path, os.listdir(temp_g_path)[0]), temp_g_path)
                    if os.path.exists(os.path.join(temp_g_path, g_tgz_file)):
                        os.remove(os.path.join(temp_g_path, g_tgz_file))

    def get_job_layer_rout_from_dms_db_pandas_one_job(self, job_id,*args, **kwargs):

        sql = '''SELECT a.* from layer a
            where a.job_id = {} and a.status = 'published' and a.layer_file_type = 'excellon2' and a.layer_type = 'rout'
                '''.format(job_id)
        # print("sql:",sql)
        engine = create_engine('postgresql+psycopg2://readonly:123456@10.97.80.119/dms')
        pd_job_current_layer_rout = pd.read_sql(sql=sql, con=engine)
        return pd_job_current_layer_rout



class Print():
    @staticmethod
    def print_with_delimiter(text, sign='*', numbers=198):
        pass
        print(str(sign) * int((numbers - len(text)) / 2), text, str(sign) * int((numbers - len(text)) / 2))


def get_data(file_path):
    """
    读取参数化文件
    :param file_path:
    :return:
    """
    data = []
    with(open(file_path, "r")) as f:
        dict_data = json.loads(f.read())
        for i in dict_data:
            data.append(tuple(i.values()))
    return data


def getFlist(path):
    for root, dirs, files in os.walk(path):
        print('root_dir:', root)  #当前路径
        print('sub_dirs:', dirs)   #子文件夹
        print('files:', files)     #文件名称，返回list类型
    return files



#存储为json文件的方法
def else1():
    pass
    all_result_g = {"layer1":"正常","layer2":"错误"}
    #结果存入josn文件，如果有需要的话
    if os.path.exists(r'result.json'):
        os.remove(r'result.json')
    with open(r'result.json', 'w') as f:
        json.dump(all_result_g, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print("我是main()")
    job_id = 2182
    layer_drill = DMS().get_job_layer_drill_from_dms_db_pandas_one_job(job_id)
    print('*' * 50, '\n', "layer_drill:", layer_drill)
    print([each.lower() for each in DMS().get_job_layer_drill_from_dms_db_pandas_one_job(job_id)['layer'] ])

