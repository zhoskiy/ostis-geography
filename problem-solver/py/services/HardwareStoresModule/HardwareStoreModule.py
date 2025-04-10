from common import ScModule, ScKeynodes, ScPythonEventType
from GetHardwareStoreByRatingAgent import GetHardwareStoreByRatingAgent
from GetHardwareStoreByCityAgent import GetHardwareStoreByCityAgent
from GetHardwareStoreByReviewsNumberAgent import GetHardwareStoreByReviewsNumberAgent

from sc import *


class HardwareStoresModule(ScModule):

    def __init__(self):
        ScModule.__init__(
            self,
            ctx=__ctx__,
            cpp_bridge=__cpp_bridge__,
            keynodes=[],
        )
        self.keynodes = ScKeynodes(self.ctx)

    def OnInitialize(self, params):
        print('Initialize Hardware Stores module')
        question_initiated = self.keynodes['question_initiated']

        getHardwareStoreByRatingAgent = GetHardwareStoreByRatingAgent(self)
        getHardwareStoreByRatingAgent.Register(question_initiated, ScPythonEventType.AddOutputEdge)

        getHardwareStoreByCityAgent = GetHardwareStoreByCityAgent(self)
        getHardwareStoreByCityAgent.Register(question_initiated, ScPythonEventType.AddOutputEdge)

        getHardwareStoreByReviewsNumberAgent = GetHardwareStoreByReviewsNumberAgent(self)
        getHardwareStoreByReviewsNumberAgent.Register(question_initiated, ScPythonEventType.AddOutputEdge)

    def OnShutdown(self):
        print('Shutting down Hardware Stores module')


service = HardwareStoresModule()
service.Run()
