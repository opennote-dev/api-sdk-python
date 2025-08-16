from opennote import OpennoteClient
from os import getenv
from json import dumps
import time

client = OpennoteClient(api_key=getenv("OPENNOTE_API_KEY"))

SEPERATOR = "================================\n"

if __name__ == "__main__":
    print(SEPERATOR)
    print("Creating Video...")

    response = client.video.create(
        model="picasso",
        messages=[
            {
                "role": "user",
                "content": "Make a video about the Silk Road"
            }
        ],
        include_sources=True,
        search_for="Silk Road History",
        source_count=5,
        upload_to_s3=True,
        title="The Silk Road",
    )

    print("\nVideo Creation Response:")
    print(dumps(response.model_dump(), indent=4))

    print(SEPERATOR)

    status_check_count = 0
    if response.success:
        while True: 
            print(SEPERATOR)
            print(f"Checking Video Status (#{status_check_count})...")
            status = client.video.status(response.video_id)
            
            print("\n", dumps(status.model_dump(), indent=4))
            print(SEPERATOR)
            if status.status == "pending":
                time.sleep(15)
                continue 
            else: 
                break
    
    print(SEPERATOR)
    print("Video Final Status\n")
    print(dumps(status.model_dump(), indent=4))
    print(SEPERATOR)
