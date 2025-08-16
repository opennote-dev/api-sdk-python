from opennote import OpennoteClient
from os import getenv
from json import dumps

SEPERATOR = "================================\n"
client = OpennoteClient(api_key=getenv("OPENNOTE_API_KEY"))

journals_response = client.journals.list()

print(SEPERATOR)
print("Set of Journals:")
print(dumps(journals_response.model_dump(), indent=4))
print(SEPERATOR)

if journals_response.success:
    first_content = client.journals.content(journals_response.journals[0].id)
    print(SEPERATOR)
    print("First Journal Content:")
    print(dumps(first_content.model_dump(), indent=4))
    print(SEPERATOR)
