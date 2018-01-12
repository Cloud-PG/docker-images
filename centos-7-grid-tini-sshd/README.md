## CentOS 7 Grid Tini

Base image for several services used in cloud projects.

This image contains an ssh server with an exposed port (22).
It's accesible with the following user and password:

```bash
username: "admin"
password: "passwd"
```

This image has also [tini](https://github.com/krallin/tini), a tiny init for containers. The image will use it as entrypoint.

Info about how to build are in the autogen folder of this repo:
* [https://github.com/krallin/tini-images/tree/master](https://github.com/krallin/tini-images/tree/master)