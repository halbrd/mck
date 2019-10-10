# mck

`mck` will find music recursively in the directory(ies) you specify, and can perform automated organization and quality checks, invoke [spek](https://github.com/alexkay/spek) for manual spectrographic quality checking, and invoke [ffmpeg](https://www.ffmpeg.org/download.html) to convert them to `m4a`, `mp3`, or `flac` with sensible default settings.

## Operations

### check

```
mck check <path/to/music>
```

For each folder containing audio, ensure:

* the folder is named in the format "Artist Name -- Album Name"
* a `cover.jpg` exists
* no other non-audio files exist, except in an `extras` directory

For each audio file, ensure:

* the bitrate listed in the metadata is over 200 KB/s

### spek

> Requires `spek` to be installed

```
mck spek <path/to/music>
```

### convert

> Requires `ffmpeg` to be installed

```
mck convert <path/to/music> [--output-format <fmt>]
```

Supported formats: `m4a`, `mp3`, `flac`. Default: `m4a`.

## Options

### `--select-formats`

```
mck <action> <path/to/music> --select-formats <fmt1> [<fmt2> ...]
```

Specify audio formats to select as inputs to the script. Must be a subset or equal to the supported formats. This option can be applied to any operation. Files with other formats (other than `cover.jpg` and those in `extras`) are treated as unexpected files.
