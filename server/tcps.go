// Copyright (C) 2023 wwhai
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

package server

import (
	"bufio"
	"log"
	"net"
)

func handleConnection(conn net.Conn) {
	defer conn.Close()

	// 创建一个带缓冲的读取器
	reader := bufio.NewReader(conn)

	for {
		// 读取一行数据
		message, err := reader.ReadString('\n')
		if err != nil {
			log.Println("Error reading:", err)
			return
		}

		// 打印接收到的数据
		log.Printf("[TCP Server] Received: %s", message)
	}
}

func StartTcpServer() {
	// 监听端口
	listener, err := net.Listen("tcp", ":6001")
	if err != nil {
		log.Fatal("Error starting the server:", err)
	}

	log.Println("TCP Server listening on [::]:6001")

	for {
		// 等待连接
		conn, err := listener.Accept()
		if err != nil {
			log.Println("Error accepting connection:", err)
			continue
		}
		log.Println(conn.RemoteAddr())

		// 启动一个 goroutine 处理连接
		go handleConnection(conn)
	}
}
