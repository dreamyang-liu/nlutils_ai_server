import subprocess
import os
import time


def gpu_memory_watcher():
    servers = []
    with open('./server.conf', 'r') as f:
        servers = f.readlines()
    server_infos = dict()
    for server in servers:
        cmd = '''ssh username@host "nvidia-smi | grep 'MiB' | awk '{print \$9 \$11}' | grep -v '|'" > ./tmp
        cat tmp
        '''
        server = server.replace('\n', '')
        username = server.split(' ')[0]
        host = server.split(' ')[1]
        cmd = cmd.replace('host', host)
        cmd = cmd.replace('username', username)
        print(cmd)
        device_memories = subprocess.getoutput(cmd)
        if 'command not found' in device_memories:
            raise CUDANotFoundException("\033[;91;1mCUDA is not found in current environment.\033[0m")
        if 'MiB' not in device_memories:
            raise SSHConnectionError('Error occurred while trying to connect GPU server via SSH.')
        device_memories = device_memories.split("\n")
        os.system('rm ./tmp')
        
        device_infos = list()
        for device_id, device_memory in enumerate(device_memories):
            device_used_memory = int(device_memory.split("MiB")[0])
            device_total_memory = int(device_memory.split("MiB")[1])
            device_available_memory = device_total_memory - device_used_memory
            device_available_memory_precent = device_available_memory / device_total_memory
            device_info = {'device_id': device_id, 'device_total_memory':device_total_memory, 'device_available_memory': device_available_memory, 'device_used_memory':device_used_memory, 'device_available_memory_precent': device_available_memory_precent, 'device_info_last_update_timestamp': time.time()}
            device_infos.append(device_info)
        server_infos[server.replace('\n', '')] = device_infos
    return server_infos

def task_dispatcher(server_infos, task_list):
    pass