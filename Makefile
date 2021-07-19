SRC = $(wildcard nbs/*ipynb)
C_SRC = $(wildcard src/*.c)
C_SRC_DIR = src/
BUILD = build/
COBJS = $(patsubst $(C_SRC_DIR)%.c,$(BUILD)%.o,$(wildcard $(C_SRC_DIR)*.c))
CLIB_OUTPUT_DIR = audioengine/clib/
CLIB_NAME = libwavutil.so
CLIB_OUTPUT_PATH = $(CLIB_OUTPUT_DIR)$(CLIB_NAME)

all: audioengine #docs

$(BUILD)%.o: $(C_SRC_DIR)%.c
	gcc -c -Wall -Werror -fpic $< -o $@

audioengine: $(SRC) $(COBJS)
	mkdir -p $(CLIB_OUTPUT_DIR)
	gcc -shared -o $(CLIB_OUTPUT_PATH) $(COBJS)
	nbdev_clean_nbs --clear_all=True
	nbdev_build_lib

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	#touch docs

test: 
	nbdev_test_nbs

#release: pypi
#	nbdev_bump_version
#
#pypi: dist
#	twine upload --repository pypi dist/*
#
#dist: clean
#	python setup.py sdist bdist_wheel
#
#clean:
#	rm -rf dist
