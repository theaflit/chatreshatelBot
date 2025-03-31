import os


def check_path(path_name):
    """Проверка существования папки"""
    if not os.path.exists(path_name):
        os.makedirs(path_name)
