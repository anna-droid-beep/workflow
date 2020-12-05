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


class ITEM_TYPE(Enum):
    PROJECT = "PROJECT"
    CHARTER = "CHARTER"

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type


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


def item_factory(item_type, item_name, item_step, **kwargs ):
    if item_type not in (ITEM_TYPE.CHARTER.value, ITEM_TYPE.PROJECT.value):
        raise ValueError(f"Invalid ItemType. Must be either CHARTER or PROJECT. Was {item_type}")
    if item_type == ITEM_TYPE.CHARTER.value:
        return Charter(item_name, item_step, **kwargs)
    if item_type == ITEM_TYPE.PROJECT.value:
        return Project(item_name, item_step, **kwargs)


class Project(Item):
    """
    Draft of a project video class. Right now, I suppose a project has a video, we can assign the project to
    some other user etc...
    """
    def __init__(self, project_name, project_step, **kwargs):
        self._video = kwargs['video']
        super().__init__(project_name, project_step)

    @property
    def video(self):
        return self._video


class Charter(Item):
    """
    Draft of a graphical chart class. Right now, I suppose a graphical chart has some rules,
    Rules can be a list of colors etc...
    """
    def __init__(self, charter_name, charter_step, **kwargs):
        self._rules = kwargs['rules']
        super().__init__(charter_name, charter_step)

    @property
    def rules(self):
        return self._rules