# artblocks-capture
Image and video capture via [playwright](https://github.com/microsoft/playwright)

This uses a headless web browser via playwright to render live code. While the examples use an endpoint from ArtBlocks, it would work for other endpoints or local development purposes.

Note: Video captures are converted to `mp4` format with [ffmpeg](https://ffmpeg.org) with settings optimized for limiting file size (for sharing purposes). Modify for higher quality if desired.

## Install

```
conda env create -f environment.yml
conda activate playwright
playwright install
```

## Examples

```
image_capture("https://generator.artblocks.io/14000091", width=1000, height=1000)
video_capture("https://generator.artblocks.io/14000091", width=1000, height=1000, duration=10, fps=60)
```
