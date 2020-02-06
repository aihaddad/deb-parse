import os
import re
import json


class DebianControlFileParser:
    """
    Parses Debian Control-File formats

    Exposes three attributes and one instance method:
    - self.raw_package_info   ==> Outputs a dictionary object with values after initial parse
    - self.clean_package_info ==> Outputs a dictionary object with only useful and clean values
    - self.package_name       ==> Outputs a list object with only the names of the packages in file
    - self.to_json_file()     ==> Dumps dictionary outputs to a JSON file
    """

    def __init__(self, file):
        with open(file, "r") as f:
            __file_text = f.read()
            # Clear trailing whitespaces in input file
            while __file_text[-1].isspace():
                __file_text = __file_text[:-1]

        self.raw_package_data = [
            self.__get_raw_info(pkg) for pkg in __file_text.split("\n\n")
        ]
        self.clean_package_data = [
            self.__get_clean_info(pkg) for pkg in self.raw_package_data
        ]
        self.package_names = [pkg["name"] for pkg in self.raw_package_data]

    def to_json_file(self, outfile="datastore/debian-packages.json", raw=False):
        """Converts parsed data into JSON and outputs to file"""
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        try:
            if raw:
                with open(outfile, "w") as f:
                    json.dump(self.raw_package_data, f, indent=4)
            else:
                with open(outfile, "w") as f:
                    json.dump(self.clean_package_data, f, indent=4)

            print(f"SUCCESS: wrote to file {outfile}")

        except FileNotFoundError:
            print(f"ERROR: {outfile} not found")
        except:
            print(f"ERROR: cannot write to file {outfile}")

    # Private
    def __get_raw_info(self, text):
        """Parses a Debian control file and returns raw dictionary"""
        # Extract package keys and values
        keys = [key[:-2].lower() for key in re.findall(r"[A-Za-z-]*: ", text)]
        values = re.split(r"\s?[A-Za-z-]*: ", text)[1:]

        # Composing initial package info dict
        pkg_name = values[0]
        pkg_details = dict(zip(keys[1:], values[1:]))
        pkg_dict = {"name": pkg_name, "details": pkg_details}

        return pkg_dict

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
        ) = self.__assign_needed_values(pkg_raw_info)

        pkg_useful_details = {
            "version": version,
            "synopsis": synopsis,
            "description": description,
            "depends": depends,
            "alt_depends": alt_depends,
            "reverse_depends": reverse_depends,
        }
        pkg_dict = {"name": pkg_name, "details": pkg_useful_details}

        return pkg_dict

    def __assign_needed_values(self, raw_info):
        """Handles safe value assignments in cases of missing information"""
        pkg_name = raw_info["name"]
        version = raw_info["details"].get("version")
        long_description = raw_info["details"].get("description")
        pkg_depends = raw_info["details"].get("depends")
        reverse_depends = self.__get_reverse_depends(pkg_name, self.raw_package_data)

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
            depends = depends_and_alt[0].split(", ")

            try:
                alt_depends = depends_and_alt[1].split(", ")
            except:
                alt_depends = None
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
