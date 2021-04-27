import subprocess
import os


def gpu_memory_watcher():
    servers = []
    with open('./server.conf', 'r') as f:
        servers = f.readlines()
    server_infos = dict()
    for server in servers:
        cmd = '''ssh xchen648@server.cc.gatech.edu "nvidia-smi | grep 'MiB' | awk '{print \$9 \$11}' | grep -v '|'" > ./tmp
        cat tmp
        '''
        cmd = cmd.replace('server', server.replace('\n', ''))
        device_memories = subprocess.getoutput(cmd).split("\n")
        os.system('rm ./tmp')
        if 'command not found' in device_memories[0]:
            raise CUDANotFoundException("\033[;91;1mCUDA is not found in current environment.\033[0m")
        device_infos = list()
        for device_id, device_memory in enumerate(device_memories):
            device_used_memory = int(device_memory.split("MiB")[0])
            device_total_memory = int(device_memory.split("MiB")[1])
            device_available_memory = device_total_memory - device_used_memory
            device_available_memory_precent = device_available_memory / device_total_memory
            device_info = {'device_id': device_id, 'device_total_memory':device_total_memory, 'device_available_memory': device_available_memory, 'device_used_memory':device_used_memory, 'device_available_memory_precent': device_available_memory_precent}
            device_infos.append(device_info)
        server_infos[server.replace('\n', '')] = device_infos
    return server_infos