# Install with Ansible

## Requirements

- OS: Centos7
- Port: one open service port
- Valid grid host certifate
- Valid service certificate that is able to read from AAA (/etc/grid-security/xrd/xrdcert.pem, /etc/grid-security/xrd/xrdkey.pem)

## XCache playbook

Have ansible installed and download the xcache role.

``` bash
sudo yum install ansible
ansible-galaxy install dciangot.xcache
```

Then run the playbook with the your preferred options. You can find the complete list of options [here](#ansible-variables)

``` bash
ansible-playbook /etc/ansible/roles/dciangot.xcache/tests/test.yml --extra-vars "metric_sitename=MYSITE elastic_password=foo ETC..."
```

## Ansible variables

Below you can find the available ansible configuration variables with the corresponding defualt value and description

``` yaml
BLOCK_SIZE: 512k # size of the file block used by the cache
CACHE_LOG_LEVEL: info # server log level
CACHE_PATH: /data/xrd # folder for cached files
CACHE_RAM_GB: 12 # amount of RAM for caching in GB. Suggested ~50% of the total
HI_WM: "0.9" # higher watermark of used fs space
LOW_WM: "0.8" # lower watermark of used fs space
N_PREFETCH: "0" # number of blocks to be prefetched
ORIGIN_HOST: origin # hostname or ip adrr of the origin server
ORIGIN_XRD_PORT: "1094" # xrootd port to contact origin on
REDIR_HOST: xcache-service # hostname or ip adrr of the cache redirector
REDIR_CMSD_PORT: "31213" # cmsd port of the cache redirector
metricbeat_polltime: 60s # polling time of the metricbeat sensor
metric_sitename: changeme # sitename to be displayed for monitoring
elk_endpoint: localhost:9000 # elasticsearch endpoint url
elastic_username: dodas # elasticsearch username
elastic_password: testpass # elasticsearch password
```