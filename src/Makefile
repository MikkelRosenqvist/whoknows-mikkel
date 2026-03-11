.PHONY: init run test

init:
	cd backend && python3 -c "from app import app, init_db; app.app_context().push(); init_db()"

run:
	cd backend && python3 app.py

test:
	cd backend && python3 -m pytest app_tests.py -v
