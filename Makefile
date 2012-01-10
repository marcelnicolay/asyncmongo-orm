# Turn echoing commands off
.SILENT:

PROJECT_PACKAGE=asyncmongoorm

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -rf {} \;
	rm -rf build

unit: clean
	echo "Running asyncmongoorm unit tests..."
	export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/asyncmongoorm  &&  \
		nosetests -s --verbose --with-coverage --cover-package=asyncmongoorm tests/unit/*

functional: clean
	echo "Running asyncmongoorm unit tests..."
	export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/asyncmongoorm  &&  \
		nosetests -s --verbose --with-coverage --cover-package=asyncmongoorm tests/functional/*
		
ci_test: clean
	PYTHONPATH=$PYTHONPATH:`pwd`/${PROJECT_PACKAGE} PATH="/home/quatix/virtualenv/asyncmongo/bin:$PATH" nosetests -s --verbose tests/unit/*
	PYTHONPATH=$PYTHONPATH:`pwd`/${PROJECT_PACKAGE} PATH="/home/quatix/virtualenv/asyncmongo/bin:$PATH" nosetests -s --verbose tests/functional/*