"""
To test, first create a journal on Opennote at https://opennote.com/home and get the Journal ID

This is found in the url, such as https://opennote.com/journals/<JOURNAL_ID>

This is referenced below as JOURNAL_ID ->
"""

JOURNAL_ID = ...

from opennote import OpennoteClient
from os import getenv
from opennote.types.block_types import HeadingBlock, ImageBlock, Position, ParagraphBlock
from opennote.util.edit_operations import create_block, update_block, delete_block

client = OpennoteClient(api_key=getenv("OPENNOTE_API_KEY"))

journal_model = client.journals.editor.model_info(JOURNAL_ID)

last_block = journal_model.model.content[-1]

# Try all the possible edit operations below! 

client.journals.editor.edit(JOURNAL_ID, [
    # create_block(
    #     position=Position.AFTER,
    #     reference_id=last_block.attrs.id,
    #     block=ImageBlock(src="https://contentfs-opennote-us-east-1.s3.us-east-1.amazonaws.com/20250922113116-ce36a32a-d8e8-4102-8f58-ba05311b8553.png", alt="Barry B. Benson")
    # ),
    # update_block(
    #     last_block.attrs.id,
    #     HeadingBlock(level=3, content="Updated Block Through SDK")
    # )
    # delete_block(last_block.attrs.id)
])

print("Done")