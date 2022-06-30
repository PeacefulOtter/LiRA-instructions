

# Import altitude data instructions

## 1. Installation
```console
~$ cd altitude
~/altitude$ pip3 install numpy pandas psycopg2 dotenv
```
use either `pip` or `conda` depending on your packet manager

## 2. .env file
Create a .env file in the `altitude` folder, with the same format as the provided `.env.template` file.

A read-only user for the Road Condition DB can be found in the `RCDB.md` file. 
To get altitude data from the DHM service, you will need to create your own username/password using their own website. 

## 3. Run
```console
~/altitude$ jupyter notebook
```
Launch a notebook and run all the cells