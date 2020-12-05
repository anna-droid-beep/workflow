import json

from Components.Item import Item


class Charter(Item):
    """
    Draft of a graphical chart class. Right now, I suppose a graphical chart has some rules,
    Rules can be a list of colors etc...
    """
    def __init__(self, charter_name, charter_step, rules):
        self._rules = rules
        super().__init__(charter_name, charter_step)

    @property
    def rules(self):
        return self._rules

    def __str__(self):
        return json.dumps(self, default=lambda x: x.__dict__)