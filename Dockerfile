FROM python:3.12.2-alpine
WORKDIR /usr/src/myapp
RUN python -m pip install jsonschema
COPY test.py .
COPY profiling.py .
ENTRYPOINT ["python3", "profiling.py"]
CMD ["python3", "test.py"]
