package main

import (
	"fmt"
	"os"
	"os/signal"
	"rulex-target-test-server/server"
	"syscall"
)

func main() {
	signalCh := make(chan os.Signal, 1)
	signal.Notify(signalCh, syscall.SIGINT, syscall.SIGTERM)

	fmt.Println("Server is running. Press Ctrl+C to exit.")
	go server.StartTcpServer()
	go server.StartUdpServer()
	go server.StartHttpServer()
	// 阻塞等待信号
	sigReceived := <-signalCh
	fmt.Printf("Received signal: %v\n", sigReceived)

	// 在这里添加你的清理逻辑，然后退出程序
	fmt.Println("Shutting down...")
}
