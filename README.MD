# An API endpoint for a decibel sensor

This repository contains a basic HTTP endpoint to fetch information from a decibel sensor sensor like [this one](https://pcbartists.com/product/i2c-decibel-sound-level-meter-module/).

The output is an averaged value and a maximum value in a given poll, in prometheus format.

## Usage:

Install with: `pip install git+https://github.com/OneBlue/dbsensorapi`

Run with: `dbsensorapi [--listen-address <listen-address>] [--listen-port <listen-port>] [--i2c_bus <bus>] [--i2c_address <address>] [--poll-rate <seconds>] [--average-count <count>]`

By default the HTTP server will run on 127.0.0.1:8000, and will us i2c_bus=1, and device_address=0x48.

## Sample output

```
$ curl localhost:8000
dbsensor_average_dba 35.67
dbsensor_max_dba 36.00
```

## Sample systemd unit

```
# /etc/systemd/system/dbsensor.service

[Unit]
Description=dbsensor

[Service]
Type=simple
ExecStart=/usr/local/bin/dbsensorapi 0.0.0.0 9000 --i2c_bus 1
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
```

See [device data sheet](https://pcbartists.com/product-documentation/i2c-decibel-meter-programming-manual/) for more details.
