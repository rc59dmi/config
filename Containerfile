FROM registry.fedoraproject.org/fedora:latest AS builder

RUN dnf install --disablerepo='*' --enablerepo='fedora,updates' --setopt install_weak_deps=0 --nodocs --assumeyes rpm-build systemd-rpm-macros

ADD files/etc/rpm-ostreed.conf /tmp/rc59dmi/update-services/etc/rpm-ostreed.conf
ADD files/usr/etc/systemd /tmp/rc59dmi/update-services/usr/etc/systemd
ADD files/usr/lib/systemd /tmp/rc59dmi/update-services/usr/lib/systemd

ADD files/usr/etc/containers /tmp/rc59dmi/signing/usr/etc/containers
ADD files/usr/etc/pki /tmp/rc59dmi/signing/usr/etc/pki

RUN mkdir -p /tmp/rc59dmi/rpmbuild/SOURCES
RUN tar cf /tmp/rc59dmi/rpmbuild/SOURCES/rc59dmi-update-services.tar.gz -C /tmp rc59dmi/update-services
RUN tar cf /tmp/rc59dmi/rpmbuild/SOURCES/rc59dmi-signing.tar.gz -C /tmp rc59dmi/signing

ADD rpmspec/*.spec /tmp/rc59dmi

RUN rpmbuild -ba \
  --define '_topdir /tmp/ublue-os/rpmbuild' \
  --define '%_tmppath %{_topdir}/tmp' \
  /tmp/ublue-os/*.spec

RUN mkdir /tmp/rc59dmi/{files,rpms}

# Dump a file list for each RPM for easier consumption
RUN \
  for RPM in /tmp/rc59dmi/rpmbuild/RPMS/*/*.rpm; do \
  NAME="$(rpm -q $RPM --queryformat='%{NAME}')"; \
  mkdir "/tmp/rc59dmi/files/${NAME}"; \
  rpm2cpio "${RPM}" | cpio -idmv --directory "/tmp/rc59dmi/files/${NAME}"; \
  cp "${RPM}" "/tmp/rc59dmi/rpms/$(rpm -q "${RPM}" --queryformat='%{NAME}.%{ARCH}.rpm')"; \
  done

FROM scratch

# Copy build RPMs
COPY --from=builder /tmp/rc59dmi/rpms /rpms
# Copy dumped RPM content
COPY --from=builder /tmp/rc59dmi/files /files
