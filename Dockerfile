FROM python:3-stretch as build

WORKDIR /opt/kubones
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt && pip install pylint
COPY /k8s /tmp/k8s/

FROM python:3.7.0-alpine3.8
ARG KUBECTL_VERSION=1.14.4

ENV TEMPLATES=/tmp/k8s/

WORKDIR /opt/kubones
COPY --from=build /root/.cache /root/.cache
COPY --from=build /opt/kubones/requirements.txt .
COPY --from=build /tmp/k8s/ /tmp/k8s

RUN pip install --no-cache-dir -r requirements.txt \
    && apk --no-cache update \
    && apk --no-cache --update add git openssh ca-certificates curl coreutils gnupg bash alpine-sdk xz \
    # update certs because they don't come with alpine out of the box
    && update-ca-certificates \
    # install AWS CLI
    && pip install awscli \
    && cd /tmp \
    # install kubectl
    && curl -LO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl 

COPY --from=build /opt/kubones .

ENTRYPOINT ["python","/opt/kubones/src/main.py"]