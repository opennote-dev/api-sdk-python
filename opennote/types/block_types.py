from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field
from uuid import uuid4
from enum import Enum

def _block_content_to_node(content: Any) -> Any:
    """Convert block content to node format."""
    if isinstance(content, str):
        return {"type": "paragraph", "content": [{"type": "text", "text": content}]}
    elif isinstance(content, ParagraphBlock):
        return {
            "type": "paragraph",
            "attrs": {"id": content.id},
            "content": [{"type": "text", "text": content.content}] if content.content else []
        }
    elif isinstance(content, list):
        return [_block_content_to_node(item) for item in content]
    return content

def _list_item_to_node(item: "ListItemBlock") -> Dict[str, Any]:
    """Convert a ListItemBlock to node format."""
    content = _block_content_to_node(item.content)
    if not isinstance(content, list):
        content = [content]
    return {
        "type": "listItem",
        "attrs": {"id": item.id},
        "content": content
    }

def _table_row_to_node(row: "TableRowBlock") -> Dict[str, Any]:
    """Convert a TableRowBlock to node format."""
    cells = [_table_cell_to_node(cell) for cell in row.cells]
    return {
        "type": "tableRow",
        "attrs": {"id": row.id},
        "content": cells
    }

def _table_cell_to_node(cell: Union["TableCellBlock", "TableHeaderBlock"]) -> Dict[str, Any]:
    """Convert a TableCellBlock or TableHeaderBlock to node format."""
    content = _block_content_to_node(cell.content)
    node_type = "tableHeader" if isinstance(cell, TableHeaderBlock) else "tableCell"
    attrs = {"id": cell.id}
    if cell.colspan and cell.colspan > 1:
        attrs["colspan"] = cell.colspan
    if cell.rowspan and cell.rowspan > 1:
        attrs["rowspan"] = cell.rowspan
    return {
        "type": node_type,
        "attrs": attrs,
        "content": [content] if not isinstance(content, list) else content
    }

def _details_summary_to_node(summary: "DetailsSummaryBlock") -> Dict[str, Any]:
    """Convert a DetailsSummaryBlock to node format."""
    return {
        "type": "detailsSummary",
        "attrs": {"id": summary.id},
        "content": [{"type": "text", "text": summary.text}]
    }

def _details_content_to_node(content: "DetailsContentBlock") -> Dict[str, Any]:
    """Convert a DetailsContentBlock to node format."""
    node_content = [_block_content_to_node(item) for item in content.content]
    return {
        "type": "detailsContent",
        "attrs": {"id": content.id},
        "content": node_content
    }

def _block_to_node_params(block: "BaseBlock") -> List[Any]:
    """
    Convert a block to parameters array for NodeCreators functions.
    Based on the TypeScript NodeCreators implementation.
    """
    # Map block types to their parameter arrays
    if isinstance(block, ParagraphBlock):
        # paragraph: (content?: Fragment | string, attrs?: Record<string, any>)
        return [block.content] if block.content else [""]
    
    elif isinstance(block, HeadingBlock):
        # heading: (level: number, content: Fragment | string, attrs?: Record<string, any>)
        return [block.level, block.content]
    
    elif isinstance(block, BulletListBlock):
        # bulletList: (items: ProseMirrorNode[], attrs?: Record<string, any>)
        items = [_list_item_to_node(item) for item in block.items]
        return [items]
    
    elif isinstance(block, OrderedListBlock):
        # orderedList: (items: ProseMirrorNode[], start: number = 1, attrs?: Record<string, any>)
        items = [_list_item_to_node(item) for item in block.items]
        return [items, block.start]
    
    elif isinstance(block, ListItemBlock):
        # listItem: (content: ProseMirrorNode | Fragment, attrs?: Record<string, any>)
        content = _block_content_to_node(block.content)
        return [content]
    
    elif isinstance(block, BlockquoteBlock):
        # blockquote: (content: Fragment | ProseMirrorNode[], attrs?: Record<string, any>)
        content = _block_content_to_node(block.content)
        return [content]
    
    elif isinstance(block, HorizontalRuleBlock):
        # horizontalRule: (attrs?: Record<string, any>)
        return []
    
    elif isinstance(block, HardBreakBlock):
        # hardBreak: ()
        return []
    
    elif isinstance(block, CustomCodeBlock):
        # customCodeBlock: (code: string, language: string = 'javascript', attrs?: Record<string, any>)
        return [block.code, block.language]
    
    elif isinstance(block, LatexBlock):
        # latex: (latex: string, attrs?: Record<string, any>)
        return [block.latex]
    
    elif isinstance(block, InlineLatexBlock):
        # inlineLatex: (latex: string, attrs?: Record<string, any>)
        return [block.latex]
    
    elif isinstance(block, ImageBlock):
        # image: (src: string, alt?: string, attrs?: Record<string, any>)
        params = [block.src]
        if block.alt is not None:
            params.append(block.alt)
        return params
    
    elif isinstance(block, VideoBlock):
        # video: (src: string, attrs?: Record<string, any>)
        return [block.src]
    
    elif isinstance(block, AudioBlock):
        # audio: (src: string, title?: string, attrs?: Record<string, any>)
        params = [block.src]
        if block.title is not None:
            params.append(block.title)
        return params
    
    elif isinstance(block, YoutubeBlock):
        # youtube: (src: string, width: number = 640, height: number = 480, attrs?: Record<string, any>)
        return [block.src, block.width, block.height]
    
    elif isinstance(block, PDFBlock):
        # pdf: (src: string, width?: number, height?: number, attrs?: Record<string, any>)
        params = [block.src]
        if block.width is not None:
            params.append(block.width)
        if block.height is not None:
            params.append(block.height)
        return params
    
    elif isinstance(block, DOCXBlock):
        # docx: (src: string, width?: number, height?: number, attrs?: Record<string, any>)
        params = [block.src]
        if block.width is not None:
            params.append(block.width)
        if block.height is not None:
            params.append(block.height)
        return params
    
    elif isinstance(block, DesmosBlock):
        # desmos: (equations: string = '', attrs?: Record<string, any>)
        return [block.equations]
    
    elif isinstance(block, ChartBlock):
        # chart: (chartType: string = 'bar', title: string = 'Chart Title', attrs?: Record<string, any>)
        return [block.chartType.value if hasattr(block.chartType, 'value') else block.chartType, block.title]
    
    elif isinstance(block, MentionBlock):
        # mention: (id: string, label: string)
        return [block.id, block.label]
    
    elif isinstance(block, EmojiBlock):
        # emoji: (name: string)
        return [block.name]
    
    elif isinstance(block, JournalLinkBlock):
        # journalLink: (journalId: string, title: string = 'New Journal', attrs?: Record<string, any>)
        return [block.journalId, block.title]
    
    elif isinstance(block, AICompletionBlock):
        # aiCompletion: (old: string, newText: string, complete: boolean = false, attrs?: Record<string, any>)
        return [block.old, block.new, block.complete]
    
    elif isinstance(block, FlashcardSetBlock):
        # flashcardSet: (setName: string, flashcards: any[] = [], description: string = '', attrs?: Record<string, any>)
        return [block.setName, block.flashcards, block.description]
    
    elif isinstance(block, PracticeProblemSetBlock):
        # practiceProblemSet: (setName: string, problems: any[] = [], description: string = '', attrs?: Record<string, any>)
        return [block.setName, block.problems, block.description]
    
    elif isinstance(block, TableBlock):
        # table: (rows: ProseMirrorNode[], attrs?: Record<string, any>)
        rows = [_table_row_to_node(row) for row in block.rows]
        return [rows]
    
    elif isinstance(block, TableRowBlock):
        # tableRow: (cells: ProseMirrorNode[], attrs?: Record<string, any>)
        cells = [_table_cell_to_node(cell) for cell in block.cells]
        return [cells]
    
    elif isinstance(block, TableCellBlock):
        # tableCell: (content: ProseMirrorNode | Fragment, attrs?: Record<string, any>)
        content = _block_content_to_node(block.content)
        return [content]
    
    elif isinstance(block, TableHeaderBlock):
        # tableHeader: (content: ProseMirrorNode | Fragment, attrs?: Record<string, any>)
        content = _block_content_to_node(block.content)
        return [content]
    
    elif isinstance(block, DetailsBlock):
        # details: (summary: ProseMirrorNode, content: ProseMirrorNode, open: boolean = false, attrs?: Record<string, any>)
        summary_node = _details_summary_to_node(block.summary)
        content_node = _details_content_to_node(block.content)
        return [summary_node, content_node, block.open]
    
    elif isinstance(block, DetailsSummaryBlock):
        # detailsSummary: (text: string, attrs?: Record<string, any>)
        return [block.text]
    
    elif isinstance(block, DetailsContentBlock):
        # detailsContent: (content: ProseMirrorNode[], attrs?: Record<string, any>)
        content = [_block_content_to_node(item) for item in block.content]
        return [content]
    
    # Default fallback
    return []

def _get_node_type(block: "BaseBlock") -> str:
    """Get the ProseMirror node type string for a block."""
    type_map = {
        ParagraphBlock: "paragraph",
        HeadingBlock: "heading",
        BulletListBlock: "bulletList",
        OrderedListBlock: "orderedList",
        ListItemBlock: "listItem",
        BlockquoteBlock: "blockquote",
        HorizontalRuleBlock: "horizontalRule",
        HardBreakBlock: "hardBreak",
        CustomCodeBlock: "customCodeBlock",
        LatexBlock: "latex",
        InlineLatexBlock: "inlineLatex",
        ImageBlock: "image",
        VideoBlock: "video",
        AudioBlock: "audio",
        YoutubeBlock: "youtube",
        PDFBlock: "pdf",
        DOCXBlock: "docx",
        DesmosBlock: "desmos",
        ChartBlock: "chart",
        MentionBlock: "mention",
        EmojiBlock: "emoji",
        JournalLinkBlock: "journalLink",
        AICompletionBlock: "aiCompletion",
        FlashcardSetBlock: "flashcardSet",
        PracticeProblemSetBlock: "practiceProblemSet",
        TableBlock: "table",
        TableRowBlock: "tableRow",
        TableCellBlock: "tableCell",
        TableHeaderBlock: "tableHeader",
        DetailsBlock: "details",
        DetailsSummaryBlock: "detailsSummary",
        DetailsContentBlock: "detailsContent",
    }
    return type_map.get(type(block), "paragraph")

# Enums for specific types
class ChartType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    AREA = "area"

class Position(str, Enum):
    BEFORE = "before"
    AFTER = "after"

class OperationType(str, Enum):
    CREATE_NODE = "create_node"
    UPDATE_NODE = "update_node"
    DELETE_NODE = "delete_node"

# Base Block Model
class BaseBlock(BaseModel):
    """Base class for all block types"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    
    class Config:
        extra = "allow"

    def to_node(self) -> Dict[str, Any]:
        params = _block_to_node_params(self)
        node_type = _get_node_type(self)
        return {
            "type": node_type,
            "params": params,
            "attrs": {
                "id": self.id
            }
        }

# Text and Formatting Blocks
class ParagraphBlock(BaseBlock):
    """Standard paragraph block"""
    content: str = ""

class HeadingBlock(BaseBlock):
    """Heading block with level 1-3"""
    level: int = Field(ge=1, le=3)
    content: str

# List Blocks
class ListItemBlock(BaseBlock):
    """Individual list item"""
    content: Union[str, "ParagraphBlock", List[Any]]

class BulletListBlock(BaseBlock):
    """Unordered/bullet list"""
    items: List[ListItemBlock]

class OrderedListBlock(BaseBlock):
    """Numbered/ordered list"""
    items: List[ListItemBlock]
    start: int = 1

# Content Blocks
class BlockquoteBlock(BaseBlock):
    """Blockquote/citation block"""
    content: Union[str, List[Any]]

class HorizontalRuleBlock(BaseBlock):
    """Horizontal divider line"""
    pass

class HardBreakBlock(BaseBlock):
    """Hard line break"""
    pass

# Code Blocks
class CustomCodeBlock(BaseBlock):
    """Code block with runnable code"""
    code: str
    language: str = "python"

# LaTeX/Math Blocks
class LatexBlock(BaseBlock):
    """Block-level LaTeX math"""
    latex: str

class InlineLatexBlock(BaseBlock):
    """Inline LaTeX math"""
    latex: str

# Media Blocks
class ImageBlock(BaseBlock):
    """Image block"""
    src: str
    alt: Optional[str] = ""
    width: Optional[int] = None
    height: Optional[int] = None

class VideoBlock(BaseBlock):
    """Video block"""
    src: str
    width: Optional[int] = None
    height: Optional[int] = None

class AudioBlock(BaseBlock):
    """Audio block"""
    src: str
    title: Optional[str] = None

class YoutubeBlock(BaseBlock):
    """YouTube embed block"""
    src: str
    width: int = 640
    height: int = 480

class PDFBlock(BaseBlock):
    """PDF embed block"""
    src: str
    width: Optional[int] = None
    height: Optional[int] = None

class DOCXBlock(BaseBlock):
    """DOCX document embed block"""
    src: str
    width: Optional[int] = None
    height: Optional[int] = None

class DesmosBlock(BaseBlock):
    """Desmos graphing calculator block"""
    equations: str = Field(default="[y=x]", description="The equations to graph in the format [y=x], using escape characters where necessary.")

class ChartBlock(BaseBlock):
    """Chart/graph block"""
    chartType: ChartType = ChartType.BAR
    title: str = "Chart Title"
    data: Optional[Dict[str, Any]] = None

# Special Elements
class MentionBlock(BaseBlock):
    """User mention block"""
    label: str

class EmojiBlock(BaseBlock):
    """Emoji block"""
    name: str = Field(default=":smile:", description="The name of the emoji in the format :name:")

class JournalLinkBlock(BaseBlock):
    """Link to another journal"""
    journalId: str
    title: str = "New Journal"

class AICompletionBlock(BaseBlock):
    """AI text completion block"""
    old: str
    new: str
    complete: bool = False

# Set Blocks
class FlashcardSetBlock(BaseBlock):
    """Flashcard set container"""
    setName: str
    flashcards: List[Dict[str, Any]] = []
    description: str = ""

class PracticeProblemSetBlock(BaseBlock):
    """Practice problem set container"""
    setName: str
    problems: List[Dict[str, Any]] = []
    description: str = ""

# Table Blocks
class TableCellBlock(BaseBlock):
    """Table cell"""
    content: Any
    colspan: Optional[int] = 1
    rowspan: Optional[int] = 1

class TableHeaderBlock(BaseBlock):
    """Table header cell"""
    content: Any
    colspan: Optional[int] = 1
    rowspan: Optional[int] = 1

class TableRowBlock(BaseBlock):
    """Table row"""
    cells: List[Union[TableCellBlock, TableHeaderBlock]]

class TableBlock(BaseBlock):
    """Table container"""
    rows: List[TableRowBlock]

# Details/Accordion Blocks
class DetailsSummaryBlock(BaseBlock):
    """Collapsible section summary"""
    text: str

class DetailsContentBlock(BaseBlock):
    """Collapsible section content"""
    content: List[Any]

class DetailsBlock(BaseBlock):
    """Collapsible/accordion block"""
    summary: DetailsSummaryBlock
    content: DetailsContentBlock
    open: bool = False

##################################
# API Operation Models
##################################

class CreateNodeOperation(BaseModel):
    """Create a new node from parameters"""
    type: Literal["create_node"] = "create_node"
    nodeType: str
    params: Dict[str, Any]
    referenceId: Optional[str] = None
    position: Position = Position.AFTER

class UpdateNodeOperation(BaseModel):
    """Replace an entire node while keeping its ID"""
    type: Literal["update_node"] = "update_node"
    nodeId: str
    node: Dict[str, Any]  # The complete new node definition

class DeleteNodeOperation(BaseModel):
    """Delete a node"""
    type: Literal["delete_node"] = "delete_node"
    nodeId: str

__all__ = [
    "ChartType",
    "Position",
    "OperationType",
    "BaseBlock",
    "ParagraphBlock",
    "HeadingBlock",
    "ListItemBlock",
    "BulletListBlock",
    "OrderedListBlock",
    "BlockquoteBlock",
    "HorizontalRuleBlock",
    "HardBreakBlock",
    "CustomCodeBlock",
    "LatexBlock",
    "InlineLatexBlock",
    "ImageBlock",
    "VideoBlock",
    "AudioBlock",
    "YoutubeBlock",
    "PDFBlock",
    "DOCXBlock",
    "DesmosBlock",
    "ChartBlock",
    "MentionBlock",
    "EmojiBlock",
    "JournalLinkBlock",
    "AICompletionBlock",
    "FlashcardSetBlock",
    "PracticeProblemSetBlock",
    "TableCellBlock",
    "TableHeaderBlock",
    "TableRowBlock",
    "TableBlock",
    "DetailsSummaryBlock",
    "DetailsContentBlock",
    "DetailsBlock",
    "CreateNodeOperation",
    "UpdateNodeOperation",
    "DeleteNodeOperation",
]
