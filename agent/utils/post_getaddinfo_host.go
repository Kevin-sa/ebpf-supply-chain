package utils

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/Kevin-sa/ebpf-supply-chain/agent/global"
)

type DnsHookInfoReq struct {
	Type     string `json:"type"`
	Package  string `json:"package"`
	Version  string `json:"version"`
	Describe string `json:"describe"`
	Comm     string `json:"comm"`
	Pid      uint32 `json:"pid"`
	Host     string `json:"host"`
}

func PostDnsHookInfo(comm string, host string, pid uint32) {

	dnsHookInfoReq := DnsHookInfoReq{
		Type:     "dns",
		Package:  global.GlobalPackageName,
		Version:  global.GlobalPackageVersion,
		Describe: "getaddrinfo",
		Comm:     comm,
		Pid:      pid,
		Host:     host,
	}

	data, err := json.Marshal(&dnsHookInfoReq)
	if err != nil {
		panic(err)
	}

	client := &http.Client{}
	req := bytes.NewBuffer(data)
	request, _ := http.NewRequest("POST", "http://172.17.0.1:8080/hook/dns", req)
	request.Header.Set("Content-type", "application/json")
	response, _ := client.Do(request)
	if response.StatusCode == 200 {
		body, _ := ioutil.ReadAll(response.Body)
		log.Println(string(body))
	}
}
