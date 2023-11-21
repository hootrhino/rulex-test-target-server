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
	"log"
	"net"
)

func handleUDPConnection(conn *net.UDPConn) {
	defer conn.Close()

	buffer := make([]byte, 1024)

	for {
		// 读取数据
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			log.Println("Error reading:", err)
			return
		}

		// 打印接收到的数据
		log.Printf("[UDP Server] Received from %s: %s", addr.String(), buffer[:n])
	}
}

func StartUdpServer() {
	// 解析地址
	addr, err := net.ResolveUDPAddr("udp", ":6002")
	if err != nil {
		log.Fatal("Error resolving UDP address:", err)
	}

	// 监听UDP连接
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		log.Fatal("Error starting the UDP server:", err)
	}
	defer conn.Close()

	log.Printf("UDP Server listening on %s", conn.LocalAddr().String())

	// 处理UDP连接
	handleUDPConnection(conn)
}
