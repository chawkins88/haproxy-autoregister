#!/bin/bash

./HAAutoReg.py addService --name test1 --addr 0.0.0.0:2000 
./HAAutoReg.py addServer --service test1 --name s1 --addr 10.10.10.10:2000
./HAAutoReg.py addServer --service test1 --name s2 --addr 10.10.10.10:2000
./HAAutoReg.py addServer --service test1 --name s3 --addr 10.10.10.10:2000

