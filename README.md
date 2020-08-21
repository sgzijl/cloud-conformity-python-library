# cloud-conformity-python-library
Python library to interact with Cloud Conformity API


## Requirements

* [Python 3.X.X](https://www.python.org/downloads/)
* [Virtualenv](https://virtualenv.pypa.io/en/latest/) (Optional but recommended)


## Installation

You can use `pip` and `virtualenv`. Create a new virtual environment, then activate the environment and install:
```bash
$ virtualenv -p python3 <path_to_anywhere_you_want_to>
$ source <path_to_anywhere_you_want_to>/bin/activate
$ pip install cloud-conformity
```

The other way, you can install it to your system's Python 3 (without `virtualenv`). 
In that case, `sudo` is most likely be required and `pip3` is the command you should be using to install the package to your Python 3:
```bash
$ sudo pip3 install cloud-conformity
```


## Test Your Installation

If you are using virtualenv, make sure the environment is activated. If not, make sure you are using the correct python:
```
$ python3
```

In the python interpreter, insert the following statements:
```
>>> from cloud_conformity import CloudConformity
>>> CloudConformity
```

The output should be: `<class 'cloud_conformity.cloud_conformity.CloudConformity'>`


## Maintainer Guide
1. After updating the code, make sure to update the code version on [setup.py](setup.py#L10)
2. Follow [this guide](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives) to ship the code to PyPi: 


## Author

- [Rafi Kurnia Putra](https://github.com/rafikurnia)


## License

Apache 2 Licensed. See [LICENSE](https://github.com/traveloka/cloud-conformity-python-library/blob/master/LICENSE) for full details.
