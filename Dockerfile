FROM python:3.9-alpine

# Add your application
COPY ./script.py /app/script.py

# Copy and enable your CRON task
COPY ./cronjob /app/cronjob
COPY ./.env /app/.env
RUN crontab /app/cronjob

# Create empty log (TAIL needs this)
RUN touch /tmp/out.log
RUN apk add --no-cache tzdata
RUN pip3 install requests
RUN pip3 install python-dotenv
ENV TZ=Europe/Amsterdam

# Start TAIL - as your always-on process (otherwise - container exits right after start)
CMD crond && tail -f /tmp/out.log