# FROM python:3.6.8-alpine
FROM python:3-onbuild

ENV FLASK_APP hello.py

EXPOSE 5000
# ENTRYPOINT ["./boot.sh"]

# run the application
CMD ["python", "./hello.py"]

