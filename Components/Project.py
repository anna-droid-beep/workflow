from Components.Item import Item


class Project(Item):
    """
    Draft of a project video class. Right now, I suppose a project has a video, we can assign the project to
    some other user etc...
    """
    def __init__(self, project_name, project_step, video):
        self._video = video
        super().__init__(project_name, project_step)

    @property
    def video(self):
        return self._video