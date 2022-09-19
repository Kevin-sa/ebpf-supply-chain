// +build ignore

#include "common.h"
#include "bpf_helpers.h"
#include "bpf_tracing.h"

char __license[] SEC("license") = "Dual MIT/GPL";


struct event {
    u32 pid;
    u8 comm[16];
    u8 host[80];
};



struct {
    // __uint(type, BPF_MAP_TYPE_RINGBUF);
    // __uint(max_entries, 256 * 1024 /* 256 KB */);
    __uint(type, BPF_MAP_TYPE_PERF_EVENT_ARRAY);
} events SEC(".maps");

struct event *unused __attribute__((unused));

SEC("uprobe/getaddrinfo")
int getaddrinfo_return(struct pt_regs *ctx)
{   
    struct event event = {};

    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;
    u32 tid = (u32)pid_tgid;
    
    bpf_probe_read(&event.host, sizeof(event.host),
                       (void *)PT_REGS_PARM1(ctx));
    bpf_get_current_comm(&event.comm, 16);
    event.pid = pid;
    bpf_perf_event_output(ctx, &events, BPF_F_CURRENT_CPU, &event, sizeof(event));

    return 0;

}