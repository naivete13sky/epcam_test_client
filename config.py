

class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    cases_path = "./test_dir/"

    # 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)。
    # driver_type = "chrome"

    driver_type = "epcam"

    # ep_cam_path=r'C:\cc\ep_local\product\EP-CAM\version\20220920\EP-CAM_beta_2.28.054_s37_jiami\Release'
    # ep_cam_path=r'C:\cc\ep_local\product\EP-CAM\version\20220920\EP-CAM_beta_2.28.054_s38_jiami\Release'
    ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20220921\EP-CAM_beta_2.28.054_s39_jiami\Release'

    epcam_python_path=r'C:\EPSemicon\cc\epcam'

    # 配置运行的 URL
    url = "http://www.epsemicon.com/"

    # 失败重跑次数
    rerun = "0"

    # 当达到最大失败数，停止执行
    max_fail = "300"

    # 浏览器驱动（不需要修改）
    driver = None

    # 报告路径（不需要修改）
    NEW_REPORT = None
