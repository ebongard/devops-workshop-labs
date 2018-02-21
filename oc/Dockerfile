FROM rastasheep/ubuntu-sshd:16.04

RUN apt-get update && apt-get -y install wget

RUN wget --progress=dot:giga -O /tmp/oc.tgz https://github.com/openshift/origin/releases/download/v3.7.1/openshift-origin-client-tools-v3.7.1-ab0f056-linux-64bit.tar.gz && \
    cd /tmp && \
    tar xvfz /tmp/oc.tgz  && \
    cp /tmp/openshift-origin-client-tools-v*/oc /usr/local/bin/oc && \
    rm -rf /tmp/oc.tgz


EXPOSE 22

CMD    ["/usr/sbin/sshd", "-D"]