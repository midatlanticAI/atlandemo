import urllib.request, gzip, shutil, pathlib, hashlib
import sys, os

FILES = {
    "train-images-idx3-ubyte.gz": "https://raw.githubusercontent.com/fgnt/mnist/master/train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz": "https://raw.githubusercontent.com/fgnt/mnist/master/train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz": "https://raw.githubusercontent.com/fgnt/mnist/master/t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz": "https://raw.githubusercontent.com/fgnt/mnist/master/t10k-labels-idx1-ubyte.gz",
}

TARGET = pathlib.Path("data/MNIST/raw")

def sha1(path: pathlib.Path):
    h = hashlib.sha1()
    with open(path, "rb") as fp:
        while True:
            chunk = fp.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()[:8]

def download():
    TARGET.mkdir(parents=True, exist_ok=True)
    for fname, url in FILES.items():
        fpath = TARGET / fname
        if fpath.exists():
            print(f"[✓] {fname} already exists ({sha1(fpath)})")
        else:
            print(f"[↓] Downloading {fname} …")
            urllib.request.urlretrieve(url, fpath)
            print(f"    saved to {fpath} ({sha1(fpath)})")
        # extract
        out_name = fpath.with_suffix("")
        if not out_name.exists():
            print(f"    extracting → {out_name.name}")
            with gzip.open(fpath, "rb") as src, open(out_name, "wb") as dst:
                shutil.copyfileobj(src, dst)
        else:
            print(f"    extracted file exists ({out_name})")

if __name__ == "__main__":
    download()
    print("\n✅ MNIST download + extraction complete →", TARGET.resolve()) 