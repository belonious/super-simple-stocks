FROM python:3.8

WORKDIR /app

COPY . /app

# run demo
CMD ["python", "demo.py"]

# run test
# CMD ["python", "-m", "unittest", "tests.py"]

