FROM python:3.11
WORKDIR /api
COPY main.py /api
COPY server.env /api
COPY requirements.txt /api
WORKDIR /api/app
COPY app/__init__.py /api/app
COPY app/app.py /api/app
COPY app/models.py /api/app
COPY app/auth.py /api/app
COPY app/db_logic.py /api/app
WORKDIR /api
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python main.py