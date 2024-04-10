# RC59 configs

A layer for adding configurations to RC59 Fedora Remixes. It's based on the
config layer from UBlue.

## Usage

Add this to your Containerfile to copy the rules over:

```Dockerfile
COPY --from=ghcr.io/ublue-os/config:latest /files/ublue-os/udev-rules /
COPY --from=ghcr.io/ublue-os/config:latest /files/ublue-os/update-services /
```

Or if you prefer to install via an RPM package:

```Dockerfile
COPY --from=ghcr.io/ublue-os/config:latest /rpms/ublue-os-udev-rules.noarch.rpm /
COPY --from=ghcr.io/ublue-os/config:latest /rpms/ublue-os-update-services.noarch.rpm /
RUN rpm -ivh /ublue-os-udev-rules.noarch.rpm
RUN rpm -ivh /ublue-os-update-services.noarch.rpm
```

Additionally, there is support for building custom RPMs:

```Dockerfile
COPY --from=ghcr.io/ublue-os/config:latest /build /tmp/build
COPY justfile /tmp/build/ublue-os-just/justfile
RUN /tmp/build/ublue-os-just/build.sh
RUN rpm -ivh /tmp/ublue-os/rpmbuild/RPMS/noarch/ublue-os-just-*.noarch.rpm
```

## Automatic updates

- Background flatpak updates
- Background rpm-ostree updates

## Verification

These images are signed with sisgstore's cosign. You can verify the signature by
downloading the `cosign.pub` key from this repo and running the following
command:

```sh
cosign verify --key cosign.pub ghcr.io/ublue-os/config
```
