package biz

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"
	"github.com/kevinsa/ebpf-supply-chain/global"
	"time"
)

type TaskPypiData struct {
	Mirror  string `json:"mirror"`
	Package string `json:"package"`
	Version string `json:"version"`
	Host    string `json:"host"`
}

type TaskPypi struct {
	ErrorMsg string       `json:"error_msg"`
	Result   int          `json:"result"`
	Data     TaskPypiData `json:"data"`
}

func Execute() {
	/**
	 * 获取task任务然后写入环境变量中
	 * 执行安装命令，安装完成获取
	 */
	for true {
		var command string
		taskpypi := getTaskPypi()
		osEnv(taskpypi.Data.Package, taskpypi.Data.Version)
		if taskpypi.Data.Package != "" && taskpypi.Data.Version != "" {
			command = "python3 -m pip install " + "-i " + taskpypi.Data.Mirror + " " + taskpypi.Data.Package + "==" + taskpypi.Data.Version + " --trusted-host " + taskpypi.Data.Host
			log.Printf("common:%s", command)
			installPackage(command)
			log.Printf("package:%s version:%s installed\n", taskpypi.Data.Package, taskpypi.Data.Version)
		}
		time.Sleep(time.Duration(5) * time.Second)
	}

}

func osEnv(packageName string, packageVersion string) {
	// if err := os.Setenv("PYPI_PACKAGE_NAME", packageName); err != nil {
	// 	log.Fatal(err)
	// }
	// if err := os.Setenv("PYPI_PACKAGE_VERSION", packageVersion); err != nil {
	// 	log.Fatal(err)
	// }
	// currentPackage := os.Getenv("PYPI_PACKAGE")
	// fmt.Println(currentPackage)
	global.GlobalPackageName = packageName
	global.GlobalPackageVersion = packageVersion
}

func installPackage(command string) {
	cmd := exec.Command("/bin/bash", "-c", command)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Fatal(err)
	}

	if err := cmd.Start(); err != nil {
		log.Fatal(err)
		return
	}

	data, err := ioutil.ReadAll(stdout)
	if err != nil {
		log.Fatal(err)
		return
	}

	if err := cmd.Wait(); err != nil {
		fmt.Println("wait:", err.Error())
		return
	}
	log.Printf("[INFO]stdout: %s", data)
}

func getTaskPypi() TaskPypi {
	resp, err := http.Get("http://172.17.0.1:8080/task/pypi")
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	var taskPypi TaskPypi
	err = json.Unmarshal(body, &taskPypi)
	if err != nil {
		log.Fatal(err)
	}
	return taskPypi
}
