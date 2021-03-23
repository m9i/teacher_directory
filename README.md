## Teacher Directory
> #### A client has requested we create a Directory app containing all the Teachers in a given school.
 
> ## Features
- Teachers can have the same first name and last name but their email address should be unique
- A teacher can teach no more than 5 subjects
- The directory should allow Teachers to filtered by first letter of last name or by subject.
- You should be able to click on a teach in the directory and open up the profile page. From there you
can see all details for the teacher.
- An Importer will be needed to allow Teachers details to be added to the system in bulk. This should
be secure so only logged in users can run the importer.
- The CSV attached contains a list of teacher who need to be uploaded as well as the filename for the
profile image. Profile images are in the attached Zip file.
- If an image is not present for the profile then you should use a default placeholder image.



> How To Run ?
> - To run this project you need to follow the instruction in python-app.yml in .github/workflow 



> ## Tech

- [Django] - ```app```
- [Python] - ```app```
- [Restframework] - ```app/core/api/**```
- [Jinja2] - ```app/core/templates```
- [Html] - ```app/core/templates/**```
- [Javascript] - ```app/core/static/**```
- [Css] - ```app/core/static/**```
- [VSCode] - ```IDE```
- [Github-action] - ```.github/workflows/python-app.yml ```
- [Docker] - ```docker-compose.yml```
- [Travis-ci] - ```travis.yml```
- [TDD] - ``` core/test/** ```
- [markdown-it] - ```Readme.md```



> ## Installation

see the install guid on .github/workflow
> - I uploaded all the staticfiles needed for this project in the app/core/static which have made the project Javascript libs more than Python libs. 

Install the dependencies and devDependencies and start the server.

```sh
    >> runs on ubuntu or mac os
   steps:
    - uses: actions/checkout@v1
    # Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    # psycopg2 prerequisites
      > sudo apt-get install python3-dev libpq-dev
    # Install dependencies
      run: |
        > python -m pip install --upgrade pip
        > pip install -r requirements.txt
    # Make needed migrations
      > python app/manage.py makemigrations
    # Wait for db
      > python app/manage.py wait_for_db
    # Run migrations
      > python app/manage.py migrate
    # collect staticfiles
      > python app/manage.py collectstatic
    # create superuser
      > python app/manage.py createsuperuser
    # clean up unused media fiels 
      > python app/manage.py cleanup_unused_meida  -e *.gitignore -e *.png
    # Run tests 
      > python app/manage.py test
 
```

If Docker installed:

```sh
docker-compose up
```

For production environments...

```sh
use .env file in the BASE_DIR

```

> ## Features built

| Built Feat | README |
| ------ | ------ |
| API | 127.0.0.1:8000/api|
| swagger | 127.0.0.1:8000/swagger|
| admin | 127.0.0.1:8000/accounts|
| viewsite | 127.0.0.1:8000/core|
| list | 127.0.0.1:8000/core/list|
> ###### For more please see **ALL** the urls.py in the project

> ## Development
This Project is developed with all desired features in both B2B and B2C side. (AdminSite and View+Templates). Moreover, it has API endpoint for more UI development in near future. 


```sh
python3.8 manage.py runserver 127.0.0.1:8000
```

> ## License

 -  ```MIT```

- <img width="200" alt="api" src="https://user-images.githubusercontent.com/11647170/111675449-6047e980-8832-11eb-9964-cd7146494414.png">
  
- <img width="200" alt="basic_auth_api" src="https://user-images.githubusercontent.com/11647170/111675594-8e2d2e00-8832-11eb-928b-b00adfe51d90.png">
  
- <img width="200" alt="default_image" src="https://user-images.githubusercontent.com/11647170/111675604-8ff6f180-8832-11eb-92ed-104491cc17d0.png">
  
- <img width="200" alt="file_upload" src="https://user-images.githubusercontent.com/11647170/111675610-91281e80-8832-11eb-97fe-8b052a415a70.png">
  
- <img width="200" alt="redoc" src="https://user-images.githubusercontent.com/11647170/111675620-95543c00-8832-11eb-8899-d6131f4f8d86.png">
  
- <img width="200" alt="swagger" src="https://user-images.githubusercontent.com/11647170/111675631-984f2c80-8832-11eb-9e66-50344038609e.png">
  
- <img width="200" alt="teacher_admin_list" src="https://user-images.githubusercontent.com/11647170/111675639-99805980-8832-11eb-9447-33bcbd4a8808.png">
  
- <img width="200" alt="teacher_detail_and_view_onsite" src="https://user-images.githubusercontent.com/11647170/111675643-9b4a1d00-8832-11eb-9442-401610b5d995.png">
  
- <img width="200" alt="teacher_detail" src="https://user-images.githubusercontent.com/11647170/111675653-9c7b4a00-8832-11eb-8c1e-31f514b3a31a.png">
  
- <img width="200" alt="teacher_seach_by_last_name" src="https://user-images.githubusercontent.com/11647170/111675656-9dac7700-8832-11eb-87a5-87dfbf0c5de6.png">









