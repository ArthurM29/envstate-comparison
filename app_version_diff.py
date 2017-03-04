class AppVersionDifference:

    def __init__(self, description):
        self.description = description

    def set_from_app_version(self, app_v, from_first):
        # adding 'Not deployed' strings to avoid further issues with accessing empty strings
        label = self.description + ' not deployed'

        # create error_message attribute only if the tail itself has an error
        if app_v.error_message:
            self.error_message = [app_v.error_message, label] if from_first else [label, app_v.error_message]

        self.svc_build_version =[app_v.service_build_version, label] if from_first else [label, app_v.service_build_version]

        self.db_build_version = []
        if app_v.db_build_version:
            self.db_build_version.append(   # casting list to string to avoid unnecessary nested list
                [''.join(app_v.db_build_version), label] if from_first else [label, ''.join(app_v.db_build_version)])
