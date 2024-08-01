
# Test Tracker

## Introduction

TestTracker allows the entire team to manage their test plans, requirements, test cases and test runs in a simple and efficient way. All essential tools to manage your test cases all in one place. 

## Features

<details>
  <summary>Authorization</summary>
  <p>&nbsp;</p>

  Signup

  Login

  Login via Github

  Login via Threefold

  Logout
  
  <p>&nbsp;</p>
</details>

<details>
  <summary>Members</summary>
  <p>&nbsp;</p>

  Invite a member


  Delete a member


  Search for a member
  
  <p>&nbsp;</p>
</details>

<details>
  <summary>Projects</summary>
  <p>&nbsp;</p>

  Create a project

  View Statistics

  View team members

  View Test runs

  View recent activities

  Add new test plan

  Add new test requirments

  Add new test suite

  Add new test run

  Delete a project

  Search for a project

  <p>&nbsp;</p>
</details>

<details>
  <summary>Test Plans</summary>
  <p>&nbsp;</p>

  Create a defaullt test plan

  Create a custom test plan

  Update a test plan

  Delete a test plan

  Search for a test plan
  
  <p>&nbsp;</p>
</details>

<details>
  <summary>Requirment Documents</summary>
  <p>&nbsp;</p>

  Create a requirment document

  Delete a requirment document

  Search for a requirment document
  
  Add a new requirment

  Delete a requirment

  Search for a requirment
  
  <p>&nbsp;</p>
</details>

<details>
  <summary>Test Suites</summary>
  <p>&nbsp;</p>

  Create a test suite
  
  Delete a test suite

  Search for a test suite

  Assign to a test plan

  Add test case section

  Add new test case 

  Add existing test case

  Search for a test case
  
  <p>&nbsp;</p>
</details>

<details>
  <summary>Test runs</summary>
  <p>&nbsp;</p>

  Create a test run

  Delete a test run

  Search for a test run
  
  View test run report

  Involve a team member
  
  <p>&nbsp;</p>
</details>


## Setup

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
      ```console
   user@user-VirtualBox:~$ make install
   ```
5. Run the following command to setup the server:
      ```console
   user@user-VirtualBox:~$ make migrate
   ```
6. Run the following command to create a super user:
      ```console
   user@user-VirtualBox:~$ make user
   ```
7. Run the following command to run server:
      ```console
   user@user-VirtualBox:~$ make runserver
   ```
8. Open a new terminal tab.
9. Run the following command to run client:
      ```console
   user@user-VirtualBox:~$ make runclient
   ```
10. Press Click + CTRL on the URL to open the client.
11. Enjoy Test Tracker features.


## Tests

1. Run the following command to run tests:
      ```console
    user@user-VirtualBox:~$ make tests
   ```
2. Run the following command to run e2e tests:
      ```console
   user@user-VirtualBox:~$ make e2e
   ```