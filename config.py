from configparser import ConfigParser
import os
from os.path import expanduser


class Config:
    def __init__(self, environments):

        # getting user's home directory
        usr_home = expanduser("~")
        new_dir = usr_home + '\\.envstate_comparison'  # directory where config.ini will be stored

        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        self.config_file = new_dir + '\\' + 'config.ini'
        self.config = ConfigParser()

        # if config file doesn't exist, create it  and initialize with DEFAULT_ENVIRONMENTS
        if not os.path.isfile(self.config_file):
            file = open(self.config_file, 'w')
            self.config.add_section('Environments')
            for key in environments:
                self.config.set('Environments', key, environments[key])
            self.config.write(file)
            file.close()

        # reading the config file content into config object
        self.config.read(self.config_file)

    def read(self, env_key):
        return self.config.get('Environments', env_key)