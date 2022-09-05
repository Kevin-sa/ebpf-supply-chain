package utils


func CommBytes2S(bs [16]uint8) string {
	ba := []byte{}
	for _, b := range bs {
		if b == 0 {
			continue
		}
		ba = append(ba, byte(b))
	}
	return string(ba)
}

func SysWriteCommBytes2S(bs [30]uint8) string {
	ba := []byte{}
	for _, b := range bs {
		if b == 0 {
			continue
		}
		ba = append(ba, byte(b))
	}
	return string(ba)
}

func ExecFilenameBytes2S(bs [100]uint8) string {
	ba := []byte{}
	startWithLen := 0
	for _, b := range bs {
		if b == 0 {
			continue
		}
		startWithLen += 1
		if startWithLen <= 14 {
			continue
		}
		ba = append(ba, byte(b))
	}
	return string(ba)
}

func FilenameBytes2S(bs [100]uint8) string {
	ba := []byte{}
	for _, b := range bs {
		if b == 0 {
			continue
		}
		ba = append(ba, byte(b))
	}
	return string(ba)
}