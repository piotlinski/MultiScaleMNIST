"""Original MNIST handlers."""
import subprocess
from pathlib import Path
from typing import List

MNIST_URL = "http://yann.lecun.com/exdb/mnist/"
MNIST_KEYS: List[str] = [
    "train-images-idx3-ubyte",
    "train-labels-idx1-ubyte",
    "t10k-images-idx3-ubyte",
    "t10k-labels-idx1-ubyte",
]


def verify_mnist_dir(data_dir: Path, mnist_keys: List[str]):
    """Check if data already downloaded and invoke downloading if needed."""
    if not all([data_dir.joinpath(file).exists() for file in mnist_keys]):
        data_dir.mkdir()
        download_mnist(data_dir=data_dir, mnist_keys=mnist_keys, mnist_url=MNIST_URL)


def download_mnist(data_dir: Path, mnist_keys: List[str], mnist_url: str):
    """Download MNIST dataset."""
    for key in mnist_keys:
        key += ".gz"
        url = (mnist_url + key).format(**locals())
        target_path = data_dir.joinpath(key)
        cmd = f"curl {url} -o {str(target_path)}"
        subprocess.call(cmd)
        cmd = f"gunzip -d {str(target_path)}"
        subprocess.call(cmd)
