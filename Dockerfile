FROM centos:7.9.2009

RUN yum update -y

RUN yum install -y python3

RUN pip3 install pytest==7.0.0

COPY app.py /code/app.py
COPY test_app.py /code/test_app.py
COPY XMLsightingData_citiesUSA07.xml /code/XMLsightingData_citiesUSA07.xml
COPY ISS.OEM_J2K_EPH.xml /code/ISS.OEM_J2K_EPH.xml

RUN chmod +rx /code/app.py
RUN chmod +rx /code/test_app.py

ENV PATH "/code:$PATH"