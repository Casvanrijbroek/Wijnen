FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#CMD ["gunicorn", "-b", ":5000","--workers=4", "--bind=0.0.0.0", "wsgi:app"]
ENTRYPOINT ["python"]
CMD ["wijnen_api.py"]
