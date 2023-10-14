package service

import "github.com/Kevin-sa/ebpf-supply-chain/agent/service/socket"

type SocketProbe struct {
	EventModules
}

func (this *SocketProbe) Start() error {
	socket.Execute()
	return nil
}

func init() {
	mod := &SocketProbe{}
	mod.name = "SocketProbe"
	Register(mod)
}
