#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 26/07/2024
@author: Zoe Dan Zhang
"""
import shutil
import os
import stat

def create_directory_if_not_exists(path):
    """
    检查文件路径是否存在,如果不存在则创建。

    Args:
        path (str): 要检查的文件路径。
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def move_file(src_filepath, dst_filepath):
    # Check if the source file exists
    if os.path.exists(src_filepath):
        # Move the file to the destination path
        shutil.move(src_filepath, dst_filepath)
        print(f"File moved from {src_filepath} to {dst_filepath}")
    else:
        print(f"Error: {src_filepath} does not exist.")


def copy_file(src_filepath, dst_filepath):
    # Check if the source file exists
    if os.path.exists(src_filepath):
        # Create the destination directory if it doesn't exist
        dst_dir = os.path.dirname(dst_filepath)
        os.makedirs(dst_dir, exist_ok=True)

        # Copy the file to the destination path
        shutil.copy(src_filepath, dst_filepath)
        print(f"File copied from {src_filepath} to {dst_filepath}")
    else:
        print(f"Error: {src_filepath} does not exist.")


def copy_file_or_folder(src_path, dst_path):
    # Check if the source path exists
    if os.path.exists(src_path):
        # Create the destination directory if it doesn't exist
        dst_dir = os.path.dirname(dst_path)
        os.makedirs(dst_dir, exist_ok=True)

        # Check if the source is a file or a directory
        if os.path.isfile(src_path):
            # Copy the file to the destination path
            shutil.copy(src_path, dst_path)
            # Make the destination file writable
            os.chmod(dst_path, stat.S_IWRITE | stat.S_IREAD)
            print(f"File copied from {src_path} to {dst_path}")
        elif os.path.isdir(src_path):
            # Copy the directory to the destination path
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            print(f"Directory copied from {src_path} to {dst_path}")
        else:
            print(f"Error: {src_path} is not a valid file or directory.")
    else:
        print(f"Error: {src_path} does not exist.")


def rename_file(old_filename, new_filename):
    """
    Renames a file from the old filename to the new filename.

    Args:
        old_filename (str): The current filename.
        new_filename (str): The new filename.
    """
    try:
        os.rename(old_filename, new_filename)
        print(f"File renamed from '{old_filename}' to '{new_filename}'.")
    except os.error as e:
        print(f"Error renaming file: {e}")
