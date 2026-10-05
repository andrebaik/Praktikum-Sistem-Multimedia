sample_rates = [8000, 44100, 48000]
bit_depths = [8, 16, 24]
channels = [1, 2]
durasi = 10

for sr in sample_rates:
    for bit in bit_depths:
        for channel in channels:
            ukuran = sr * (bit / 8) * channel * durasi

            jenis_channel = "Mono" if channel == 1 else "Stereo"

            print(
                sr, "Hz |",
                bit, "bit |",
                jenis_channel, "|",
                ukuran, "byte"
            )
            sample_rates = [8000, 44100, 48000]
            bit_depths = [8, 16, 24]
            channels = [1, 2]
            durasi = 10

for sr in sample_rates:
    for bit in bit_depths:
        for channel in channels:
            ukuran = sr * (bit / 8) * channel * durasi

            jenis_channel = "Mono" if channel == 1 else "Stereo"

            print(
                sr, "Hz |",
                bit, "bit |",
                jenis_channel, "|",
                ukuran, "byte"
            )