FROM python:3.11-slim
RUN apt update && apt-get install -y curl && apt-get install -y python3 && apt-get install -y python3-pip
COPY . .
RUN bash ./install.sh
CMD bash -c "cd bin && . run.sh"
