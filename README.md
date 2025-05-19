# Opennote Python SDK

This is the Python SDK for the Opennote Video API. [Read the documentation here and see more examples](https://docs.opennote.com/video-api/introduction).

## Installation

```bash
pip install opennote
```

## Usage

```python
from opennote import OpennoteVideoClient

client = OpennoteVideoClient(api_key="your_api_key")

# Create a video
video = client.video.create(
    sections=5,
    model="feynman2",
    messages=[{"role": "user", "content": "Hello, world!"}],
)

# Get the status of a video
status = client.video.status(video.video_id)
```