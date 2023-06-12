# wacto-backend

## Installation
### Project
```sh
pipenv shell
pipenv install
```
### Python Installation
```sh
sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8 python3.8-distutils -y
```
## Usage
### Activate Environment
```sh
pipenv shell
```
### Install/Add new package
```sh
pipenv install <package_name>
```
### Install/Add new package as development dependency
```sh
pipenv install -D <package_name>
```
### Generating requirements files from a Pipfile
```sh
pipenv lock -r > requirements.txt
pipenv lock -r -d > dev-requirements.txt
```
### Pre-commit Installation
NOTE: Installing git hook
```sh
pre-commit install
```
now pre-commit will run automatically on git commit

NOTE: Run against all the files
```sh
pre-commit run --all-files
```

## References
[pre-commit reference](https://pre-commit.com/)