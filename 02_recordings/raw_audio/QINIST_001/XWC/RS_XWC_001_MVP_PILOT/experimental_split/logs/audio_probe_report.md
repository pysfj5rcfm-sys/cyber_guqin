# Audio Probe Report

- ffmpeg_available: true
- afconvert_available: true
- afinfo_available: true
- selected_wav_converter_profile: ffmpeg_pcm_s16le_wav

## Converter Probe Matrix

| converter | profile | command | exit_code | output_exists | output_size | status | stderr_summary |
| --- | --- | --- | ---: | --- | ---: | --- | --- |
| ffmpeg | ffmpeg_pcm_s16le_wav | `/Users/chenyulin/Documents/AIProjects/cyber_guqin/.tools/ffmpeg/ffmpeg -y -i /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a -acodec pcm_s16le 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_ffmpeg_pcm_s16le_wav.wav` | 0 | true | 24236110 | success | ffmpeg version 7.1 Copyright (c) 2000-2024 the FFmpeg developers   built with Apple clang version 13.1.6 (clang-1316.0.21.2.5)   configuration: --prefix=/Volumes/tempdisk/sw --extra-cflags=-fno-stack-check --arch=arm64 --cc=/usr/bin/clang --enable-gpl --enable-libvmaf --enable-libopenjpeg --enable-libopus --enable-libmp3lame --enable-libx264 --enable-libx265 --enable-libvpx --enable-libwebp --enable-libass --enable-libfreetype --enable-fontconfig --enable-libtheora --enable-libvorbis --enable-li |
| afconvert | afconvert_wav_LEI16_48000_positional | `/usr/bin/afconvert /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_wav_LEI16_48000_positional.wav -f WAVE -d LEI16@48000` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |
| afconvert | afconvert_wav_LEI16_44100_positional | `/usr/bin/afconvert /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_wav_LEI16_44100_positional.wav -f WAVE -d LEI16@44100` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |
| afconvert | afconvert_wav_I16_48000_positional | `/usr/bin/afconvert /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_wav_I16_48000_positional.wav -f WAVE -d I16@48000` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |
| afconvert | afconvert_wav_I16_44100_positional | `/usr/bin/afconvert /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_wav_I16_44100_positional.wav -f WAVE -d I16@44100` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |
| afconvert | afconvert_wav_LEI16_48000_options_first | `/usr/bin/afconvert -f WAVE -d LEI16@48000 /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_wav_LEI16_48000_options_first.wav` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |
| afconvert | afconvert_wav_LEI16_44100_options_first | `/usr/bin/afconvert -f WAVE -d LEI16@44100 /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_wav_LEI16_44100_options_first.wav` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |
| afconvert | afconvert_aiff_BEI16_48000_diagnostic | `/usr/bin/afconvert /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_aiff_BEI16_48000_diagnostic.aiff -f AIFF -d BEI16@48000` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |
| afconvert | afconvert_caf_LEI16_48000_diagnostic | `/usr/bin/afconvert /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/experimental_split/logs/converter_probe_outputs/batch01_afconvert_caf_LEI16_48000_diagnostic.caf -f caff -d LEI16@48000` | 1 | false | 0 | failed | Error: ExtAudioFileSetProperty ('cfmt') failed ('fmt?') |

## afinfo Diagnostics

### batch01: `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a`

```text
File:           /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch01.m4a
File type ID:   mp4f
Num Tracks:     1
----
Data format:     2 ch,  48000 Hz, aac  (0x00000000) 0 bits/channel, 0 bytes/packet, 1024 frames/packet, 0 bytes/frame
                no channel layout.
estimated duration: 126.185333 sec
audio bytes: 2019960
audio packets: 5917
bit rate: 128018 bits per second
packet size upper bound: 556
maximum packet size: 556
audio data file offset: 3232
not optimized
audio 6056896 valid frames + 2112 priming + 0 remainder = 6059008
----
```

### batch02: `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch02.m4a`

```text
File:           /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch02.m4a
File type ID:   mp4f
Num Tracks:     1
----
Data format:     2 ch,  48000 Hz, aac  (0x00000000) 0 bits/channel, 0 bytes/packet, 1024 frames/packet, 0 bytes/frame
                no channel layout.
estimated duration: 50.964000 sec
audio bytes: 816466
audio packets: 2391
bit rate: 128053 bits per second
packet size upper bound: 552
maximum packet size: 552
audio data file offset: 3232
not optimized
audio 2446272 valid frames + 2112 priming + 0 remainder = 2448384
----
```

### batch03: `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch03.m4a`

```text
File:           /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch03.m4a
File type ID:   mp4f
Num Tracks:     1
----
Data format:     2 ch,  48000 Hz, aac  (0x00000000) 0 bits/channel, 0 bytes/packet, 1024 frames/packet, 0 bytes/frame
                no channel layout.
estimated duration: 153.406667 sec
audio bytes: 2455463
audio packets: 7193
bit rate: 128013 bits per second
packet size upper bound: 559
maximum packet size: 559
audio data file offset: 3232
not optimized
audio 7363520 valid frames + 2112 priming + 0 remainder = 7365632
----
```

### batch04: `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch04.m4a`

```text
File:           /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch04.m4a
File type ID:   mp4f
Num Tracks:     1
----
Data format:     2 ch,  48000 Hz, aac  (0x00000000) 0 bits/channel, 0 bytes/packet, 1024 frames/packet, 0 bytes/frame
                no channel layout.
estimated duration: 126.377333 sec
audio bytes: 2023242
audio packets: 5926
bit rate: 128031 bits per second
packet size upper bound: 558
maximum packet size: 558
audio data file offset: 3232
not optimized
audio 6066112 valid frames + 2112 priming + 0 remainder = 6068224
----
```

### batch05: `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch05.m4a`

```text
File:           /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch05.m4a
File type ID:   mp4f
Num Tracks:     1
----
Data format:     2 ch,  48000 Hz, aac  (0x00000000) 0 bits/channel, 0 bytes/packet, 1024 frames/packet, 0 bytes/frame
                no channel layout.
estimated duration: 37.033333 sec
audio bytes: 593727
audio packets: 1738
bit rate: 128105 bits per second
packet size upper bound: 532
maximum packet size: 532
audio data file offset: 3232
not optimized
audio 1777600 valid frames + 2112 priming + 0 remainder = 1779712
----
```

### batch06: `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch06.m4a`

```text
File:           /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch06.m4a
File type ID:   mp4f
Num Tracks:     1
----
Data format:     2 ch,  48000 Hz, aac  (0x00000000) 0 bits/channel, 0 bytes/packet, 1024 frames/packet, 0 bytes/frame
                no channel layout.
estimated duration: 43.668000 sec
audio bytes: 699691
audio packets: 2049
bit rate: 128054 bits per second
packet size upper bound: 571
maximum packet size: 571
audio data file offset: 3232
not optimized
audio 2096064 valid frames + 2112 priming + 0 remainder = 2098176
----
```

### batch07: `02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch07.m4a`

```text
File:           /Users/chenyulin/Documents/AIProjects/cyber_guqin/02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001_MVP_PILOT/raw/batch07.m4a
File type ID:   mp4f
Num Tracks:     1
----
Data format:     2 ch,  48000 Hz, aac  (0x00000000) 0 bits/channel, 0 bytes/packet, 1024 frames/packet, 0 bytes/frame
                no channel layout.
estimated duration: 29.716000 sec
audio bytes: 476391
audio packets: 1395
bit rate: 128062 bits per second
packet size upper bound: 536
maximum packet size: 536
audio data file offset: 3232
not optimized
audio 1426368 valid frames + 2112 priming + 0 remainder = 1428480
----
```
