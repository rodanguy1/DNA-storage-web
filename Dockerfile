FROM alpine:3.7
#todoL make sure that alpine is ok for our libraries
# Update
WORKDIR    .

COPY requirements.txt  .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install app dependencies
RUN pip install Flask

COPY / ./

EXPOSE  8000
CMD ["python", "/my_app.py", "-p 8000"]