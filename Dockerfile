# Install the base requirements for the app.

RUN gh repo clone eeroolli/SalsaAnnotation
WORKDIR /SalsaAnnotation
RUN pip install -r ./env/requirements.txt
