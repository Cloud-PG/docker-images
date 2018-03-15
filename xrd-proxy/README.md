# USAGE

## Local stack deployment with docker compose: Origin+Cache+CacheRedirector

You need to first install [docker-compose](https://docs.docker.com/compose/install/#install-compose).
Then run use the docker-compose.yml file provided to bring up locally:
* an origin server with config in config/xrd_test_origin.conf
* a file cache server with config in config/xrd_test.conf
* a file cache redirector with config in config/xrd_test-redir.conf

The command for bringing the full stack up is:
```
/usr/local/bin/docker-compose up
```

You should see now something like:
```
Creating xrdproxy_origin_1     ... done
Recreating xrdproxy_cache_1 ...
Recreating xrdproxy_cache_1 ... done
Attaching to xrdproxy_origin_1, xrdproxy_redirector_1, xrdproxy_cache_1
origin_1      | 2018-03-15 08:49:47,319 Starting server:
origin_1      |  proxy: False
origin_1      |  redirector: False
origin_1      |  config: /etc/xrootd/xrd_test_origin.conf
origin_1      |  cache host: 0.0.0.0
origin_1      |  redirector host: 0.0.0.0
origin_1      |  origin host: 0.0.0.0
origin_1      |  cache xrootd port: 1094
origin_1      |  redirector xrootd port: 1094
origin_1      |  origin xrootd port: 1094
origin_1      |  cache cmsd port: 1213
origin_1      |  redirector cmsd port: 1213
origin_1      | 2018-03-15 08:49:47,319 Using configuration file: /etc/xrootd/xrd_test_origin.conf
origin_1      | 2018-03-15 08:49:47,319 Starting cmsd daemon:
origin_1      |  sudo -u xrootd /usr/bin/cmsd -l /var/log/xrootd/cmsd.log -c/etc/xrootd/xrd_test_origin.conf
origin_1      | 2018-03-15 08:49:47,321 cmsd daemon started!
origin_1      | 2018-03-15 08:49:47,321 Starting xrootd daemon:
origin_1      |  sudo -u xrootd /usr/bin/xrootd -l /var/log/xrootd/xrd.log -c/etc/xrootd/xrd_test_origin.conf
origin_1      | 2018-03-15 08:49:47,323 xrootd daemon started!
origin_1      | 2018-03-15 08:49:47,326  * Running on http://0.0.0.0:8081/ (Press CTRL+C to quit)
cache_1       | 2018-03-15 08:49:47,388 Starting server:
cache_1       |  proxy: False
cache_1       |  redirector: False
cache_1       |  config: /etc/xrootd/xrd_test.conf
cache_1       |  cache host: 0.0.0.0
cache_1       |  redirector host: 0.0.0.0
cache_1       |  origin host: 0.0.0.0
cache_1       |  cache xrootd port: 1094
redirector_1  | 2018-03-15 08:49:47,388 Starting server:
cache_1       |  redirector xrootd port: 1094
redirector_1  |  proxy: False
cache_1       |  origin xrootd port: 1094
redirector_1  |  redirector: False
cache_1       |  cache cmsd port: 1213
redirector_1  |  config: /etc/xrootd/xrd_test_redir.conf
cache_1       |  redirector cmsd port: 1213
redirector_1  |  cache host: 0.0.0.0
cache_1       | 2018-03-15 08:49:47,389 Using configuration file: /etc/xrootd/xrd_test.conf
redirector_1  |  redirector host: 0.0.0.0
cache_1       | 2018-03-15 08:49:47,389 Starting cmsd daemon:
redirector_1  |  origin host: 0.0.0.0
cache_1       |  sudo -u xrootd /usr/bin/cmsd -l /var/log/xrootd/cmsd.log -c/etc/xrootd/xrd_test.conf
redirector_1  |  cache xrootd port: 1094
redirector_1  |  redirector xrootd port: 1094
redirector_1  |  origin xrootd port: 1094
redirector_1  |  cache cmsd port: 1213
redirector_1  |  redirector cmsd port: 1213
redirector_1  | 2018-03-15 08:49:47,389 Using configuration file: /etc/xrootd/xrd_test_redir.conf
redirector_1  | 2018-03-15 08:49:47,389 Starting cmsd daemon:
redirector_1  |  sudo -u xrootd /usr/bin/cmsd -l /var/log/xrootd/cmsd.log -c/etc/xrootd/xrd_test_redir.conf
redirector_1  | 2018-03-15 08:49:47,390 cmsd daemon started!
redirector_1  | 2018-03-15 08:49:47,390 Starting xrootd daemon:
redirector_1  |  sudo -u xrootd /usr/bin/xrootd -l /var/log/xrootd/xrd.log -c/etc/xrootd/xrd_test_redir.conf
cache_1       | 2018-03-15 08:49:47,391 cmsd daemon started!
cache_1       | 2018-03-15 08:49:47,391 Starting xrootd daemon:
cache_1       |  sudo -u xrootd /usr/bin/xrootd -l /var/log/xrootd/xrd.log -c/etc/xrootd/xrd_test.conf
redirector_1  | 2018-03-15 08:49:47,392 xrootd daemon started!
cache_1       | 2018-03-15 08:49:47,393 xrootd daemon started!
redirector_1  | 2018-03-15 08:49:47,394  * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
cache_1       | 2018-03-15 08:49:47,395  * Running on http://0.0.0.0:8888/ (Press CTRL+C to quit)
```

## Running by hand

Just put your xrootd config file in $PWD/config:/etc/xrootd

```bash
# with your xrd_cache.conf on $PWD/config
sudo docker run --rm --privileged -p 32294:32294 -p 31113:31113 -v $PWD/config:/etc/xrootd cloudpg/xrootd-proxy --config /etc/xrootd/xrd_test.conf
```
*Remember:* to expose the ports indicated in your config file. In the case of config/xrd_test.conf are: 32294, 31113

*Remember2:* file cached will be put on /data/xrd, so you may want to mount your storage backend there

Logs are stored in:
```
/var/log/xrootd/xrd.log
/var/log/xrootd/cmsd.log
```

An health check is available on:
```bash
# response 0 everything running, response 1 something went wrong
curl <container_ip>/check_health
```

In case of response 1, with `docker logs` you can see a log dump of the crashed daemon.


## Available options

* `--nogrid`: avoid grid CAs installation
* `--health_port`: port for healthcheck process listening, type=int, default=80
