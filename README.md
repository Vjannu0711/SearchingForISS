# GOD'S EYE | ISS Object Detection
## By: Vrishank Jannu

### Project Description:
We live in a world where data is abundant and often unstructured. 
The goal of this project is to build a reliable and containerized Flask application that queries and returns interesting information from a large dataset that contains position and velocity data of the world-renowned International Space Station at given times as well as specific points in time and space when the ISS can be seen over select cities.
This project aims to automate the process of sifting through large and often complex datasets which is a necessary skill to have in the modern era run by big data.

### Download Original Data (Step-by-Step Instructions):
1) Log into ISP on the TACC computer.
2) On a separate window, paste this link `https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq` into your internet browser's URL and go to this site.
3) Under "Access this Data", you will see the "Public Distribution File" with two button options: TXT and XML. Right click on the `XML` option and click `Open Link in New Tab`.
4) You will see the URL of the xml file on your web browser now. Please highlight and copy this URL.
5) Now, on your TACC Computer, in a brand new directory, simply type `wget ` and then the URL. It should look something like this: `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml`
6) Next, we must download the specific sighting data with similar instructions. On the same website: `https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq`, navigate to the section that says "XMLsightingData_citiesUSA07".
7) Right click on the `XML` button and click `Open Link in New Tab`. Copy the website URL.
8) On the TACC Computer, enter this command `wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA07.xml`.

### Build Container from Dockerfile (Step-by-Step Instructions):

### Pull a Working Container from Dockerhub (Step-by-Step Instructions):

### Interact with ALL Routes in the Application using Curl (Step-by-Step Instructions):

### Interpretation of Values Returned:

### Citations:
