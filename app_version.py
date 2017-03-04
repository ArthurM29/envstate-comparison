from app_version_diff import AppVersionDifference


class ApplicationVersion:

    def __init__(self, element):
        # as the xml has a default namespace,, it should be added before element name for find method to work properly
        self.description = element.find('{http://schemas.datacontract.org/2004/07/EnvironmentStateServiceModel}Description').text
        self.error_message = element.find('{http://schemas.datacontract.org/2004/07/EnvironmentStateServiceModel}ErrorMessage').text
        self.service_build_version = element.find('{http://schemas.datacontract.org/2004/07/EnvironmentStateServiceModel}ServiceBuildVersion').text

        # handling Folio and FolioArtifact DBs
        db_version = element.find('{http://schemas.datacontract.org/2004/07/EnvironmentStateServiceModel}DbBuildVersion').text
        self.db_build_version = []

        if not db_version:
            pass
        elif 'Artifact' not in db_version:
            self.db_build_version.append(db_version)
        else:  # if Artifact in db_version
            dbs = db_version.split(',')  # breaking down the initial string into Folio and FolioArtifact parts
            folio_db = dbs[0].split(':')
            artifact_db = dbs[1].split(':')
            self.db_build_version.append(folio_db[1].lstrip())  # stripping left space
            self.db_build_version.append(artifact_db[1].lstrip().strip('\n'))  # stripping left space and '\n'

    @staticmethod
    # takes 2 ApplicationVersion objects. If at least one of error_message, service_build_description or db_build_description
    # is different, returns AppVersionObject with difference data. Returns 'None' if objects are identical
    def compare(app_v1, app_v2):

        app_version_diff = AppVersionDifference(app_v1.description)

        # if one of the app versions contains error, we just return the errors
        if app_v1.error_message is not None or app_v2.error_message is not None:
            app_version_diff.error_message = [app_v1.error_message, app_v2.error_message]
            return app_version_diff

        # if error is empty for both app_version objects
        is_service_diff = False
        is_db_diff = False

        if app_v1.service_build_version != app_v2.service_build_version:
            app_version_diff.svc_build_version = [app_v1.service_build_version, app_v2.service_build_version]
            is_service_diff = True

        # DB comparison
        app_version_diff.db_build_version = []

        for i in range(len(app_v1.db_build_version)):
            if app_v1.db_build_version[i] != app_v2.db_build_version[i]:
                app_version_diff.db_build_version.append([app_v1.db_build_version[i], app_v2.db_build_version[i]])
                is_db_diff = True

        if is_service_diff or is_db_diff:
            return app_version_diff
        else:
            return None

    def __eq__(self, other):
        if isinstance(other, ApplicationVersion):
            return self.description == other.description

    def __ne__(self, other):
        return not self.__eq__(other)








