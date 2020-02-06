import re


class DebianControlFileParser:
    """Parses Debian Control-File formats and exports to JSON"""
    def __init__(self, file):
        with open(file) as f:
            __file_text = f.read()

        self.raw_package_data = [
            self.__get_raw_info(pkg) for pkg in __file_text.split("\n\n")
        ]
        self.clean_package_data = [
            self.__get_useful_info(pkg) for pkg in self.raw_package_data
        ]
        self.package_names = [pkg["name"] for pkg in self.raw_package_data]

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


    def __get_useful_info(self, pkg_raw_info):
        """Cleans up raw parsed package information and filters unneeded"""
        pkg_name = pkg_raw_info["name"]
        version, synopsis, description, depends, alt_depends = self.__get_useful_values(
            pkg_raw_info["details"]
        )

        pkg_useful_details = {
            "version": version,
            "synopsis": synopsis,
            "description": description,
            "depends": depends,
            "alt_depends": alt_depends
        }
        pkg_dict = {"name": pkg_name, "details": pkg_useful_details}

        return pkg_dict

    def __get_useful_values(self, raw_info):
        """Handles safe value assignments in cases of missing information"""
        version = raw_info.get("version")
        long_description = raw_info.get("description")
        pkg_depends = raw_info.get("depends")

        if long_description is not None:
            split_description = tuple(long_description.split("\n", maxsplit=1))
            synopsis = split_description[0]
            try:
                description = split_description[1]
            except:
                description = None
        else:
            synopsis, description = None, None

        if pkg_depends is not None:
            depends_and_alt = pkg_depends.split(" | ")
            try:
                depends = depends_and_alt[0].split(", ")
            except:
                depends = pkg_depends.split(", ")

            try:
                alt_depends = depends_and_alt[1].split(", ")
            except:
                alt_depends = None
        else:
            depends, alt_depends = None, None

        return (version, synopsis, description, depends, alt_depends)
