## Super simple stocks

### Requirements  
Python 3.8

#### Run demo 
```commandline
python demo.py
```
Outputs:
```commandline
INFO:root:Stock initialization
INFO:root:Stock initialization
INFO:root:Stock initialization
INFO:root:Stock initialization
INFO:root:Stock initialization
INFO:root:Stock market initialization
INFO:root:calculate_dividend_yield : 100
INFO:root:calculate_pe_ratio : 0.11
INFO:root:Volume Weighted Stock Price : 59.0
INFO:root:calculating all shares index
INFO:root:GBCE All Share Index: 58.98
```
#### Run tests
```commandline
python -m unittest tests.py
```

#### Run in Docker

Build the Docker image
```commandline
docker build -t super-simple-stocks .
```
Run the Docker container
```commandline
docker run super-simple-stocks
```
For Running test in docker, edit Dockerfile to have:
````commandline
# run demo
# CMD ["python", "demo.py"]

# run test
CMD ["python", "-m", "unittest", "tests.py"]
````
Rebuild image and re-run container.
