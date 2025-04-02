FROM fedora:41

RUN dnf update -y
RUN dnf install -y rpm-build rpm-devel rpmlint rpmdevtools
RUN dnf install -y make golang

RUN mkdir /out

WORKDIR /root/rpmbuild

RUN rpmdev-setuptree

COPY wrapper.sh .
COPY tapir-edge.spec ./SPECS/
COPY tapir-edm.service ./SOURCES
COPY tapir-pop.service ./SOURCES
COPY tapir-renew.service ./SOURCES
COPY tapir-edge.sysusers ./SOURCES
COPY changelog ./SOURCES

CMD ["./wrapper.sh"]
