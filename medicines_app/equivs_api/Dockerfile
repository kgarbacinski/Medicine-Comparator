FROM python:latest
WORKDIR /equivs_api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "__init__.py"]
