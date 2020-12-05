"""
An Item is a base class for project, charter, template etc...
"""

from abc import ABC
from enum import Enum

import json

class OFF_WORKFLOW_STATUS(Enum):
    UNASSIGNED = "UNASSIGNED"
    FINISHED = "FINISHED"

    def __init__(self, state):
        self.state = state

    def __str__(self):
        return self.state

class Item(ABC):

    def __init__(self, item_name, item_step=None):
        self._item_name = item_name
        self._item_step = item_step
        self._is_complete = False

    def __str__(self):
        return json.dumps(self, default=lambda x: x.__dict__)

    @property
    def status(self):
        if self.is_complete is True:
            return OFF_WORKFLOW_STATUS.FINISHED.state
        if self.item_step is None:
            return OFF_WORKFLOW_STATUS.UNASSIGNED.state
        return self.item_step.status

    @property
    def is_complete(self):
        return self._is_complete

    @is_complete.setter
    def is_complete(self, is_complete):
        self._is_complete = is_complete
    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, item_name):
        self._item_name = item_name

    @property
    def item_step(self):
        return self._item_step

    @item_step.setter
    def item_step(self, item_step):
        self._item_step = item_step
