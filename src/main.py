
from TaskManager import TaskManager
from AIServerController import GLOBAL_CONTROLLER
from AIServerSocket import AIServerSocketStore
from GPUManager import GPUServerManager
from CommandHandler import COMMAND_HANDLER_STORE

GLOBAL_CONTROLLER.gpu_manager = GPUServerManager.get_instance()
GLOBAL_CONTROLLER.gpu_manager.run()
GLOBAL_CONTROLLER.command_handler_store = COMMAND_HANDLER_STORE
GLOBAL_CONTROLLER.task_manager = TaskManager()
GLOBAL_CONTROLLER.task_manager.run()

GLOBAL_CONTROLLER.socket = AIServerSocketStore()
GLOBAL_CONTROLLER.socket.bind()
GLOBAL_CONTROLLER.socket.run()