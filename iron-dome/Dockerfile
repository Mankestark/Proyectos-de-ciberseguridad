# Docker File Sistema Debian para monitorizar
# con python3.12 instalado.
ARG APP="irondome.py"
ARG APPLOG="/var/log/irondome.log"
FROM debian:bullseye-slim
RUN set -x -e && apt update && \
    apt -y install procps net-tools sysstat \
    python3-magic python3-psutil python3-watchdog
COPY --chmod=700 irondome.init /etc/init.d/irondome
WORKDIR /usr/src
COPY --chmod=700 irondome.sh ./
COPY --chmod=755 initenv.sh ./
COPY ironaux.py irondome.py ./
#COPY ${APP} requirements.txt .
RUN set -x -e && update-rc.d -f irondome defaults && \
#    python -m pip install -q -r requirements.txt && \
    mkdir /data

ENTRYPOINT set -x -e && bash /usr/src/initenv.sh && \
    service irondome start && sleep 0.5 && \
    bash -c "[ -f /var/log/irondome.log ] && \
        tail -f /var/log/irondome.log || tail -f /var/log/irondome-out.log"
#CMD bash


