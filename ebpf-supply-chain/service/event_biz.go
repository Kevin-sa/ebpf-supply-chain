package service

import 	"github.com/kevinsa/ebpf-supply-chain/service/biz"

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
