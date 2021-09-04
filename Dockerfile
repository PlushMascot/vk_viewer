FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
ENV FLASK_APP vk_viewer.py
ENV FLASK_ENV production
ENV FLASK_CONFIG heroku
EXPOSE 5000
CMD exec gunicorn --bind 5000:$PORT --workers 1 --threads 8 --timeout 0 vk_viewer:app
CMD exec flask run --host=0.0.0.0 --port=$PORT