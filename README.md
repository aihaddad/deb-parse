# Deb-Parse

A simple parser for [Debian control file formats][1].

Once initialized, it exposes three attributes with information from the input Control File, and one method to export the information to a JSON file.

_A CLI functionality may be added later._

## Installation

Install using `pip`:

```
$ pip install --user -e .
```

## Usage

### Import it in your project

```python
from deb_parse.parser import Parser
```
Initialze it with a valid Control File path or a string that follows the schema:

```python
my_parser = Parse("/var/lib/dpkg/status")
```
__Note:__ A `TypeError` is raised if the input is not `str`
__Note:__ A `ValueError` is raised if the input string or path don't follow the schema

If everything goes well, `my_parser` will now have three accessible attributes:

* `my_parser.pkg_names` outputs a `list` of package names in the input
* `my_parser.raw_pkg_info` outputs a `list` of raw `dict` objects as seen in input
* `my_parser.clean_pkg_info` outputs a `list` of cleaned up `dict` objects with more useful information

_Examples:_

```python
print(my_parser.pkg_names)

['libws-commons-util-java', 'python-pkg-resources', 'tcpd', ... ]
```

```python
print(my_parser.raw_pkg_info)

[{'name': 'libws-commons-util-java', 'details': {'status': 'install ok installed', 'priority': 'optional', 'section': 'java', 'installed-size': '101', 'maintainer': 'Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>', 'architecture': 'all', 'version': '1.0.1-7', 'description': 'Common utilities from the Apache Web Services Project\n This is a small collection of utility classes, that allow high\n performance XML processing based on SAX.', 'original-maintainer': 'Debian Java Maintainers <pkg-java-maintainers@lists.alioth.debian.org>', 'homepage': 'http://ws.apache.org/commons/util/'}}, ... ]
```

```python
print(my_parser.clean_pkg_info)

[{'name': 'libws-commons-util-java', 'details': {'version': '1.0.1-7', 'synopsis': 'Common utilities from the Apache Web Services Project', 'description': 'This is a small collection of utility classes, that allow high\nperformance XML processing based on SAX.', 'depends': None, 'alt_depends': None, 'reverse_depends': None}}, ... ]
```

If you want, you can also dump the parsed information in a JSON file using `.to_json_file()`:

Attributes:
* outfile= str, default: './datastore/dpkgs.json'
* names_only= bool, default: False (if True supercedes other options, outputs list of names)
* raw= bool, default: False (if True outputs raw parse)

If both options are False, JSON will be based on clean package information


## Development

For working on `deb-parse`, you will need Python >= 3.7 and [`pipenv`][2] installed. Configure `pipenv` to create its `.venv` in the current folder if you want to use the VS-Code settings. With these installed, run the following command to create a virtualenv for the project and fetch the dependencies:

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

[1]: https://www.debian.org/doc/debian-policy/ch-controlfields.html
[2]: https://docs.pipenv.org/en/latest/
