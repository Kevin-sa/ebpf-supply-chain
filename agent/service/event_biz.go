package service

import "github.com/Kevin-sa/ebpf-supply-chain/agent/service/biz"

type BizProbe struct {
	EventModules
}

func (this *BizProbe) Start() error {
	biz.Execute()
	return nil
}

func init() {
	mod := &BizProbe{}
	mod.name = "BizProbe"
	Register(mod)
}
