from termcolor import colored

from common import ScAgent, ScEventParams, ScKeynodes
from sc import *
from common.sc_log import Log


class GetHardwareStoreByCityAgent(ScAgent):
    def __init__(self, module):
        super().__init__(module)
        self.ctx = module.ctx
        self.keynodes = ScKeynodes(self.ctx)
        self.main_node = None
        self.log = Log(self.__class__.__name__)

    def RunImpl(self, evt: ScEventParams) -> ScResult:
        self.main_node = evt.other_addr
        status = ScResult.Ok
        self.log.debug("GetHardwareStoreByCityAgent starts")
        if self.module.ctx.HelperCheckEdge(
                self.keynodes['action_get_hardware_store_by_city'],
                self.main_node,
                ScType.EdgeAccessConstPosPerm,
        ):
            try:
                if self.main_node is None or not self.main_node.IsValid():
                    raise Exception("The question node isn't valid.")

                self.log.debug("GetHardwareStoreByCityAgent get arguments")
                city = self.get_action_argument(self.main_node, 'rrel_1')

                concept_store = self.module.ctx.HelperResolveSystemIdtf("concept_hardware_store", ScType.NodeConstClass)
                answer = self.module.ctx.HelperResolveSystemIdtf("found_store_by_city", ScType.NodeConst)
                nrel_city = self.module.ctx.HelperResolveSystemIdtf("nrel_city", ScType.NodeConstNoRole)
                store = self.module.ctx.Iterator3(concept_store, ScType.EdgeAccessConstPosPerm, ScType.NodeConst)
                while store.Next():
                    print("check new store")
                    find_store = self.module.ctx.Iterator5(store.Get(2), ScType.EdgeDCommonConst, city,
                                                            ScType.EdgeAccessConstPosPerm, nrel_city)
                    print(find_store)
                    while find_store.Next():
                        if find_store.IsValid():
                            print('is_valid')
                            self.module.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, answer, store.Get(2))
                            print('created')

                self.log.debug("GetHardwareStoreByCityAgent ends")
            except Exception as ex:
                self.set_unsuccessful_status()
                status = ScResult.Error
        return status

    def set_unsuccessful_status(self):
        self.module.ctx.CreateEdge(
            ScType.EdgeAccessConstPosPerm,
            self.keynodes['question_finished_unsuccessfully'],
            self.main_node,
        )

    def get_action_argument(self, question: ScAddr, rrel: str, argument_class=None) -> ScAddr:
        actual_argument = "_actual_argument"

        template = ScTemplate()
        template.TripleWithRelation(
            question,
            ScType.EdgeAccessVarPosPerm,
            ScType.NodeVar >> actual_argument,
            ScType.EdgeAccessVarPosPerm,
            self.keynodes[rrel],
        )
        if argument_class is not None:
            template.Triple(self.keynodes[argument_class], ScType.EdgeAccessVarPosPerm, actual_argument)

        search_result = self.ctx.HelperSearchTemplate(template)

        search_result_size = search_result.Size()
        if search_result_size > 0:
            argument_node = search_result[0][actual_argument]
        else:
            raise Exception("The argument node isn't found.")

        return argument_node

