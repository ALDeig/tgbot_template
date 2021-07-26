# tgbot_template

#Alembic
alembic init alembic
#in env.py import Base from models.models
alembic revision --message="Create tables" --autogenerate
alembic upgrade head
