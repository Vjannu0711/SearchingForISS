# GOD'S EYE | ISS Object Detection
## By: Vrishank Jannu

### Project Description:
We live in a world where data is abundant and often unstructured. 
The goal of this project is to build a reliable and containerized Flask application that queries and returns interesting information from a large dataset that contains position and velocity data of the world-renowned International Space Station at given times as well as specific points in time and space when the ISS can be seen over select cities.
This project aims to automate the process of sifting through large and often complex datasets which is a necessary skill to have in the modern era run by big data.

### Download Original Data (Step-by-Step Instructions):
1) Log into ISP on the TACC computer in a terminal like Windows Powershell.
2) On a separate window, paste this link `https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq` into your internet browser's URL and go to this site.
3) Under "Access this Data", you will see the "Public Distribution File" with two button options: TXT and XML. Right click on the `XML` option and click `Open Link in New Tab`.
4) You will see the URL of the xml file on your web browser now. Please highlight and copy this URL.
5) Now, on your TACC Computer, in a brand new directory, simply type `wget ` and then the URL. It should look something like this: `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml`
6) Next, we must download the specific sighting data with similar instructions. On the same website: `https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq`, navigate to the section that says "XMLsightingData_citiesUSA07".
7) Right click on the `XML` button and click `Open Link in New Tab`. Copy the website URL.
8) In the terminal, enter this command: `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA07.xml`

### Build Container from Dockerfile (Step-by-Step Instructions):
1) In the terminal, type and hit enter on this command: `touch Dockerfile`
2) Additionally, we need to specify the requirements of our Flask application. To do this, type and hit enter on this command: `emacs requirements.txt`. This will create a brand new requirements text file.
3) In this file, type this command: `Flask==2.0.3` and then save and exit from the file. This is the only line of code that you need in the file.
4) Let's modify the Dockerfile by entering `emacs Dockerfile` in the terminal.
5) Enter the following lines of code:
```
FROM python:3.9

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]
```
6) To build the container, type and modify this command to reflect your username and file name: `docker build -t <username>/<file-name>:latest .`
7) To push the container, type and enter: `docker push <username>/<file-name>:latest`

### Pull a Working Container from Dockerhub (Instructions):
1) To pull a working container from Dockerhub, simply type and enter: `docker pull <username>/<file-name>:latest`

### Interact with ALL Routes in the Application using Curl (Step-by-Step Instructions) & Interpretation of Values Returned:

1) Run this set of commands. The first three are presented below. Type each one and hit enter:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run -p 5000
```
2) Open a second terminal and log into TACC. Then, run this command: `curl localhost:5000/read_data -X POST` This command will load and read all of the data from both XML files.
3) Next, you can interact with the routes and achieve your desired output. Here is a list of the routes below:
```
**ROUTE**                                              **VALUES RETURNED**
/epochs                                                lists all epochs
/epochs/<epoch>                                        lists all data associated with a specific epoch
/countries                                             lists all countries in sighting data
/countries/<country>                                   lists all data for a specific country
/countries/<country>/regions                           lists all regions in a specific country
/countries/<country>/regions/<regions>                 lists all data for a specific region
/countries/<country>/regions/<regions>/cities          lists all cities in a specific region
/countries/<country>/regions/<regions>/cities/<city>   lists all data for a specific city
```
4) Note that in order to run these routes shown above to the left side of the table, you must first type `curl localhost:5000` followed by one of these 8 route commands. If the terminal returns an error, that means you simply need to re-enter the read_data command from Step 2 and then enter the route command on the next line.
5) The right column of the table above shows the given values returned from each application route.

### Citations (MLA):

1) Goodwin, S. (n.d.). ISS_COORDS_2022-02-13. NASA. https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml Retrieved March 17, 2022, from https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq 

2) Goodwin, S. (n.d.). XMLsightingData_citiesUSA07. NASA. Retrieved March 17, 2022, from https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA07.xml

These two data XML files represent the best estimated real-time trajectory and local sightings opportunities for the International Space Station (ISS) as generated by the Trajectory Operations and Planning (TOPO) flight controllers at the NASA Johnson Space Center.
