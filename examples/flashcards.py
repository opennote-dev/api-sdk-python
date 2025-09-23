from opennote import OpennoteClient
from os import getenv
from json import dumps

client = OpennoteClient(api_key=getenv("OPENNOTE_API_KEY"))

flashcards = client.interactives.flashcards.create(set_description="The most important things to know about the Silk Road", count=5)

print("Flashcards:")
print(dumps(flashcards.model_dump(), indent=4))
