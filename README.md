# apt-cacher-ng-maintenance
apt-cacher-ng-maintenance

# Motivation
The main Motivation for this Docker/Podman/Container Image was to be able to automate the `apt-cacher-ng` Maintenance Tasks.

These are usually performed by visiting the Web Interface (usually at `acng-report.html`) and triggering the Maintenance Tasks.

Since I am currently experiencing quite a few Issues from Time to Time due to either corrupt or partially downloaded Lists Files (particularly on Ubuntu, to a lower but not zero extent also on Debian), I decided to automate the Maintenance Task.

This is done through the use of Python and Selenium (using the Firefox Driver).

Since Firefox requires quite a few Dependencies in order to run, it was preferable to package everything inside a neat Container.

# Features
- Support Basic Authentication
- Support Custom Port

# Setup
## This Tool
You need to first clone the Common https://github.com/luckylinux/container-build-tools somewhere in your System first, as I didn't want to over-complicate the Setup with `git subtree` or `git submodule`).

Then Symlink the Directory within this Repository to the "includes" Target:
```
git clone https://github.com/luckylinux/container-registry-tools
cd container-registry-tools
ln -s /path/to/container-build-tools includes
```

## apt-cacher-ng TLS Proxy
In order to be able to use Basic Authentication securely, the `apt-cacher-ng` Web Page needs to be accessed via TLS.

Since `apt-cacher-ng` does NOT provide this Feature out-of-the Box, the easiest is just to use a Reverse Proxy (e.g. `caddy`) and let it reverse proxy the Requests.

Refer to [Caddy Install Instructions](https://caddyserver.com/docs/install) for Caddy Installation on the same Host that is running `apt-cacher-ng`.

Then edit `/etc/caddy/Caddyfile` and use something like:
```
# Example and Guide
# https://caddyserver.com/docs/caddyfile/options

# General Options
{
    # (Optional) Debug Mode
    # debug

    # Disable Admin API
    admin off

    # TLS Options
    # (Optional) Disable Certificates Management (only if SSL/TLS Certificates are managed by certbot or other external Tools)
    auto_https disable_certs

    # (Optional) Default SNI
    default_sni apt-cacher-ng.MYDOMAIN
}

localhost {
	reverse_proxy /api/* localhost:9001
}

# (Optional) Only if SSL/TLS Certificates are managed by certbot or other external Tools and Custom Logging is required
apt-cacher-ng.MYDOMAIN.TLD {
    tls /etc/letsencrypt/fullchain.pem /etc/letsencrypt/privkey.pem
    
    log {
	output file /var/log/caddy/access.json {
		roll_size 100MiB
	        roll_keep 5000
	        roll_keep_for 720h
	        roll_uncompressed
	}
    
        format json
    }

    reverse_proxy http://0.0.0.0:3142
}
```

# Build
The Container can simply be built using:
```
./build_container.sh
```

Edit the Options to your liking.

# Run
## Podman Quadlets
As a general Rule, I prefer to have a `.pod` as well as one/several `.container` Files defined separately, even though that is not strictly necessary if only one `.container` File is required (such as in this Case).

Feel free to adapt according to your Liking :wink:.

`apt-cacher-ng-maintenance.pod`:
```
[Pod]
PodName=apt-cacher-ng-maintenance

Network=pasta

[Install]
WantedBy=default.target
```

`apt-cacher-ng-maintenance-app.container`:
```
[Unit]
Description=APT Cacher NG Maintenance Application Container
#Requires=apt-cacher-ng-maintenance-caddy.service
#After=apt-cacher-ng-maintenance-caddy.service

[Service]
Restart=always

[Container]
ContainerName=apt-cacher-ng-maintenance-app

Pod=apt-cacher-ng-maintenance.pod
StartWithPod=true

EnvironmentFile=.env

Environment=ENABLE_INFINITE_LOOP=true

Image=localhost/apt-cacher-ng-maintenance:debian-latest
Pull=missing

# If running as the "Backend" of another Container (e.g. Caddy)
# Network=container:apt-cacher-ng-maintenace-caddy

# Use latest Application Version (Editable)
# Volume=/home/MYUSER/apt-cacher-ng-maintenance/app/maintenance.py:/opt/app/maintenance.py:ro,z
```

Reload Configuration and run Podman Quadlet Generators:
```
systemctl --user daemon-reload
```

Restart Pod and Container(s):
```
systemctl --user restart apt-cacher-ng-maintenance-pod
```

Monitor Logs:
```
journalctl --user -f -xeu apt-cacher-ng-maintenance-app
```
