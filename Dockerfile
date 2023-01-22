FROM python:3.9
WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt
COPY ./backend /backend/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]