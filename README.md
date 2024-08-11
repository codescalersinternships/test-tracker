<p align="center">
  <img src="./client/public/testtrackerlogo.png" width="250" height="200" alt="logo"/>
</p>
<p align="center">
  <img src="./client/public/NavBarLogo.png" width="400" alt="logo"/>
</p>

---
<p align="center">
  <img src="https://img.shields.io/badge/-TypeScript-black?style=for-the-badge&logoColor=white&logo=typescript&color=2F73BF" alt="Typescript"/>
  <img src="https://img.shields.io/badge/-Vue.js-4fc08d?style=for-the-badge&logo=vuedotjs&logoColor=white" alt="Vue"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" alt="Django"/>
  <img src="https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgresql"/>
</p>

## <a name="table-contents">Table of Contents</a>

1.  [Introduction](#introduction)
2.  [Prerequisites](#prerequisites)
3.  [Setup on your local machine](#local-setup)
4.  [Setup using docker](#docker-setup)
5.  [Tests](#tests)


## <a name="introduction">Introduction</a>

TestTracker allows the Quality Assurance team to manage their test plans, requirements, test cases and test runs in a simple and efficient way. All essential tools to manage your test cases all in one place. 

## <a name="prerequisites">Prerequisites</a>

Make sure you have installed all of the following prerequisites on your machine:
* Git - [Download & Install Git](https://git-scm.com/downloads). OSX and Linux machines typically have this already installed.
* Node.js - [Download & Install Node.js](https://nodejs.org/en/download/) and the pnpm package manager. If you encounter any problems, you can also use this [GitHub Gist](https://gist.github.com/isaacs/579814) to install Node.js.
* Python3 - [Download & Install Python3](https://www.python.org/downloads/).
* Poetry - [Download & Install Poetry](https://python-poetry.org/docs/).
* Docker - [Download & Install Docker](https://docs.docker.com/engine/install/). Skip this step if you plan to use your local machine to run Test Tracker.


## <a name="local-setup">Setup on your local machine</a>

1. Clone the Repository to a directory of your choice.
2. Create .env file using the following template:

        # === General ===        
        DJANGO_SECRET_KEY=
        SERVER_DOMAIN_NAME=
        SERVER_DOMAIN_NAME_API=
        CLIENT_DOMAIN_NAME=
        ENV=production
        DJANGO_DEBUG=OFF
        
        
        # === Email ===
        EMAIL=
        EMAIL_PASSWORD=
        EMAIL_HOST=
        
        # === Database ===
        DATABASE_NAME=
        DATABASE_USER=
        DATABASE_PASSWORD=
        DATABASE_HOST=
        DATABASE_PORT=
        
        DJANGO_SUPERUSER_EMAIL=
        DJANGO_SUPERUSER_PASSWORD=
  
4. Run the following command to install dependencies:
      console
    make install
   
5. Run the following command to setup the server:
      console
    make migrate
   
6. Run the following command to create a super user:
      console
    make user
   
7. Run the following command to run server:
      console
    make runserver
   
8. Open a new terminal tab.
9. Run the following command to run client:
      console
    make runclient
   
10. Press Click + CTRL on the URL to open the client.
11. Enjoy Test Tracker features.

## <a name="docker-setup">Setup using docker</a>

1. Clone the Repository to a directory of your choice.
2. Create .env file using the following template:

        # === General ===        
        DJANGO_SECRET_KEY=
        SERVER_DOMAIN_NAME=
        SERVER_DOMAIN_NAME_API=
        CLIENT_DOMAIN_NAME=
        ENV=production
        DJANGO_DEBUG=OFF
        
        
        # === Email ===
        EMAIL=
        EMAIL_PASSWORD=
        EMAIL_HOST=
        
        # === Database ===
        DATABASE_NAME=
        DATABASE_USER=
        DATABASE_PASSWORD=
        DATABASE_HOST=
        DATABASE_PORT=
        
        DJANGO_SUPERUSER_EMAIL=
        DJANGO_SUPERUSER_PASSWORD=
  

3. Run the following command to run server:
      console
    make docker-up
   
4. Enjoy Test Tracker features.

## <a name="tests">Tests</a>

1. Run the following command to run tests:
      console
    make tests
   
2. Run the following command to run e2e tests:
      console
    make e2e
   