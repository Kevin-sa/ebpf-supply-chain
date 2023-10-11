package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/Kevin-sa/ebpf-supply-chain/agent/service"
)

func main() {
	stopper := make(chan os.Signal, 1)
	signal.Notify(stopper, os.Interrupt, syscall.SIGTERM)
	_, cancelFun := context.WithCancel(context.TODO())

	for _, module := range service.GetModules() {
		go func(module service.Modules) {
			err := module.Start()
			if err != nil {
				fmt.Printf("%v\n", err)
			}
		}(module)
	}

	<-stopper
	cancelFun()
}
