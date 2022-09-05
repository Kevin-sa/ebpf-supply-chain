package utils

import (
	"bytes"
	"encoding/json"
	"log"
	"io/ioutil"
	"net/http"
	"github.com/kevinsa/ebpf-supply-chain/global"
)

type SysExecHookInfoReq struct {
	Type     string `json:"type"`
	Package  string `json:"package"`
	Version  string `json:"version"`
	Describe string `json:"describe"`
	Comm     string `json:"comm"`
	Pid		 uint32 `json:"pid"`
	Filename    string `json:"filename"`
}


func PostSysExecHookInfo(comm string, filename string, pid uint32) {

	hookInfoReq := SysExecHookInfoReq{
		Type:     "sys_exec",
		Package:  global.GlobalPackageName,
		Version:  global.GlobalPackageVersion,
		Describe: "describe",
		Comm:     comm,
		Pid:	  pid,
		Filename: filename,
	}

	data, err := json.Marshal(&hookInfoReq)
	if err != nil {
		panic(err)
	}

	client := &http.Client{}
	req := bytes.NewBuffer(data)
	request, _ := http.NewRequest("POST", "http://172.17.0.1:8080/hook/sys/exec", req)
	request.Header.Set("Content-type", "application/json")
	response, _ := client.Do(request)
	if response.StatusCode == 200 {
		body, _ := ioutil.ReadAll(response.Body)
		log.Println(string(body))
	}
}
