# USAGE

```
# with your xrd_cache.conf on $PWD/config
sudo docker run --rm --privileged -p 32294:32294 -p 31113:31113 -v $PWD/config:/etc/xrootd cloudpg/xrootd-proxy --config /etc/xrootd/xrd_test.conf
```
*Remember* to expose the ports indicated in your config file. In the case of config/xrd_test.conf are: 32294, 31113
*Remember2* file cached will be put on /data/xrd, so you may want to mount your storage backend there

Logs are stored in: 
```
/var/log/xrootd/xrd.log
/var/log/xrootd/cmsd.log
```

An health check is available on:
```
# response 0 everything running, response 1 something went wrong
curl <container_ip>/check_health
```

In case of response 1, with `docker logs` you can see a log dump of the crashed daemon.