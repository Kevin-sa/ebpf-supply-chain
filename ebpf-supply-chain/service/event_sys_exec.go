package service

import 	"github.com/kevinsa/ebpf-supply-chain/service/sysexec"

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