#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""The script to start or stop the es cluster.
author: icefiva
version: 0.0.1
content: adapt to es 2.x and run on root

version: 0.0.2
updated: accept passed a user parameter to start or stop the es cluster.(python2)
updated date: 20180702
"""

import os
import sys
#import imp ---python3
import time
import paramiko

#imp.reload(sys)
reload(sys)
sys.setdefaultencoding('utf-8')

def start_es(es_nodes_cfg):
    with (open(es_nodes_cfg,'r')) as f:
        for line in f.readlines():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(line,22,'elastic5','elastic5')
            try:
                stdin, stdout, stderr = ssh.exec_command('(source /etc/profile;cd /opt/elasticsearch-5.6.10;bin/elasticsearch -d)')
            except  SSHException as e:
                print('exec_command has proble, raise exception: ' + '\n' + e)
                sys.exit(1)

            time.sleep(5)
            try:
                stdin, stdout, stderr = ssh.exec_command('jps')
            except SSHException as e:
                print('exec_command has proble, raise exception: ' + '\n' + e)
                sys.exit(1)
            jpsout = stdout.read().rstrip('\n')
            for jps_row in jpsout.split('\n'):
                if line.find('Elasticsearch'): print('node ' + line + ' success start the es.')
            ssh.close()
            #print(line)
    f.close()

def stop_es(es_nodes_cfg):

    with (open(es_nodes_cfg,'r')) as f:
        for line in f.readlines():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(line,22,'elastic5','elastic5')
            try:
                stdin, stdout, stderr = ssh.exec_command('source /etc/profile;jps')
            except  SSHException as e:
                print('exec_command has proble, raise exception: ' + '\n' + e)
                sys.exit(1)

            jpsout = stdout.read().rstrip('\n')
            for jps_row in jpsout.split("\n"):
                id_and_name = jps_row.split(' ')
                if len(id_and_name) > 1:
                    if id_and_name[1] == 'Elasticsearch':
                        print('ready to kill ' + id_and_name[1] +'\n' + 'id is: ' + id_and_name[0])
                        try:
                            killstr = "kill -9 " + id_and_name[0]
                            stdin, stdout, stderr = ssh.exec_command(killstr)
                        except SSHException as e:
                            print('exec_command has proble, raise exception: ' + '\n' + e)
                            sys.exit(1)
            print('success to kill node ' + line.rstrip('\n') + '\'s es.')
            time.sleep(5)
            ssh.close()
    f.close()


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print('Usage:python es_kibanba_start_stop_useradapt.py <config_ip_file> <start or stop>')
        sys.exit(1)

    es_nodes_cfg = sys.argv[1]
    tasktype = sys.argv[2]
    if tasktype == "start":
        start_es(es_nodes_cfg)
    elif tasktype == "stop":
        stop_es(es_nodes_cfg)
    else:
        print("unknow tasktype!")
        sys.exit(1)