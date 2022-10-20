import os, sys, datetime
import logging

log_dir = '{}/log'.format(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

cur_time = datetime.datetime.now()
cur_time_str = datetime.datetime.strftime(cur_time, '%Y-%m-%d %H_%M_%S')

log_path = os.path.join(log_dir, cur_time_str + '.log')
format_str1 = logging.Formatter('%(levelname)s: %(message)s')
format_str2 = logging.Formatter(fmt='%(asctime)s - %(pathname)s[line: %(lineno)d] - %(levelname)s: %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format_str1)
file_handler = logging.FileHandler(log_path, mode='a+')
file_handler.setFormatter(format_str2)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)