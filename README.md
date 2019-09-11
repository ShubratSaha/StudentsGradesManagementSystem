# StudentsGradesManagementSystem
This project was designed to develop REST APIs using Django which serve as a backend for a front end for handling grades of students of an institution. The project is then deployed in the Amazon EC2 instance.

# Steps to execute the project:
1. Install Postman from https://www.getpostman.com/downloads/.
2. Signin to AWS Management Console.
3. Create an Ubuntu 2016 EC2 instance. Enable the ports for HTTP and HTTPS protocol. Install python3, python3-pip, mysql-server, django(1.9.2), djangorestframework(3.3.3), libmysqlclient-dev and mysqlclient.
4. Move this project to the EC2 instance using FileZilla or WinSCP.
5. Create a database with name of your choice.
6. Change the Database Name, UserName and Password as per your MySQL in the settings.py file.
7. Execute django commands to migrate the models into the database and create a superuser.
8. Run the django server at port 80.
8. Use the IP Address of the EC2 instance to access the admin page and to make API requests using Postman application.
