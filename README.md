# Opennote Python SDK

This is the Python SDK for the Opennote API. [Read the documentation here and see more examples](https://docs.opennote.com/video-api/introduction).

## Installation

```bash
pip install opennote
```

## Usage

### Videos

```python
from opennote import OpennoteClient

client = OpennoteClient(api_key="your_api_key")

# Create a video
video = client.video.create(
    model="picasso",
    messages=[{"role": "user", "content": "Make a video about the Silk Road"}],
    include_sources=True,
    search_for="Silk Road History",
    source_count=5,
    upload_to_s3=True,
    title="The Silk Road",
)

# Get the status of a video
status = client.video.status(video.video_id)
```

### Journals

```python
from opennote import OpennoteClient

client = OpennoteClient(api_key="your_api_key")

# List all journals
journals_response = client.journals.list()

# Get content of a specific journal
if journals_response.success:
    journal_content = client.journals.content(journals_response.journals[0].id)
```

## Examples

For more detailed examples, see the [examples](./examples) directory.