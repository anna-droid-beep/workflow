import tornado.web
import logging

from services.Workflow import WorkflowAddItemService, WorkflowAddStepService, WorkflowChangeStepNameService, WorkflowCreationService, \
    WorkflowMoveItemToStepService, WorkflowUpgradeItemService, WorkflowDowngradeItemService


class APIGateway(tornado.web.Application):

    def __init__(self, api_cfg, **kwargs):
        self.log = logging.getLogger(__name__)

        #simulates our db
        workflow_lookup = dict()
        item_lookup = dict()

        kwargs['handlers'] = [(r"/workflow/create", WorkflowCreationService,
                               dict(workflow_lookup=workflow_lookup)),
                              (r"/workflow/add_step", WorkflowAddStepService,
                               dict(workflow_lookup=workflow_lookup)),
                              (r"/workflow/change_step_name", WorkflowChangeStepNameService,
                               dict(workflow_lookup=workflow_lookup)),
                              (r"/workflow/add_item", WorkflowAddItemService,
                               dict(workflow_lookup=workflow_lookup,
                                    item_lookup=item_lookup)),
                              (r"/workflow/upgrade_item", WorkflowUpgradeItemService,
                               dict(workflow_lookup=workflow_lookup,
                                    item_lookup=item_lookup)),
                              (r"/workflow/downgrade_item", WorkflowDowngradeItemService,
                               dict(workflow_lookup=workflow_lookup,
                                    item_lookup=item_lookup)),
                              (r"/workflow/move_item_to_step", WorkflowMoveItemToStepService,
                               dict(workflow_lookup=workflow_lookup,
                                    item_lookup=item_lookup))]

        kwargs['debug'] = api_cfg.DEBUG
        super().__init__(**kwargs)