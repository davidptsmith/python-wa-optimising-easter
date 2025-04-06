FROM python:3.10-slim

WORKDIR /

COPY . .

RUN pip3 install -r app_requirements.txt

ENV PYTHONPATH .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "./app/Home.py"]

