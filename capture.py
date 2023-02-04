import time
from PIL import Image
from playwright.sync_api import sync_playwright
from ffmpeg import FFmpeg
from tempfile import NamedTemporaryFile

def image_crop(img):
    transparent_border = img.convert("RGBa").getbbox()
    return(img.crop(transparent_border))

def image_capture(url, width, height, fn="image.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
          viewport={"width": width/2, "height": height/2},
          device_scale_factor=2
        )
        page = context.new_page()
        page.goto(url)
        page.inner_html("canvas")
        with NamedTemporaryFile(suffix=".png") as fp:
            page.screenshot(path=fp.name, omit_background=True)
            img = Image.open(fp.name)
            img = image_crop(img)
            img.save(fn)

def video_capture(url, width, height, duration=10, fps=60, padding=5, fn="video.mp4"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": width+padding, "height": height+padding},
            record_video_dir="./",
            record_video_size={"width": width+padding, "height": height+padding}
        )
        page = context.new_page()
        page.goto(url)
        page.inner_html("canvas")
        time.sleep(duration+1)
        page.close()
        with NamedTemporaryFile(suffix=".webm") as fp:
            page.video.save_as(fp.name)
            page.video.delete()
            ffmpeg = (
                FFmpeg()
                .option("y")
                .option("an")
                .option("sn")
                .option("dn")
                .input(fp.name)
                .output(
                    fn,
                    {"codec:v": "libx264"},
                    vf=f"crop={width}:{height}:0:0",
                    preset="veryslow",
                    crf=24,
                    ss=1,
                    t=duration,
                    r=fps,
                    map_metadata=-1
                )
            )
            ffmpeg.execute()