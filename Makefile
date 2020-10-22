PACKAGE_NAME := snapshottest_ext
PYPI_SERVER_URL := http://172.21.97.105

build: ## Build package
	python setup.py sdist

upload: ## Upload package
	twine upload -u admin -p admin --non-interactive --skip-existing --repository-url $(PYPI_SERVER_URL) dist/*

distribute: build upload ## Build and upload package
