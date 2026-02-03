import os
import sys
import zipfile
import shutil
import requests
from tqdm import tqdm

def download_ffmpeg():
    # Use a mirror or reliable source. Gyan.dev is standard.
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    
    target_zip = "ffmpeg.zip"
    if os.path.exists(target_zip):
        os.remove(target_zip)
        
    print(f"Downloading ffmpeg from {url}...")
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        
        with open(target_zip, 'wb') as f, tqdm(
            desc="Downloading",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
    except Exception as e:
        print(f"Download failed: {e}")
        return False

    print("Extracting...")
    extract_temp = "ffmpeg_temp"
    if os.path.exists(extract_temp):
        shutil.rmtree(extract_temp)
    
    with zipfile.ZipFile(target_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_temp)
        
    # Find bin folder
    ffmpeg_exe = None
    for root, dirs, files in os.walk(extract_temp):
        if "ffmpeg.exe" in files:
            ffmpeg_exe = os.path.join(root, "ffmpeg.exe")
            break
            
    if not ffmpeg_exe:
        print("Could not find ffmpeg.exe in the zip.")
        return False
        
    # Move to ./ffmpeg folder
    target_dir = os.path.join(os.getcwd(), "ffmpeg")
    if os.path.exists(target_dir):
        # Only overwrite if empty or broken? 
        # Actually just overwrite to be safe.
        pass
    else:
        os.makedirs(target_dir)
    
    # Move ffmpeg.exe, ffprobe.exe, ffplay.exe
    src_dir = os.path.dirname(ffmpeg_exe)
    for file in os.listdir(src_dir):
        if file.endswith(".exe"):
            dst_file = os.path.join(target_dir, file)
            shutil.move(os.path.join(src_dir, file), dst_file)
            
    print(f"Installed ffmpeg to {target_dir}")
    
    # Clean up
    if os.path.exists(target_zip):
        os.remove(target_zip)
    if os.path.exists(extract_temp):
        shutil.rmtree(extract_temp)
    return True

if __name__ == "__main__":
    if download_ffmpeg():
        print("FFmpeg setup complete.")
    else:
        sys.exit(1)
