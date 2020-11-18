FROM python:3.8.5
WORKDIR /home/oorgien/code/Project2
ENV FLASK_APP project.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
