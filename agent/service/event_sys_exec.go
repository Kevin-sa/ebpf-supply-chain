package service

import "github.com/Kevin-sa/ebpf-supply-chain/agent/service/sysexec"

type SysExecProbe struct {
	EventModules
}

func (this *SysExecProbe) Start() error {
	sysexec.Execute()
	return nil
}

func init() {
	mod := &SysExecProbe{}
	mod.name = "SysExecProbe"
	Register(mod)
}
