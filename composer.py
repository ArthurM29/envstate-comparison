from abc import ABCMeta, abstractmethod
from _datetime import datetime
import os


class Composer(metaclass=ABCMeta):
    def __init__(self, difference):
        self.difference = difference

    @abstractmethod
    def create_content(self, env1, env2):
        pass

    @abstractmethod
    def get_extension(self):
        pass

    def create_file(self, ext, env1, env2):
        filename = env1 + ' vs ' + env2 + ' ' + datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        # creating the project folder on desktop
        folder = os.path.expanduser("~\\Desktop\\EnvState comparison\\")
        if not os.path.exists(folder):
            os.makedirs(folder)

        path = folder + filename + ext
        file = open(path, "w")
        return file

    def write_content(self, env1, env2):
        content = self.create_content(env1, env2)
        ext = self.get_extension()
        file = self.create_file(ext, env1, env2)
        file.write(content)
        file.close()