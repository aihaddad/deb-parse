# TODO
class DebianControlFileParser:
    # TODO
    def __init__(self, file):
        pass

    # TODO
    def to_json(self, output="datastore/debian-packages.json"):
        pass


    # Private
    def __get_raw_info(self, text):
        """Parses a Debian control file and returns raw dictionary"""
        # Extract package keys and values
        keys = [key[:-2].lower() for key in re.findall("[A-Za-z-]*: ", text)]
        values = re.split("\s?[A-Za-z-]*: ", text)[1:]

        # Composing initial package info dict
        pkg_name = values[0]
        pkg_details = dict(zip(keys[1:], values[1:]))
        pkg_dict = {"name": pkg_name, "details": pkg_details}

        return pkg_dict


    # TODO
    def __get_useful_info(self, pkg_raw_info):
        pass
