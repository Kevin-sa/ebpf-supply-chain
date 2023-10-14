// +build ignore

#include "common.h"
#include "bpf_helpers.h"
#include "bpf_tracing.h"

char __license[] SEC("license") = "Dual MIT/GPL";


// struct ksys_write_event_t {
// 	u32 pid;
// 	u32 count;
// 	u32 fd;
// 	u64 ts;
// 	char buf[20];
// } __attribute__((packed));

struct event {
	u32 pid;
	u32 count;
	u32 fd;
	u64 ts;
    u8 filename[100];
	u8 comm[30];
    u64 cg_id;
};


struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024 /* 256 KB */);
} events SEC(".maps");

struct event *unused __attribute__((unused));

SEC("kprobe/ksys_write")
int kprobe_ksys_write(struct pt_regs *ctx) {

	// int my_pid;
    // asm("%0 = MY_PID ll" : "=r"(my_pid));

	u64 id   = bpf_get_current_pid_tgid();
	u32 tgid = id >> 32;

	struct event *task_info;

	task_info = bpf_ringbuf_reserve(&events, sizeof(struct event), 0);
	if (!task_info) {
		return 0;
	}

    task_info->pid = tgid;
    task_info->fd = PT_REGS_PARM1(ctx);
	task_info->count = PT_REGS_PARM3(ctx);
	task_info->ts = bpf_ktime_get_ns();

    char *filename = (char *)PT_REGS_PARM2(ctx);

    bpf_probe_read(&task_info->filename, sizeof(task_info->filename), filename);
	bpf_get_current_comm(&task_info->comm, 30);

	task_info->cg_id = bpf_get_current_cgroup_id();

	bpf_ringbuf_submit(task_info, 0);
    return 0;
}