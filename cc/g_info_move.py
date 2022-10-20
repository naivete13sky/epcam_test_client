import cc_method
from cc_method import GetTestData, DMS, Print
import pytest
from os.path import dirname, abspath
import os, sys, time, json, shutil

sys.path.append(r'C:\cc\python\epwork\dms\job_manage\epcam')
import job_operation, epcam_api

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from g_cc_method_no_django import Asw
from epcam_cc_method_no_django import EpGerberToODB, Information
import urllib  # 导入urllib库
import urllib.request
from config import RunConfig
from pathlib import Path

asw = Asw(r"C:\EPSemicon\cc\gateway.exe")#拿到G软件


