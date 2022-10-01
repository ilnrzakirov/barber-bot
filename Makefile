makemigrations:
	alembic revision --m="$(NAME)" --autogenerate

migrate:
	alembic upgrate head