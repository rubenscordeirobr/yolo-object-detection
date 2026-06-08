import sys
import platform
import torch

def check_sys_info():
    print(sys.executable)
    print("--- Python Information ---")
    print(f"Python Version: {platform.python_version()}")
    print(f"Executable Path: {sys.executable}")

    print(torch.__version__)
    print("PyTorch:", torch.__version__)
    print("CUDA version:", torch.version.cuda)
    print("CUDA available:", torch.cuda.is_available())
    print("GPU count:", torch.cuda.device_count())

    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
    else:
        print("No GPU available, using CPU.")
        #print error with red color
        print("\033[91m" + "Error: No GPU available. Please ensure you have a compatible NVIDIA GPU and the correct CUDA drivers installed." + "\033[0m")
        exit(1)
