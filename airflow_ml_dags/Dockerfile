FROM apache/airflow:2.3.2-python3.10
USER root
RUN apt-get update && apt-get install git -y
RUN apt-get install python3-distutils -y
RUN apt-get install python3-apt -y
RUN chmod -R 1777 /tmp
USER airflow
RUN pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.in-project true
RUN mkdir -p /home/airflow/.cache/pypoetry/
RUN chmod -R 0777 /home/airflow/.cache/
RUN chmod -R 0755 /home/airflow/.config/pypoetry/config.toml
RUN export PIP_USER=false

