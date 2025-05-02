package main

import (
	"fmt"
	"math"
	"net"
	"time"
)

func main() {
	const target = "google.com:80"
	const attempts = 10
	var delays []float64

	fmt.Printf("Started to Jitter  (%d Test):\n", attempts)

	for i := 0; i < attempts; i++ {
		start := time.Now()

		conn, err := net.DialTimeout("tcp", target, 2*time.Second)
		if err != nil {
			fmt.Printf("Connection Error: %v\n", err)
			continue
		}
		conn.Close()

		elapsed := time.Since(start).Seconds() * 1000 // saniyeyi ms'e çeviriyoruz
		delays = append(delays, elapsed)

		fmt.Printf("Test %2d: %.2f ms\n", i+1, elapsed)

		time.Sleep(1 * time.Second)
	}

	jitter := calculateJitter(delays)
	fmt.Printf("\nJitter: %.3f ms\n", jitter)
}

// Jitter = ardışık ölçümler arasındaki farkların ortalaması
func calculateJitter(delays []float64) float64 {
	if len(delays) < 2 {
		return 0
	}

	var sum float64
	for i := 1; i < len(delays); i++ {
		diff := math.Abs(delays[i] - delays[i-1])
		sum += diff
	}
	return sum / float64(len(delays)-1)
}