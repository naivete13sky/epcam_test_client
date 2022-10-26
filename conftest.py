import os,sys
from py.xml import html
from config import RunConfig
sys.path.append(RunConfig.epcam_python_interface_path)
import pytest
from os.path import dirname, abspath
import epcam_api
base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from config_g.g_cc_method import Asw



# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/test_report/"


# 定义基本测试环境
@pytest.fixture(scope='function')
def base_url():
    return RunConfig.url

# 设置用例描述表头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()

# 设置用例描述表格
def pytest_html_results_table_row(report, cells):
    pass
    cells.insert(2, html.td(report.description))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"
            else:
                case_name = case_path
            capture_screenshots(case_name)
            img_path = "image/" + case_name.split("/")[-1]
            if img_path:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html

def capture_screenshots(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        pass
        # raise NameError('没有初始化测试报告目录')
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        # RunConfig.driver.save_screenshot(image_dir)

# 加载epcam
@pytest.fixture(scope='session', autouse=True)
def epcam():
    """
    全局定义epcam驱动
    :return:
    """
    global driver

    if RunConfig.driver_type == "epcam":
        import epcam
        epcam.init()
        epcam_api.set_config_path(RunConfig.ep_cam_path)
        driver = None

    else:
        raise NameError("driver驱动类型定义错误！")

    RunConfig.driver = driver

    return driver

@pytest.fixture(scope='function', autouse=False)
def prepare_test_job_clean_g():
    pass
    # 删除所有料号
    # asw = Asw(r"C:\EPSemicon\cc\gateway.exe")
    asw = Asw(RunConfig.gateway_path)
    asw.clean_g_all_pre_get_job_list(r'//vmware-host/Shared Folders/share/job_list.txt')
    asw.clean_g_all_do_clean(r'C:\cc\share\job_list.txt')

    #yield前是前置操作
    yield




if __name__ == "__main__":
    capture_screenshots("test_dir/test_baidu_search.test_search_python.png")
