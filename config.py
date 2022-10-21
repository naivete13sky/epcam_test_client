

class RunConfig:
    """
    运行测试配置
    """


    #配置EPCAM路径，只要换了版本就要更改
    ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20221017\EP-CAM_beta_2.29.055_s15_jiami\Release'

    # ep_cam_path=r'C:\cc\ep_local\product\EP-CAM\version\20220920\EP-CAM_beta_2.28.054_s37_jiami\Release'
    # ep_cam_path=r'C:\cc\ep_local\product\EP-CAM\version\20220920\EP-CAM_beta_2.28.054_s38_jiami\Release'
    # ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20220921\EP-CAM_beta_2.28.054_s39_jiami\Release'
    # ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20220922\EP-CAM_beta_2.28.054_s43_jiami\Release'
    # ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20220928\EP-CAM_beta_2.29.055_s1_u3_jiami\Release'
    # ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20220930\EP-CAM_beta_2.29.055_s6_jiami\Release'
    # ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20221010\EP-CAM_beta_2.29.055_s13_jiami\Release'
    # ep_cam_path = r'C:\cc\ep_local\product\EP-CAM\version\20221013\EP-CAM_beta_2.29.055_s14_test_jiami\Release'






    # 运行测试用例的目录或文件
    cases_path = "./test_dir/"

    # 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)。
    # driver_type = "chrome"

    # EPCAM驱动类型
    driver_type = "epcam"

    #悦谱python接口目录
    epcam_python_interface_path = r'config_ep/epcam'


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

    # 当前执行电脑的临时目录
    temp_path_base = r'C:\cc\share\temp'

    # 悦谱出gerber的配置默认參數
    config_ep_output = r'config_ep\outcfg.json'

    # 调用G的管道
    gateway_path = r'config_g\bin\gateway.exe'
