To create a virtual environment, in terminal run this command : (source - https://kinsta.com/blog/fastapi/)
        python3 -m venv env
activate the virtual environment run this command : (source - https://stackoverflow.com/questions/37137664/issue-with-activating-virtualenv)
        source env/bin/activate
Now, install FastAPI: 
        pip3 install fastapi
    WARNING: You are using pip version 20.2.3; however, version 23.0.1 is available.
    upgrade pip version using command:
        env/bin/python3 -m pip install --upgrade pip
Now, for create requirements file/requirements.txt need to install pipreqs command:
        pip install pipreqs
to create requirments.txt command:
        pipreqs
to test APIs we need a local web server Uvicorn. To install Uvicorn, run this command:
        pip3 install "uvicorn[standard]"
Create an empty file named __init__.py

create a file named main.py application entry point

Now in the same project directory create a file Dockerfile (source : https://fastapi.tiangolo.com/deployment/docker/)

To build the container image command : 
        docker build -t userimage .
Start the Docker Container
        docker run -d --name usercontainer -p 50:80 userimage
        docker run -d  --restart always --name usercontainer -p 50:80 userimage

start the API server using command :
        uvicorn main:app --reload
In browser, navigate to http://localhost:8000 to confirm that your API is working

