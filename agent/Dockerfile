FROM ebpf-supply-chain:base


RUN apt-get update
RUN apt-get install supervisor


RUN echo "[program:ebpf]" >> /etc/supervisor/conf.d/ebpf.conf \
    && echo "user=root" >> /etc/supervisor/conf.d/ebpf.conf \
    && echo "command=/home/ebpf-supply-chain" >> /etc/supervisor/conf.d/ebpf.conf \
    && echo "stderr_logfile=/var/log/supervisor/ebpf_stderr.log" >> /etc/supervisor/conf.d/ebpf.conf \
    && echo "stdout_logfile=/var/log/supervisor/ebpf_stdout.log" >> /etc/supervisor/conf.d/ebpf.conf \
    && echo "autostart=true" >> /etc/supervisor/conf.d/ebpf.conf \
    && echo "startretries=15" >> /etc/supervisor/conf.d/ebpf.conf

WORKDIR /home
COPY ebpf-supply-chain ./
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
