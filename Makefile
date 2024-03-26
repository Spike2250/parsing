
parse-2gis:
	poetry run start-app

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl
