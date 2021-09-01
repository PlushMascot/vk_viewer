FROM python:3
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
ENV FLASK_APP vk_viewer.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV development
EXPOSE 5000
CMD ["flask", "run"]