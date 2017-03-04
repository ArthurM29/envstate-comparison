from env_state import EnvironmentState
from text_composer import TextComposer
from config import Config


DEFAULT_ENVIRONMENTS = {
    'dev01': 'http://192.168.66.101:89/v1/version',
    'qa01': 'http://192.168.67.101:89/v1/version',
    'dev02': 'http://192.168.69.101:89/v1/version',
    'qa02': 'http://192.168.70.101:89/v1/version',
    'dev03': 'http://192.168.75.101:89/v1/version',
    'qa03': 'http://192.168.76.101:89/v1/version',
    #'pedev01': 'http://192.168.72.101:89/v1/version',
    #'peqa01': 'http://192.168.73.101:89/v1/version',
    'train': 'http://192.168.74.101:89/v1/version',
    'uat': 'http://192.168.68.101:89/v1/version',
    #'perf01': 'http://192.168.71.101:89/v1/version'
}

conf = Config(DEFAULT_ENVIRONMENTS)
options = sorted(conf.config.options('Environments'))
valid_envs = ' '.join(options)

while True:
    # accepting first environment from the user
    env1 = input("Enter the first environment:  ")
    if conf.config.has_option('Environments', env1):
        break
    else:
        print("Available environments: " + valid_envs + '\n')

while True:
    # accepting second environment from the user
    env2 = input("Enter the second environment:  ")
    if conf.config.has_option('Environments', env2):
        break
    else:
        print("Available environments: " + valid_envs + '\n')

# constructing the URLs for the entered environments
env_URL1 = conf.read(env1.lower())  # lowering the case to support both uppercase and lowercase inputs
env_URL2 = conf.read(env2.lower())

env_state1 = EnvironmentState(env_URL1, env1)
env_state2 = EnvironmentState(env_URL2, env2)

env_difference = EnvironmentState.compare(env_state1, env_state2)

txt_composer = TextComposer(env_difference)
txt_composer.write_content(env1.upper(), env2.upper())

# to keep the window opened until user enters a key to close
input(5*"\n" + "Enter any key to exit ")










