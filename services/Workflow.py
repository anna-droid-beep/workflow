import tornado.web
import tornado.escape
import json

from helpers.WebServerHelper import ServiceEndpoint, ServiceException
import Components


class WorkflowCreationService(ServiceEndpoint):

    def initialize(self, workflow_lookup):
        self.workflow_lookup = workflow_lookup

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            workflow_name = json_request["workflow_name"]
        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)

        workflow = Components.Workflow(workflow_name)
        index = len(self.workflow_lookup.keys())
        self.workflow_lookup[index] = workflow

        res = {
            "id": index,
            "message": f"Workflow {workflow_name} added successfully. Accessible at index {index}",
            "workflow": str(workflow)
        }
        return json.dumps(res)


class WorkflowAddStepService(ServiceEndpoint):

    def initialize(self, workflow_lookup):
        self.workflow_lookup = workflow_lookup

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            workflow_index = json_request["workflow_index"]
            step_name = json_request["step_name"]
        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)

        workflow = self.workflow_lookup[workflow_index]
        step = Components.Step(step_name)
        workflow.add_step(step)
        last_step_index = workflow.last_step_index
        res = {
            "message": f"Step {step_name} added successfully at {last_step_index} in workflow of index {workflow_index}",
            "workflow": str(workflow)
        }
        return json.dumps(res)


class WorkflowChangeStepNameService(ServiceEndpoint):

    def initialize(self, workflow_lookup):
        self.workflow_lookup = workflow_lookup

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            workflow_index = json_request["workflow_index"]
            step_index = json_request["step_index"]
            step_new_name = json_request["step_new_name"]

        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)

        workflow = self.workflow_lookup[workflow_index]
        step_old_name = workflow.steps[step_index-1].status
        workflow.change_step_name(step_index, step_new_name)

        res = {
            "message": f"Step {step_old_name} was changed successfully to {step_new_name} in workflow of index {workflow_index}",
            "workflow": str(workflow)
        }
        return json.dumps(res)


class WorkflowAddItemService(ServiceEndpoint):

    def initialize(self, workflow_lookup, item_lookup):
        self.workflow_lookup = workflow_lookup
        self.item_lookup = item_lookup

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            workflow_index = json_request["workflow_index"]
            item = json_request["item"]
            item_type = item["item_type"]
            item_name = item["item_name"]
            video = item.get("video", None)
            rules = item.get("rules", None)
        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)

        meta_data = {"video": video, "rules": rules}

        workflow = self.workflow_lookup[workflow_index]
        item = Components.item_factory(item_type=item_type,
                                       item_name=item_name,
                                       item_step=None,
                                       **meta_data)
        item_index = len(self.item_lookup.keys())
        self.item_lookup[item_index] = item
        workflow.add_item(item)

        res = {
            "item_index": item_index,
            "message": f"Item {item.item_name} was added successfully to workflow of index {workflow_index}. "
                                   f"Item is now accessible at index {item_index}",
            "workflow": str(workflow)
        }
        return json.dumps(res)


class WorkflowUpgradeItemService(ServiceEndpoint):

    def initialize(self, workflow_lookup, item_lookup):
        self.workflow_lookup = workflow_lookup
        self.item_lookup = item_lookup

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            workflow_index = json_request["workflow_index"]
            item_index = json_request["item_index"]
        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)


        workflow = self.workflow_lookup[workflow_index]
        item = self.item_lookup[item_index]
        workflow.upgrade_item(item)

        res = {
            "item_index": item_index,
            "message": f"Item {item.item_name} was upgraded successfully to the next step in workflow of index {workflow_index}."
            f"If it doesn't appear in the workflow, it means the item is marked as finished.",
            "workflow": str(workflow)
        }
        return json.dumps(res)


class WorkflowDowngradeItemService(ServiceEndpoint):

    def initialize(self, workflow_lookup, item_lookup):
        self.workflow_lookup = workflow_lookup
        self.item_lookup = item_lookup

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            workflow_index = json_request["workflow_index"]
            item_index = json_request["item_index"]
        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)


        workflow = self.workflow_lookup[workflow_index]
        item = self.item_lookup[item_index]
        workflow.downgrade_item(item)

        res = {
            "item_index": item_index,
            "message": f"Item {item.item_name} was downgraded successfully to the next step in workflow of index {workflow_index}.",
            "workflow": str(workflow)
        }
        return json.dumps(res)


class WorkflowMoveItemToStepService(ServiceEndpoint):

    def initialize(self, workflow_lookup, item_lookup):
        self.workflow_lookup = workflow_lookup
        self.item_lookup = item_lookup

    async def post(self):
        try:
            json_request = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            raise ServiceException(reason='Something went wrong.', status_code=400)
        self.set_header("Content-Type", "application/json")
        self.write(await self.__worker(json_request=json_request))

    async def __worker(self, json_request):
        try:
            workflow_index = json_request["workflow_index"]
            item_index = json_request["item_index"]
            new_step_index = json_request["new_step_index"]

        except KeyError as e:
            raise ServiceException(reason=f'Field {e} is missing in the payload.', status_code=400)


        workflow = self.workflow_lookup[workflow_index]
        item = self.item_lookup[item_index]
        old_step_index = item.item_step.index
        workflow.move_item_to_step_index(item, new_step_index)

        res = {
            "item_index": item_index,
            "message": f"Item {item.item_name} was moved from Step [{old_step_index}] to  Step [{new_step_index}] "
            f"in workflow of index {workflow_index}.",
            "workflow": str(workflow)
        }
        return json.dumps(res)
