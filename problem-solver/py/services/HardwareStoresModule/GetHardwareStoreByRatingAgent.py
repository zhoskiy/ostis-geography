from termcolor import colored

from common import ScAgent, ScEventParams, ScKeynodes
from sc import *
from common.sc_log import Log


class GetHardwareStoreByRatingAgent(ScAgent):
    def __init__(self, module):
        super().__init__(module)
        self.ctx = module.ctx
        self.keynodes = ScKeynodes(self.ctx)
        self.main_node = None
        self.log = Log(self.__class__.__name__)

    def RunImpl(self, evt: ScEventParams) -> ScResult:
        self.main_node = evt.other_addr 
        status = ScResult.Ok
        self.log.debug("GetHardwareStoreByRatingAgent starts")
        if self.module.ctx.HelperCheckEdge(
                self.keynodes['action_get_hardware_store_by_rating'],
                self.main_node,
                ScType.EdgeAccessConstPosPerm,
        ):
            try:
                if self.main_node is None or not self.main_node.IsValid():
                    raise Exception("The question node isn't valid.")

                self.log.debug("GetHardwareStoreByRatingAgent get arguments")

                firstRatingNode = self.get_action_argument(self.main_node, 'rrel_1')
                secondRatingNode = self.get_action_argument(self.main_node, 'rrel_2')
                answer = self.module.ctx.HelperResolveSystemIdtf("found_store_by_rating", ScType.NodeConst)

                self.log.debug("GetHardwareStoreByRatingAgent get stores")
                storeRating = self.get_hardwate_stores_with_rating()
                self.log.debug("GetHardwareStoreByRatingAgent get rating value")
                firstRating = float(self.get_main_idtf(firstRatingNode))
                secondRating = float(self.get_main_idtf(secondRatingNode))

                results = []
                for store, rating in storeRating.items():
                    if firstRating <= rating <= secondRating:
                        print(colored(str(rating), 'green'))
                        results.append(store)

                for store in results:
                    self.log.debug("GetHardwareStoreByRatingAgent add answer")
                    self.module.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, answer, store)

                self.log.debug("GetHardwareStoreByRatingAgent ends")
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

    def get_hardwate_stores_with_rating(self):
        template = ScTemplate()
        template.Triple(
            self.keynodes['concept_hardware_store'],
            ScType.EdgeAccessVarPosPerm,
            ScType.NodeVar >> '_hardware_store'
        )
        template.TripleWithRelation(
            '_hardware_store',
            ScType.EdgeDCommonVar,
            ScType.LinkVar >> '_store_rating',
            ScType.EdgeAccessVarPosPerm,
            self.keynodes['nrel_store_rating'],
        )

        search_result = self.ctx.HelperSearchTemplate(template)
        stores_with_rating = {}
        if search_result.Size():
            for i in range(search_result.Size()):
                stores_with_rating[search_result[i]['_hardware_store']] = float(self.ctx.GetLinkContent(search_result[i]['_store_rating']).AsString())
        return stores_with_rating

    def get_main_idtf(self, node):
        template = ScTemplate()
        template.TripleWithRelation(
            node,
            ScType.EdgeDCommonVar,
            ScType.LinkVar >> 'value',
            ScType.EdgeAccessVarPosPerm,
            self.keynodes['nrel_main_idtf']
        )
        template_result = self.ctx.HelperSearchTemplate(template)
        value = ''
        if template_result.Size():
            value = self.ctx.GetLinkContent(template_result[0]['value']).AsString()

        return value
