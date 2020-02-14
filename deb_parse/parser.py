import os
import re
import json
import logging


class Parser:
    """
    Parses Debian Control-File formats

    Exposes three attributes and one instance method:
    - self.raw_pkg_info   ==> Outputs a dictionary object with values after initial parse
    - self.clean_pkg_info ==> Outputs a dictionary object with only useful and clean values
    - self.pkg_names      ==> Outputs a list object with only the names of the packages in file
    - self.to_json_file() ==> Dumps dictionary outputs to a JSON file
    """

    def __init__(self, file):
        file_text = self.__read_input(file)
        packages = file_text.split("\n\n")

        if len(packages[0]) > 0:
            self.raw_pkg_info = [self.__get_raw_info(pkg) for pkg in packages]
            self.clean_pkg_info = [self.__get_clean_info(pkg) for pkg in self.raw_pkg_info]
            self.pkg_names = [pkg["name"] for pkg in self.raw_pkg_info]

    def to_json_file(self, outfile="./datastore/dpkgs.json", names_only=False, raw=False):
        """
        Dumps parsed data into JSON output file

        Attributes:
        - outfile= str, default: './datastore/dpkgs.json'
        - names_only= bool, default: False (if True supercedes other options, outputs list of names)
        - raw= bool, default: False (if True outputs raw parse)

        If both options are False, JSON will be based on clean package information
        """
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        try:
            if names_only:
                with open(outfile, "w") as f:
                    json.dump(self.pkg_names, f, indent=4)
            elif raw:
                with open(outfile, "w") as f:
                    json.dump(self.raw_pkg_info, f, indent=4)
            else:
                with open(outfile, "w") as f:
                    json.dump(self.clean_pkg_info, f, indent=4)
            logging.info("extracted information to JSON file")
        except:
            logging.exception("unable to write to file")

    # Private
    def __read_input(self, input_obj):
        if type(input_obj) is not str:
            raise TypeError("input must be string or string path to file")
        elif os.path.exists(os.path.dirname(input_obj)):
            with open(input_obj, "r") as f:
                file_text = f.read().strip()
            return file_text
        else:
            return input_obj.strip()


    def __get_raw_info(self, text):
        """Parses a Debian control file and returns raw dictionary"""
        # Extract package keys and values
        keys = [key[:-2].lower() for key in re.findall(r"[A-Za-z-]*:\s", text)]
        values = re.split(r"\s?[A-Za-z-]*:\s", text)[1:]

        # Composing initial package info dict
        if len(values) > 0:
            pkg_name = values[0]
            pkg_details = dict(zip(keys[1:], values[1:]))
            pkg_dict = {"name": pkg_name, "details": pkg_details}
            return pkg_dict
        else:
            raise ValueError("file or text don't match Debian Control File schema")

    def __get_clean_info(self, pkg_raw_info):
        """Cleans up raw parsed package information and filters unneeded"""
        pkg_name = pkg_raw_info["name"]
        (
            version,
            synopsis,
            description,
            depends,
            alt_depends,
            reverse_depends,
        ) = self.__assign_clean_values(pkg_raw_info)

        pkg_clean_details = {
            "version": version,
            "synopsis": synopsis,
            "description": description,
            "depends": depends,
            "alt_depends": alt_depends,
            "reverse_depends": reverse_depends,
        }
        pkg_dict = {"name": pkg_name, "details": pkg_clean_details}

        return pkg_dict

    def __assign_clean_values(self, raw_info):
        """Handles safe value assignments in cases of missing information"""
        pkg_name = raw_info["name"]
        version = raw_info["details"].get("version")
        long_description = raw_info["details"].get("description")
        pkg_depends = raw_info["details"].get("depends")
        reverse_depends = self.__get_reverse_depends(pkg_name, self.raw_pkg_info)

        if long_description is not None:
            split_description = tuple(long_description.split("\n", maxsplit=1))
            synopsis = split_description[0]
            description = (
                re.sub(r"^\s", "", split_description[1], flags=re.MULTILINE)
                if 1 < len(split_description)
                else None
            )
        else:
            synopsis, description = None, None

        if pkg_depends is not None:
            depends_and_alt = pkg_depends.split(" | ")
            depends = depends_and_alt[0].split(", ")
            alt_depends = (
                depends_and_alt[1].split(", ") if 1 < len(depends_and_alt) else None
            )
        else:
            depends, alt_depends = None, None

        return (version, synopsis, description, depends, alt_depends, reverse_depends)

    def __get_reverse_depends(self, pkg_name, pkg_dict_list):
        """Gets the names of the packages that depend on the the specified one"""
        r_depends = []
        for pkg in pkg_dict_list:
            pkg_depends = pkg["details"].get("depends")
            if pkg_depends is not None:
                if pkg_name in pkg_depends:
                    r_depends.append(pkg["name"])

        return None if len(r_depends) == 0 else r_depends
