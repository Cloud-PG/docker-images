# USAGE

```
# with your xrd_cache.conf on $PWD/config
sudo docker run -v $PWD/config:/etc/xrootd cloudpg/xrootd-proxy --config /etc/xrootd/xrd_cache.conf
```

Logs are stored in: 
```
/var/log/xrootd/xrd.log
/var/log/xrootd/cmsd.log
```