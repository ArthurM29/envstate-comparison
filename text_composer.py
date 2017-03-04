from composer import Composer
import itertools


class TextComposer(Composer):
    def create_content(self, env1, env2):

        content = ""
        service_diff = []
        db_diff = []
        error_diff = []

        for item in self.difference:
            if hasattr(item,'svc_build_version'):
                service_diff.append([item.description, item.svc_build_version])
            if hasattr(item, 'db_build_version') and item.db_build_version != []:
                db_diff.append(item.db_build_version)
            if hasattr(item, 'error_message'):
                for i in range(len(item.error_message)):
                    if item.error_message[i] is None:
                        item.error_message[i] = 'No error'
                error_diff.append([item.description, item.error_message])

        # preparing content for service differences
        content += '\n'
        content += '{0}{1}{2}'.format(65*'=', 'Services', 90*'=' + 3*'\n')

        if not service_diff:  # if the list is empty
            content += 'No difference in services'
        else:
            content += 163*'-' + '\n'
            content += '{:<50}{:<60}{}'.format('Service', env1, env2 + '\n')
            content += 163*'-' + 3*'\n'
            for item in service_diff:
                content += '{:<50}{:<60}{}'.format(item[0], item[1][0], item[1][1] + '\n')

        # preparing content for database differences
        content += 3*'\n'
        content += '{0}{1}{2}'.format(65*'=', 'Databases', 89*'=' + 3*'\n')

        # eliminate the duplicates
        db_diff.sort()
        db_diff = list(db_diff for db_diff, _ in itertools.groupby(db_diff))

        if not db_diff:
            content += 'No difference in databases'
        else:
            content += 163*'-' + '\n'
            content += '{:<60}{}'.format(env1, env2 + '\n')
            content += 163*'-' + 3*'\n'
            for item in db_diff:
                for i in range(len(item)):
                    content += ('{:60}{}'.format(item[i][0], item[i][1])) + '\n'

        # preparing content for errors
        content += 3*'\n'
        content += '{0}{1}{2}'.format(65*'=', 'Errors', 92*'=' + 3*'\n')

        if not error_diff:
            content += 'No errors'
        else:
            content += 163*'-' + '\n'
            content += '{:<20}{}'.format('Environment', 'Service' + '\n')
            content += 163*'-' + 3*'\n'

            for item in error_diff:
                content += 163 * '_' + '\n'
                content += '{:<20}{:<40}{}'.format(env1, item[0], 2*'\n' + item[1][0] + 2*'\n')
                content += 163 * '_' + '\n'
                content += '{:<20}{:<40}{}'.format(env2, item[0], 2*'\n' + item[1][1] + 2*'\n')

        print("\nComparison completed successfully !")

        return content

    def get_extension(self):
        return '.txt'



