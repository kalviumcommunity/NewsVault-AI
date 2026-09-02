from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Document:
    title: str
    filename: str
    document_type: str
    author: Optional[str] = None
    document_date: Optional[date] = None
    topic: Optional[str] = None
    id: Optional[int] = None