# Notes
This project aims for a specific use case for my University's Wi-Fi that implements Microsoft's Single Sign-On (SSO). You can adjust the script to suit your desire.
The script is designed to run on Linux, especially with `NetworkManager` as the network management system. I'm using NM dispatcher to handle the authentication pending event to re-authenticate after a while.

# Using the script
This project utilize [`uv`](https://docs.astral.sh/uv/), an extremely fast Python package and project manager.
You can synchronize the `uv` environment by:
```bash
uv sync
```

Then source the environment:
```bash
source .venv/bin/activate
```
The python version that I'm using is 3.10.2, you can modify it in the `.python-version`
