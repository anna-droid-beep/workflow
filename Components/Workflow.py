import json


class Workflow:
    def __init__(self, workflow_name):
        self._name = workflow_name
        self._steps = []
        self._items = []

    @property
    def name(self):
        return self._name

    @property
    def steps(self):
        return self._steps

    @property
    def items(self):
        return self._items

    @property
    def last_step_index(self):
        return len(self._steps) - 1

    def add_step(self, step):
        """
        Add step in the workflow
        :param step:
        :return:
        """
        self.steps.append(step)
        step.index = self.last_step_index

    def change_step_name(self, step_index, step_new_name):
        """
        Change the name of a step in the workflow
        :param step_index:
        :param step_new_name:
        :return:
        """
        if step_index-1 > self.last_step_index or step_index-1 < 0:
            raise ValueError(f"step_index must be between [1,{len(self.steps)}]. Was {step_index}")
        self.steps[step_index-1].status = step_new_name

    def add_item(self, item):
        """
        Add an Item in a workflow at step 1 initially
        :param item:
        :return:
        """
        if self.last_step_index < 0:
            raise ValueError(f"Worflow must have at least one step before adding a project to it.")
        item.item_step = self.steps[0]
        self.items.append(item)

    def upgrade_item(self, item):
        """
        Promote item to the next step
        :param item:
        :return:
        """
        if item.item_step is None:
            raise ValueError(f"Current item {item} doesn't have any step assigned to it.")
        if item.item_step.index == self.last_step_index:
            print("Marking the project as Finished.")
            item.is_complete = True
            self._items.remove(item)
            item.item_step = None
        else:
            item.item_step = self._steps[item.item_step.index+1]

    def downgrade_item(self, item):
        """
        Downgrade item to the previous step
        :param item:
        :return:
        """
        if item.item_step.index == 0:
            raise ValueError(f"Item is already at its lowest position.")
        item.item_step = self._steps[item.item_step.index-1]

    def move_item_to_step_index(self, item, step_index):
        if step_index-1 > self.last_step_index or step_index-1 < 0:
            raise ValueError(f"step_index must be between [1,{len(self.steps)}. Was {step_index}")
        item.item_step = self._steps[step_index-1]

    def __str__(self):
        return json.dumps(self, default=lambda x: x.__dict__)

