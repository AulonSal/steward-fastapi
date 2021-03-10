
run:
	poetry run python run_uvicorn.py

clean-db: clean-sqlite clean-pg

clean-sqlite: clean-migrations
	rm -rf ../instance/*

clean-pg: clean-migrations
	psql --file=scripts/clean.sql

clean-migrations:
	rm -rf migrations/models

reinstall-db: remove-db
	cp ../../aerich/dist/aerich* ../dist/
	poetry add ~/developer/projects/active/steward-fastapi/dist/aerich*

refresh-db: clean-db init-db

init-db:
	poetry run aerich init-db

pypi-db: remove-db
	poetry add aerich

remove-db:
	poetry remove aerich

