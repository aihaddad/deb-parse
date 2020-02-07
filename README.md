# Deb-Parse

A simple Parser for Debian Control-File formats. It exposes three attributes with information from the input Control File, and one method to export the information to a JSON file.

A CLI functionality may be added later.

## Installation

Install using `pip`:

```
$ pip install --user -e .
```

## Usage

### Import it in your project

```python
from deb_parse.parser import Parser

# Initialize
my_parser_instance = Parse("/var/lib/dpkg/status")
```

At this point the `my_parser_instance` will have three accessible attributes:
* `my_parser_instance.pkg_names` outputs a list of package names in the input file
* `my_parser_instance.raw_pkg_info` outputs a list of dict objects after the first parsing run (_values are just strings_)
* `my_parser_instance.clean_pkg_info` outputs a list of dict objects with specific information after cleanup.
(_Specifically: name, version, synopsis, description, dependencies, alternative dependencies and reverse dependencies_)

`my_parser_instance` also has the method `.to_json_file()`
`.to_json_file()` takes two variables: `outfile="./datastore/dpkgs.json", raw=False`


## Development

For working on `deb-parse`, you will need Python >= 3.7 and [`pipenv`][1] installed. Configure `pipenv` to create its `.venv` in the current folder if you want to use the VS-Code settings. With these installed, run the following command to create a virtualenv for the project and fetch the dependencies:

```
$ pipenv install --dev
...
```

Next, activate the virtual environment and get to work:

```
$ pipenv shell
...
(deb-parse) $
```

[1]: https://docs.pipenv.org/en/latest/
