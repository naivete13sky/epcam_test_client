from os.path import dirname, abspath
import sys

sys.path.append(r'C:\cc\python\epwork\dms\job_manage\epcam')

base_path = dirname(dirname(abspath(__file__)))
sys.path.insert(0, base_path)
from config_g.g_cc_method_no_django import Asw

asw = Asw(r"C:\EPSemicon\cc\gateway.exe")#拿到G软件


