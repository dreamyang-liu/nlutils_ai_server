import subprocess
import os
import time

from nlutils.Utils.Log import default_logger
from nlutils.Utils.Exception import *

def task_dispatcher(server_infos, task_list):
    pass

def task_info_check(task_info):
    try:
        required_fileds = ["repo_name", "repo_url", "assigned_gpu_id", "assigned_server", "launch_script"]
        for required_filed in required_fileds:
            if required_filed not in task_info.keys():
                default_logger.error(f"{required_filed} is required for task information")
                return False
        if type(task_info["assigned_gpu_id"]) != int:
            default_logger.error(f"assigned_gpu_id must be an integer")
            return False
    except Exception:
        return False
    return True