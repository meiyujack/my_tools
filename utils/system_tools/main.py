from . import os, ctypes


def walk_file(path):
    """得到路径下所有文件访问地址
    :param path: 访问路径
    :return: 列表形式，包含所有文件的访问地址
    """
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            result.append(os.path.join(root, file))
    return result


def get_available_space(driver_letter):
    """
    获取磁盘剩余空间
    :param driver_letter: 磁盘盘符
    :return: 剩余空间，单位G
    """
    target_driver = driver_letter + ":"
    if os.path.exists(target_driver):
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(target_driver), None, None,
                                                   ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 / 1024


