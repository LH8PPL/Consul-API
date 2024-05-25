FROM python:3.11
EXPOSE 5000
WORKDIR /app
RUN pip install flask requests
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]