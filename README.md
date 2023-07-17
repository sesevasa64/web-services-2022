# Foobar
Foobar is a simple web app written in python with FastAPI framework.
## Installation
In order to use Foobar you need installed [anaconda](https://www.anaconda.com/products/distribution) or [miniconda](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links) distributions.<br>
Second, install [poetry](https://python-poetry.org/) and configure it:
```sh
poetry config virtualenvs.in-project false
poetry config virtualenvs.path <conda-install-path>/envs
```
Next, create and activate *conda* virtual environment for development:
```sh
conda create -n BaseApp python=3.10
conda activate BaseApp
```
Install dependencies with Poetry:
```sh
poetry install
```
Run Foobar with command:
```sh
uvicorn app.main:app --reload
```
Run tests with command:
```sh
python -m pytest grpc/
python -m pytest main-project/
``` 
## License
[MIT](https://choosealicense.com/licenses/mit/)
