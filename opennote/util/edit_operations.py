from opennote.types.block_types import *
from opennote.types.api_types import *
from typing import List, Optional

def create_block(
    block: BaseBlock,
    reference_id: Optional[str] = None,
    position: Position = Position.AFTER
) -> CreateNodeOperation:
    node = block.to_node()
    
    return CreateNodeOperation(
        type="create_node",
        nodeType=node["type"],
        params=node["params"],
        referenceId=reference_id,
        position=position.value if isinstance(position, Position) else position
    )

def update_block(
    block_id: str,
    block: BaseBlock
) -> UpdateNodeOperation:
    node = block.to_node()
    return UpdateNodeOperation(
        type="update_node",
        nodeId=block_id,
        node=node
    )


def delete_block(node_id: str) -> DeleteNodeOperation:
    return DeleteNodeOperation(
        type="delete_node",
        nodeId=node_id
    )

##################################
# Example creation helpers
##################################
def make_paragraph(text: str, reference_id: Optional[str] = None) -> CreateNodeOperation:
    """Quickly create a paragraph operation."""
    block = ParagraphBlock(content=text)
    return create_block(block, reference_id)


def make_heading(level: int, text: str, reference_id: Optional[str] = None) -> CreateNodeOperation:
    """Quickly create a heading operation."""
    block = HeadingBlock(level=level, content=text)
    return create_block(block, reference_id)


def make_code_block(code: str, language: str = "javascript", reference_id: Optional[str] = None) -> CreateNodeOperation:
    """Quickly create a code block operation."""
    block = CustomCodeBlock(code=code, language=language)
    return create_block(block, reference_id)


def make_image(src: str, alt: str = "", reference_id: Optional[str] = None) -> CreateNodeOperation:
    """Quickly create an image operation."""
    block = ImageBlock(src=src, alt=alt)
    return create_block(block, reference_id)


def make_list(items: List[str], ordered: bool = False, reference_id: Optional[str] = None) -> CreateNodeOperation:
    """Quickly create a list operation."""
    list_items = [ListItemBlock(content=text) for text in items]
    if ordered:
        block = OrderedListBlock(items=list_items)
    else:
        block = BulletListBlock(items=list_items)
    return create_block(block, reference_id)
