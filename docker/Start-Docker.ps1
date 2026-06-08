docker run --rm -it `
  -e MTX_RTSPTRANSPORTS=tcp `
  -e MTX_WEBRTCADDITIONALHOSTS=127.0.0.1,localhost,192.168.0.0/16 `
  -p 8554:8554 `
  -p 1935:1935 `
  -p 8888:8888 `
  -p 8889:8889 `
  -p 8890:8890/udp `
  -p 8189:8189/udp `
  bluenviron/mediamtx:latest