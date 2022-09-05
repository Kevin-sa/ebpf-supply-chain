package service

import 	"github.com/kevinsa/ebpf-supply-chain/service/syswrite"

type SysWriteProbe struct {
	EventModules
}

func (this *SysWriteProbe) Start() error {
	syswrite.Execute()
	return nil
}

func init() {
	mod := &SysWriteProbe{}
	mod.name = "SysWriteProbe"
	Register(mod)
}