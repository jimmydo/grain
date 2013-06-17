test:
	nosetests --with-progressive

watch:
	nosetests --with-progressive --with-watch

publish:
	python setup.py sdist bdist_wininst upload
