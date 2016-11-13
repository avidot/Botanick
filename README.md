# Botanick

![image] 
![image][1] 
![Codacy Badge] 
![Codacy Coverage Badge]![Codacy Badge] 
![Documentation Status] 
![Updates]

-   Free software: MIT license
-   Documentation: <https://Botanick.readthedocs.io>.

## Features

- Search email address for a specified domain
- Reachable by RESTFUL webservice call
- Reachable by email communication

## Installation

### Pypi methode
```shell
$ pip install -U botanick
```

### Docker methode
```shell
$ docker pull avidot/botanick:latest
```

## Usages
### Python methode
```shell
$ botanick webservice # Run botanick as a webservice
$ botanick inline foo.com # Run botanick from the shell
```
### Docker methode
```shell
$ docker run -d -p 5000:5000 avidot/botanick:latest
```

## Credits
Authors: Adrien Vidot (avidot), Hervé Beraud (4383)

This package was created with [Cookiecutter] and the [audreyr/cookiecutter-pypackage] project template.

[image]: https://img.shields.io/pypi/v/Botanick.svg
[![image]]: https://pypi.python.org/pypi/Botanick
[1]: https://img.shields.io/travis/avidot/Botanick.svg
[![image][1]]: https://travis-ci.org/avidot/Botanick
[Codacy Badge]: https://api.codacy.com/project/badge/Grade/45701b2cbc724d22b60381a8e3cec5e0
[![Codacy Badge]]: https://www.codacy.com/app/Codacy/python-codacy-coverage
[Codacy Coverage Badge]: https://api.codacy.com/project/badge/Coverage/45701b2cbc724d22b60381a8e3cec5e0
[Documentation Status]: https://readthedocs.org/projects/Botanick/badge/?version=latest
[![Documentation Status]]: https://Botanick.readthedocs.io/en/latest/?badge=latest
[Updates]: https://pyup.io/repos/github/avidot/Botanick/shield.svg
[![Updates]]: https://pyup.io/repos/github/avidot/Botanick/
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[audreyr/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
