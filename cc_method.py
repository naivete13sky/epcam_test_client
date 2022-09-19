import os
import pandas as pd
import urllib


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


if __name__ == "__main__":
    print("我是main()")
    cc=GetTestData().get_job_id('Input')
    print(cc)