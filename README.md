# chatGPT clone
Flask's first project using the ChatGPT API

## Description
A Flask application that mimics ChatGPT by using the OpenAI API. 
It allows creating accounts and logging into the application using a MySQL database.
![image](https://github.com/MaksymiIian/chatGPT-clone/assets/107677787/ab1f8fca-72df-401e-97b4-d11a1a8d1882)

## Database query for table
CREATE TABLE user (
  ID INT NOT NULL AUTO_INCREMENT,
  Login VARCHAR(255) NOT NULL,
  Password VARCHAR(255) NOT NULL,
  Responses_count INT NOT NULL DEFAULT 0,
  PRIMARY KEY(ID)
);

## Python version
Project is created with Python 3.9.13
