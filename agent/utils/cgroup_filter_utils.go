package utils

import (
	"strings"

	"github.com/Kevin-sa/ebpf-supply-chain/agent/global"
)

func CgroupIdFilter(hookCgroupId uint64, hookComm string) bool {
	if global.CgroupId == 0 {
		initCgroupId(hookCgroupId, hookComm)
	}

	if global.CgroupId != 0 {
		return global.CgroupId == hookCgroupId
	}
	return false
}

func initCgroupId(hookCgroupId uint64, hookComm string) {
	if strings.HasPrefix(hookComm, "ebpf-supply-cha") || hookComm == "ebpf-supply-cha" {
		global.CgroupId = hookCgroupId
	}
}
