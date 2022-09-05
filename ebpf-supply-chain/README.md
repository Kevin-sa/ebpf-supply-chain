```
sudo docker build -t ebpf-supply-chain:v1 .
sudo docker run -d -ti --privileged=true ebpf-supply-chain:v1 /bin/bash
```