// +build ignore

#include "common.h"
#include "bpf_helpers.h"
#include "bpf_tracing.h"

char __license[] SEC("license") = "Dual MIT/GPL";


struct event
{
    u32 pid;
    u8 comm[16];
    // char filename;
    u8 filename[100];
};


struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024 /* 256 KB */);
} events SEC(".maps");

struct event *unused __attribute__((unused));

SEC("kprobe/bprm_execve")
int kprobe_do_sys_openat2(struct pt_regs *ctx)
{   
    u64 id   = bpf_get_current_pid_tgid();
	u32 tgid = id >> 32;
    struct event *task_info;

    // char file_name[255];
    // long err = bpf_probe_read_user_str(&task_info->filename, sizeof(task_info->filename), (void *)ctx->rdi);
    
    task_info = bpf_ringbuf_reserve(&events, sizeof(struct event), 0);
	if (!task_info) {
		return 0;
	}

    char *filename = (char *)PT_REGS_PARM3(ctx);
    bpf_probe_read(&task_info->filename, sizeof(task_info->filename), filename);


    task_info->pid = tgid;
    bpf_get_current_comm(&task_info->comm, 16);
    bpf_ringbuf_submit(task_info, 0);

    return 0; 
}