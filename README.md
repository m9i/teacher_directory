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
    - runs on ubuntu or mac os
      with:
        python-version: 3.8
    - name: psycopg2 prerequisites
      run: sudo apt-get install python3-dev libpq-dev
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Wait for db
      run: python app/manage.py wait_for_db
    - name: Run migrations
      run: python app/manage.py migrate
    - name: collect staticfiles
      run: python app/manage.py collectstatic
    - name: create superuser
      run: python app/manage.py createsuperuser
    - name: Run tests
      run: python app/manage.py test  
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
> For more please see **ALL** the urls.py in the project

> ## Development



```sh
python3.8 manage.py runserver 127.0.0.1:8000
```

> ## License

MIT

