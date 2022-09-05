package service

import "fmt"

var modules = make(map[string]Modules)

func Register(p Modules) {
	if p == nil {
		panic("Register probe is nil")
	}
	name := p.Name()
	if _, dup := modules[name]; dup {
		panic(fmt.Sprintf("Register called twice for probe %s", name))
	}
	modules[name] = p
}

func GetModules() map[string]Modules {
	return modules
}
