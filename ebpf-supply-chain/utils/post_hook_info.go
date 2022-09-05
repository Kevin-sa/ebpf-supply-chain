package utils

import (
	"bytes"
	"encoding/json"
	"log"
	"io/ioutil"
	"net/http"
	"os"
	"github.com/kevinsa/ebpf-supply-chain/global"
)

type HookInfoReq struct {
	Type     string `json:"type"`
	Package  string `json:"package"`
	Version  string `json:"version"`
	Describe string `json:"describe"`
	Comm     string `json:"comm"`
	Daddr    string `json:"daddr"`
	Dport    uint16 `json:"dport"`
}

func getEnv(envName string) string {
	return os.Getenv(envName)
}

func PostHookInfo(comm string, daddr string, dport uint16) {

	hookInfoReq := HookInfoReq{
		Type:     "socket",
		Package:  global.GlobalPackageName,
		Version:  global.GlobalPackageVersion,
		Describe: "describe",
		Comm:     comm,
		Daddr:    daddr,
		Dport:    dport,
	}

	data, err := json.Marshal(&hookInfoReq)
	if err != nil {
		panic(err)
	}

	client := &http.Client{}
	req := bytes.NewBuffer(data)
	request, _ := http.NewRequest("POST", "http://172.17.0.1:8080/hook/socket", req)
	request.Header.Set("Content-type", "application/json")
	response, _ := client.Do(request)
	if response.StatusCode == 200 {
		body, _ := ioutil.ReadAll(response.Body)
		log.Println(string(body))
	}
}
