from cc.cc_method import GetTestData,DMS,Print,getFlist
import pytest
from config_ep.epcam import job_operation,epcam_api
from config_ep.epcam_cc_method_no_django import EpGerberToODB,Information
from config_g.g_cc_method_no_django import Asw
from config import RunConfig
from pathlib import Path

asw = Asw(r"C:\EPSemicon\cc\gateway.exe")#拿到G软件
