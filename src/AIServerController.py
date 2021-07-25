from typing import Union
from nlutils.Utils.SocketStore import SocketSenderProxy

__all__ = ['GLOBAL_CONTROLLER']
class AIServerController(object):

    def __init__(self):
        self.gpu_manager = None
        self.command_handler_store = None
        self.socket = None
        self.task_manager = None
        self.sender_proxy = SocketSenderProxy()

GLOBAL_CONTROLLER = AIServerController()