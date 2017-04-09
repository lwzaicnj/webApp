#coding:utf-8

__author__ = 'Eric Lee'

import os, sys, time, subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def logs(s):
    print ('[Monitor] %s' % s)

class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            logs('Python source file change: %s' % event.src_path)
            self.restart()

command = ['echo', ' ok'] # 执行命令
process = None

def kill_process():
    global process
    if process:
        logs('Kill process [%s]' % process) # id???
        process.kill()
        process.wait()
        logs('Process ended with code %s.' % process.returncode)
        process = None

def start_process():
    global process, command
    logs('Start process %s...' % ' '.join(command))
    # 设定标准输入输出和标准错误
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def restart_process():
    kill_process()
    start_process()

def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHander(restart_process), path, recursive=True)
    observer.start()
    logs('Watching directory %s...' % path )
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    argv = sys.argv[1:] # 跟着本脚本名后的参数
    if not argv:
        print('Usage:./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python':
        argv.insert(0, 'python') # ['python', 'app.py']
    command = argv
    path = os.path.abspath('.') #当前目录
    start_watch(path, None)










