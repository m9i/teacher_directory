# Teacher Directory
## _ A client has requested we create a Directory app containing all the Teachers in a given school.
 
## Features
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



> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Tech

- [Django] - 
- [VSCode] - 
- [Python] - 
- [Github-action] - 
- [Docker]
- [Travis-ci]
- [TDD]
- [markdown-it]



## Installation

see the install guid on .github/workflow

Install the dependencies and devDependencies and start the server.

```sh
 python-version: 3.8
    - name: psycopg2 prerequisites
      run: sudo apt-get install python3-dev libpq-dev
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run migrations
      run: python app/manage.py migrate
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

## Plugins

| Plugin | README |
| ------ | ------ |
|  | |


## Development



```sh
127.0.0.1:8000
```

## License

MIT

