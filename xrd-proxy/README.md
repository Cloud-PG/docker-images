# HOW TO

Proxy deployment:
`docker run --net host -d cloudpg/xrootd-proxy proxy -redirector_url 193.204.89.76 -cmsd_redirector_port 1213 -xrd_redirector_port 1194`

Redirector deployment:
`docker run --net host -d cloudpg/xrootd-proxy redirector -cmsd_redirector_port 1213 -xrd_redirector_port 1194 -redirector_global 193.204.89.77 -redirector_global_port 1213`
