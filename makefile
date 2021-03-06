.PHONY: all update

all:
	@echo "Hello $(LOGNAME)"
	@echo "Try 'make help'"


# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile


# target: update - Update pip venv packages
update:
	pipenv update
	pipenv run pip freeze > requirements.txt
