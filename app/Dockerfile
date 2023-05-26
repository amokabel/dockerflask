FROM python:3.11.3-alpine3.18

WORKDIR /home/app

# Copy project files
COPY . .

# Upgrade pip before setting upp venv
RUN pip install --upgrade pip

#Setup virtual environment
ENV VIRTUAL_ENV=/home/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH = "$VIRTUAL_ENV/bin:$PATH"

# Setup python
run export FLASK_APP=app.py
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
