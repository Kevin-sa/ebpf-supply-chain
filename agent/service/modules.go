package service

type Modules interface {
	// Name 获取当前module的名字
	Name() string

	// Start 启动模块
	Start() error
}

type EventModules struct {
	name string
}

func (this *EventModules) Name() string {
	return this.name
}
