package service

import "github.com/Kevin-sa/ebpf-supply-chain/agent/service/getaddrinfo"

type GetAddfInfoProbe struct {
	EventModules
}

func (this *GetAddfInfoProbe) Start() error {
	getaddrinfo.Execute()
	return nil
}

func init() {
	mod := &GetAddfInfoProbe{}
	mod.name = "GetAddfInfoProbe"
	Register(mod)
}
