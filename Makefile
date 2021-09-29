PYTHON_BIN=python3
PIP_BIN=pip3
MANAGE_FILE=manage.py
REQUIREMENTS_FILE=requirements.txt


help:
	@echo 'Makefile for Progame                                                     '
	@echo '                                                                         '
	@echo 'Usage:                                                                   '
	@echo '   make setup    install dependencies and execute migrations             '
	@echo '   make run      run Django built-in server                              '
	@echo '   make test     run all or specific app tests                           '


setup:
	@$(PIP_BIN) install -r $(REQUIREMENTS_FILE)
	@$(PYTHON_BIN) $(MANAGE_FILE) migrate
	@$(PYTHON_BIN) $(MANAGE_FILE) loaddata conquistas

run:
	@$(PYTHON_BIN) $(MANAGE_FILE) runserver

test:
	@$(PYTHON_BIN) $(MANAGE_FILE) test $(app)
