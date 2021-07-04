from abc import ABC, abstractmethod
from utils import *
from Define import *

__all__ = ['OPERATION_DISPATCHER']


class OperationHandler(ABC):

    @abstractmethod
    def handle(self, msg):
        pass

class WorkerInitedOperationHandler(OperationHandler):

    def handle(self, cb, **kwargs):
        cb(**kwargs)

class UpdateGPUSummaryOperationHandler(OperationHandler):

    def handle(self, cb, **kwargs):
        cb(**kwargs)


OPERATION_DISPATCHER = {
    OPERATION_ID.OPERATION_ID_WORKER_INITED: WorkerInitedOperationHandler,
    OPERATION_ID.OPERATION_ID_UPDATE_GPU_SUMMARY: UpdateGPUSummaryOperationHandler,
}