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

## [Table of Contents](#table-of-contents)

1.  [Introduction](#introduction)
2.  [Prerequisites](#prerequisites)
3.  [Setup on Your Local Machine](#setup-on-your-local-machine)
4.  [Setup Using Docker](#setup-using-docker)
5.  [Tests](#tests)


## [Introduction](#introduction)

TestTracker allows the Quality Assurance team to manage their test plans, requirements, test cases and test runs in a simple and efficient way. All essential tools to manage your test cases all in one place. 

## [Prerequisites](#prerequisites)

Make sure you have installed all of the following prerequisites on your machine:
- **Git** - [Download & Install Git](https://git-scm.com/downloads). OSX and Linux machines typically have this already installed.
- **Node.js** - [Download & Install Node.js](https://nodejs.org/en/download/) and the pnpm package manager. If you encounter any problems, you can also use this [GitHub Gist](https://gist.github.com/isaacs/579814) to install Node.js.
- **Python3** - [Download & Install Python3](https://www.python.org/downloads/).
- **Poetry** - [Download & Install Poetry](https://python-poetry.org/docs/).
- **Docker** - [Download & Install Docker](https://docs.docker.com/engine/install/). Skip this step if you plan to use your local machine to run Test Tracker.


## [Setup on Your Local Machine](#setup-on-your-local-machine)

1. Clone the repository to a directory of your choice.
2. Create a `.env` file using the following template:

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
    ```bash
    make install
    ```
   
5. Run the following command to setup the server:
    ```bash
    make migrate
    ```
   
6. Run the following command to create a super user:
    ```bash
    make user
    ```
   
7. Run the following command to run server:
    ```bash
    make runserver
    ```
   
8. Open a new terminal tab.
9. Run the following command to run client:
    ```bash
    make runclient
    ```
   
10. Press Click + CTRL on the URL to open the client.
11. Enjoy Test Tracker features.

## [Setup Using Docker](#setup-using-docker)

1. Clone the repository to a directory of your choice.
2. Create a `.env` file using the following template:

    ```env
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
    ```
  

3. Run the following command to run server:
    ```bash
    make docker-up
    ```
   
4. Enjoy Test Tracker features.

## [Tests](#tests)

1. Run the following command to run tests:
    ```bash
    make tests
    ```
   
2. Run the following command to run e2e tests:
    ```bash
    make e2e
    ```
   
