#
# Pylr Makefile
# 
# 
#
.PHONY: doc

default:
	@echo "Use target:  install uninstall upload or doc"


test:
	python -m pylr.tests.units


# Install in develop mode
# (require setuptools)
install:
	python setup.py develop --no-deps

# Uninstall develop mode
uninstall:
	python setup.py develop --no-deps --uninstall

upload:
	python setup.py sdist upload -r lbsbuild


doc:
	sphinx-apidoc -o doc/ pylr/
	sphinx-build -b html doc/ build/doc/

upload_doc:
	rsync -av build/doc/ lbsdoc:/home/jenkins/datadoc/docs/pylr

clean:
	rm -rf build
	rm -rf dist
	rm -rf pylr/*.pyc


