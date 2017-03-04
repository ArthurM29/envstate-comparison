import requests
import xml.etree.ElementTree as ET
from app_version import ApplicationVersion
from app_version_diff import AppVersionDifference


class EnvironmentState:

    def __init__(self, url, env):
        """call the given url and get the XML root element from the response string"""
        print("\nGetting the state for " + env.upper() + ' environment...')

        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            print("\nThe call failed. Please check the connection and try again.")
            input(5 * "\n" + "Enter any key to exit ")
        except requests.exceptions.RequestException as e:
            print('\n' + str(e))
            input(5 * "\n" + "Enter any key to exit ")

        if response.status_code == 200:
            print("Response status code - " + str(response.status_code) + ". The call was successful!")

        try:
            response_string = response.content
            root_element = ET.fromstring(response_string)
        except ET.ParseError as e:
            print('\n' + 'XML ParseError: ' + str(e))
            input(5 * "\n" + "Enter any key to exit ")

        self.application_versions = []

        for applications_node in root_element:
            for app_version in applications_node:
                self.application_versions.append(ApplicationVersion(app_version))

        response.close()

    def find_by_description(self, description):
        """take a description string and return the ApplicationVersion object containing the description"""
        for app_version in self.application_versions:
            if app_version.description == description:
                return app_version

    @staticmethod
    def compare(env_state1, env_state2):

        env_state_diff = []

        tail1 = [app_v for app_v in env_state1.application_versions if app_v not in env_state2.application_versions]
        env_state1.application_versions = [app_v for app_v in env_state1.application_versions if app_v not in tail1]

        tail2 = [app_v for app_v in env_state2.application_versions if app_v not in env_state1.application_versions]
        env_state2.application_versions = [app_v for app_v in env_state2.application_versions if app_v not in tail2]

        # loops through applicationVersions for the first environment state
        for app_version1 in env_state1.application_versions:
            app_version2 = env_state2.find_by_description(app_version1.description)
            app_diff = ApplicationVersion.compare(app_version1, app_version2)
            # if Application.compare method found some difference
            if app_diff is not None:
                env_state_diff.append(app_diff)

        # adding the tails
        for app_v in tail1:
            app_version_diff = AppVersionDifference(app_v.description)
            app_version_diff.set_from_app_version(app_v, True)
            env_state_diff.append(app_version_diff)

        for app_v in tail2:
            app_version_diff = AppVersionDifference(app_v.description)
            app_version_diff.set_from_app_version(app_v, False)
            env_state_diff.append(app_version_diff)

        # returns list of ApplicationVersionDifference objects
        return env_state_diff




