
tests:
	pytest .

start-celery-worker:
	cd src && celery -A main.celery_app worker --loglevel=info 

start-app:
	 cd src && uvicorn main:app --reload 


