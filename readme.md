# Eversports notifier

> This project allows you to run a Docker container that uses a cron job to check for new training sessions online on [Eversports](https://eversports.com/).

## Casus

The goal of this project was to receive an email notification whenever a new training schedule is published on the Eversports platform.

The end result is a script that regularly checks for new training sessions by utilizing a cron job. To minimize the load on the Eversports API, the API is only accessed on specific days and times.

If new training sessions are found, an email is sent to a specified email address to notify that new training sessions are available online.

## Environment variables

To use the script, you need to define several environment variables. Copy the file [.env.example](.env.example) to a file named [.env]().

Next, define the environment variables. Below, we describe what each variable represents.

```
SEND_MAIL=Leave this variable as default, the script will use this variable

EMAIL_SENDER=The email address of the sender
EMAIL_RECEIVER=The email address of the receiver
EMAIL_SUBJECT=The subject of the email
EMAIL_MESSAGE=The message of the email

SMTP_SERVER=The SMTP server address
SMTP_PORT=The SMTP server port
SMTP_USERNAME=The SMTP username
SMTP_PASSWORD=The SMTP password

EVERSPORTS_FACILITY_ID=The Eversports facility id

ALLOWED_DAYS_START=The script is allowed to run starting from the specified day of the month
ALLOWED_DAYS_END=The script is allowed to run until the specified day of the month
ALLOWED_HOURS_START=The script is allowed to run starting from the specified hour of the day
ALLOWED_HOURS_END=The script is allowed to run until the specified hour of the day
```

It is recommended to consult your email provider for the correct SMTP details.

The file [cronjob](cronjob) contains the code that is used for the cron job. You can modify it to control how frequently or infrequently the script is executed. Additionally, you can choose whether to use an output log or not.

## Installation

To facilitate the use of the script, I have created a Dockerfile, which allows running the script within a Docker container.

Follow the steps below to utilize the Dockerfile and start a container.

## 1. change directory

Make sure that you are in the correct directory using your terminal, which should be the root directory of this project.

## 2. build image

To start the container, you first need to build the image using the Dockerfile. You can build the image by using the following command:  

`docker build -t 'eversports-notifier' .`.

### optional exporting the image

If desired, you can also export the image as a .tar file and import the image separately within a Docker manager. Use the following command to export the Docker image:  

`docker save -o eversports-notifier.tar eversports-notifier`.

## 3. run container

You can then use the Docker image to start the container. Start the container using the following command: 

`docker run --name eversports-notifier -it eversports-notifier`.  

The container will now be started, and the script will be executed according to the specified cron job.