package service

import 	"github.com/kevinsa/ebpf-supply-chain/service/sysopen"

type SysopenProbe struct {
	EventModules
}

func (this *SysopenProbe) Start() error {
	sysopen.Execute()
	return nil
}

func init() {
	mod := &SysopenProbe{}
	mod.name = "SysopenProbe"
	Register(mod)
}