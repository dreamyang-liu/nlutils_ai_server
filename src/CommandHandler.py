from abc import ABC, abstractmethod
from nlutils.Defines import COMMAND_ID
from utils import *
from AIServerController import *

__all__ = ['COMMAND_HANDLER_STORE']


class CommandHandler(ABC):

    @staticmethod
    def handle(msg):
        pass

class WorkerInitedDoneCommandHandler(CommandHandler):

    @staticmethod
    def handle(msg):
        default_logger.info(f"worker init done for {msg}")

class UpdateGPUSummaryDoneCommandHandler(CommandHandler):

    @staticmethod
    def handle(msg):
        default_logger.info(f"GPU summary: {msg}")
        GLOBAL_CONTROLLER.gpu_manager.update(msg['worker_alias'], msg['gpu_summary'])

class ClientLaunchTaskCommandHandler(CommandHandler):

    @staticmethod
    def handle(msg):
        GLOBAL_CONTROLLER.task_manager.add_task(msg)


COMMAND_HANDLER_STORE = {
    COMMAND_ID.COMMAND_ID_WORKER_INITED: WorkerInitedDoneCommandHandler,
    COMMAND_ID.COMMAND_ID_UPDATE_GPU_SUMMARY_DONE: UpdateGPUSummaryDoneCommandHandler,
    COMMAND_ID.COMMAND_ID_CLIENT_LAUNCH_TASK: ClientLaunchTaskCommandHandler,
}