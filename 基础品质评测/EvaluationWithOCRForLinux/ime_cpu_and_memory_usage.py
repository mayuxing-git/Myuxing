import psutil
from keys import do, ctrl, shift
from config import INPUT, PARAMS
import time
import os
import inspect
import ctypes

ime_pid = None
fcitx_pid = None
ime_name = INPUT


def get_all_ime_pid(proc):
    pids = psutil.pids()
    pid = list()
    for p in pids:
        try:
            p_name = psutil.Process(p)
            if ime_name == 'xunfei':
                if p_name.name().lower().startswith(proc):
                    print(p_name.pid, p_name.name())
                    pid.append(p)
            else:
                if p_name.name() == proc:
                    print(p_name.pid, p_name.name())
                    pid.append(p)
        except:
            pass
    return pid


def get_ime_pid(ime_name):
    pid = []
    if ime_name == 'sogou':
        pid = get_all_ime_pid('sogouImeService')
    elif ime_name == 'xunfei':
        pid = get_all_ime_pid('ifly')
    fcitx = get_all_ime_pid('fcitx')
    return pid, fcitx


def get_process_by_pid(pids):
    proc_list = []
    for i in range(len(pids)):
        try:
            proc = psutil.Process(pids[i])
            proc_list.append(proc)
        except psutil.NoSuchProcess:
            pass
    return proc_list


def init_get_cpu_usage(proc_list):
    try:
        for i in range(len(proc_list)):
            proc_list[i].cpu_percent()
    except psutil.NoSuchProcess:
        pass


def get_cpu_and_memory_usage_by_process(proc_list):
    cpu_total_usage = 0
    memory_total_usage = 0
    for i in range(len(proc_list)):
        cpu_total_usage += proc_list[i].cpu_percent()
        memory_total_usage += proc_list[i].memory_full_info().uss
    print('[Error  ] <> Repository got deleted while a highli is cpu_total_usage: ' + str(cpu_total_usage))
    return cpu_total_usage, memory_total_usage


def get_cpu_and_memory_usage(cpu_usage, memory_usage):
    global ime_pid, fcitx_pid
    ime_pid, fcitx_pid = get_ime_pid(ime_name)
    ime_proc_list = get_process_by_pid(ime_pid)
    fcitx_proc_list = get_process_by_pid(fcitx_pid)
    init_get_cpu_usage(ime_proc_list)
    init_get_cpu_usage(fcitx_proc_list)
    while True:
        try:
            time.sleep(5)
            cpu_total_usage, memory_total_usage = get_cpu_and_memory_usage_by_process(ime_proc_list)
            cpu_usage.setdefault('ime_cpu_usage', []).append(cpu_total_usage)
            memory_usage.setdefault('ime_memory_usage', []).append(memory_total_usage)
            cpu_total_usage, memory_total_usage = get_cpu_and_memory_usage_by_process(fcitx_proc_list)
            cpu_usage.setdefault('fcitx_cpu_usage', []).append(cpu_total_usage)
            memory_usage.setdefault('fcitx_memory_usage', []).append(memory_total_usage)
            # cpu_usage.append(cpu_total_usage)
            # memory_usage.append(memory_total_usage)
        except:
            time.sleep(10)
            ime_pid, fcitx = get_ime_pid(ime_name)
            ime_proc_list = get_process_by_pid(ime_pid)
            fcitx_proc_list = get_process_by_pid(fcitx_pid)
            init_get_cpu_usage(ime_proc_list)
            init_get_cpu_usage(fcitx_proc_list)
            pass


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

