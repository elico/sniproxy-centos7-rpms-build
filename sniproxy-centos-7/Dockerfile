FROM golang:alpine AS build-env
LABEL maintainer "Eliezer Croitoru <ngtech1ltd@gmail.com>"

# Install OS-level dependencies.
RUN apk add --no-cache curl git vim bash wget

# Copy our source code into the container.
RUN mkdir /build / && \
        git clone https://github.com/fangdingjun/sniproxy /build/sniproxy && \
        cd /build/sniproxy && \
	sed -i -e "s@config.yaml@/etc/sniproxy-fang/config.yaml@g" main.go && \
        CGO_ENABLED=0 go build

VOLUME /build

FROM centos:7
LABEL maintainer "Eliezer Croitoru <ngtech1ltd@gmail.com>"

RUN yum install -y gcc gcc-c++ \
                   libtool libtool-ltdl \
                   make cmake \
                   git \
                   pkgconfig \
                   sudo \
                   automake autoconf \
                   yum-utils rpm-build && \
    yum clean all

RUN useradd builder -u 1000 -m -G users,wheel \
   &&  echo "builder ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers \
   &&  echo "# macros" > /home/builder/.rpmmacros \
   &&  echo "%_topdir /home/builder/rpm" >> /home/builder/.rpmmacros \
   &&  echo "%_sourcedir %{_topdir}/SOURCES" >> /home/builder/.rpmmacros \
   &&  echo "%_builddir %{_topdir}/BUILD" >> /home/builder/.rpmmacros \
   &&  echo "%_specdir %{_topdir}/SPECS" >> /home/builder/.rpmmacros \
   &&  echo "%_rpmdir %{_topdir}/RPMS" >> /home/builder/.rpmmacros \
   &&  echo "%_srcrpmdir %{_topdir}/SRPMS" >> /home/builder/.rpmmacros \
   &&  mkdir /home/builder/rpm \
   &&  chown -R builder /home/builder

USER builder

ENV FLAVOR=rpmbuild OS=centos DIST=el7

COPY --from=build-env /build/sniproxy/sniproxy /sniproxy-fang

CMD ["/srv/pkg"]
