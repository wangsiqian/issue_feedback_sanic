FROM kevinanew/python-driver:1.3.8

COPY src/ /opt/app
WORKDIR /opt/app
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"

RUN curl -s http://ip-api.com | grep China > /dev/null && \
    pip install -r requirements.txt --no-cache-dir -i https://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com || \
    pip install -r requirements.txt --no-cache-dir
