import os

def handle_config_args(path_project, configs):

    config_jsons = []

    for config_filename in configs:

        _, file_extension = os.path.splitext(config_filename)

        if file_extension == '.list':
            # open the list file which lists up the config json file to be used
            with open(os.path.join(path_project, config_filename), 'rt') as fin:
                names = fin.read().splitlines()
                # remove empty strings
                names = list(filter(None, names))
                # add to the final list
                config_jsons.extend(names)
        elif file_extension == '.json':
            # add to the final list
            config_jsons.append(config_filename)
        else:
            raise Exception('Unrecognized file extension (must be .list or .json)')

    return config_jsons
