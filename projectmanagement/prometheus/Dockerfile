# In ./prometheus/Dockerfile
FROM prom/prometheus:latest

LABEL maintainer="mritunjay <a34mritunjaysingh@gmail.com>"

# Copy additional configuration files if needed
# COPY prometheus.yml /etc/prometheus/
# COPY rules/ /etc/prometheus/rules/

USER root
RUN mkdir -p /prometheus && chown -R nobody:nobody /prometheus
USER nobody

ENTRYPOINT [ "/bin/prometheus" ]
CMD [ "--config.file=/etc/prometheus/prometheus.yml", \
      "--storage.tsdb.path=/prometheus", \
      "--web.console.libraries=/usr/share/prometheus/console_libraries", \
      "--web.console.templates=/usr/share/prometheus/consoles" ]