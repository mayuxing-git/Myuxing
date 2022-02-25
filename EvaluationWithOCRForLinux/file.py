#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 20:27:13 2017

@author: wufangyu
"""
import os
import logging

logger = logging.getLogger(__name__)
img_suffix_name = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.cr2', '.tif', '.bmp', '.jxr', '.psd', '.ico']
video_suffix_name = ['.mp4', '.m4v', '.mkv', '.webm', '.mov', '.avi', '.wmv', '.mpg', '.flv']


def is_img_file(file_path):
    file_path = file_path.lower()
    return os.path.splitext(file_path)[1] in img_suffix_name


def is_video_file(file_path):
    file_path = file_path.lower()
    return os.path.splitext(file_path)[1] in video_suffix_name


def mkdir(path):
    # Remove the first space
    path = path.strip()
    # Remove the trailing slash
    path = path.rstrip("\\")
    path = path.rstrip("/")

    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        logger.debug("path : %s created successfully" % path)


def delete_file(path):
    try:
        os.remove(path)
        logger.debug("File deleted: %s" % path)
    except:
        logger.error("Failed to delete file: %s" % path)
        pass
    return


def clear_dir(path):
    logger.debug("start clear: %s" % path)
    for item in os.listdir(path):
        temp_path = os.path.join(path, item)
        logger.debug("list path: %s" % temp_path)
        delete_path(temp_path)


def delete_path(path):
    logger.debug("start delete: %s" % path)
    if not os.path.exists(path):
        logger.error("Path: %s is not exist" % path)
    if os.path.isfile(path):
        os.remove(path)
        logger.debug("File deleted: %s" % path)
    elif os.path.isdir(path):
        clear_dir(path)
    else:
        logger.error("Not a file or folder: %s" % path)
        return

    try:
        os.rmdir(path)
        logger.debug("Folder deleted: %s" % path)
    except:
        logger.error("Failed to delete folder: %s" % path)
        pass

    return


def get_img_num(img_dir):
    if not os.path.exists(img_dir):
        logger.error("path: %s is not exists" % img_dir)
        return -1
    img_list = os.listdir(img_dir)
    file_num = len(img_list)
    img_num = 0
    for i in range(file_num):
        if is_img_file(img_list[i]):
            img_num += 1
    return img_num


def get_img_list(img_list, img_dir):
    if not os.path.exists(img_dir):
        logger.error("path: %s is not exists" % img_dir)
        return -1
    file_list = os.listdir(img_dir)
    file_num = len(file_list)
    img_num = 0
    for i in range(file_num):
        if is_img_file(file_list[i]):
            img_num += 1
            img_list.append(file_list[i])
    return img_num


def get_img_list_with_compare(img_list, img_dir, compare_func=None):
    img_num = get_img_list(img_list, img_dir)
    if compare_func == None:
        img_list.sort()
    else:
        img_list.sort(compare_func)
    return img_num
