# import os

# from utils import gpu_memory_watcher


# server_infos = gpu_memory_watcher()
# for key, val in server_infos.items():
#     for device in val:
#         if device['device_available_memory'] > 15000:
#             print(key, device['device_id'])

from AIServerSocket import AIServerSocketStore

x = AIServerSocketStore('asd')
x.bind('127.0.0.1', 22005)
x.run()