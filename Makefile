test:
	test -d env || virtualenv env
	env/bin/pip install djangocms-helper pysqlite
	env/bin/python setup.py install
	mkdir -p shippable/testresults
	. env/bin/activate; make runtest

runtest:
	djangocms-helper aldryn_people test --cms --extra-settings=test_settings
