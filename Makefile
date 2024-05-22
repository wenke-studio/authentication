quick-start:
	uvicorn server.main:app --reload


requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes


reset:
	rm -f db.sqlite3
	uvicorn server.main:app --reload
