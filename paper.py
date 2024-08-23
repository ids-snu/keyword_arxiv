from dataclasses import dataclass
from typing import List

@dataclass
class PaperClass:
    title: str
    authors: str
    abstract: str
    link: str
    comments: str = None
    keywords: list[str] = None
    
    
    def highligh_keywords(self, text):
        for keyword in self.keywords:
            text = text.replace(keyword, f'<b><mark>{keyword}</mark></b>')
        return text
    
    
    def __repr__(self) -> str:
        if self.comments is None:
            return f"""<h3>Title</h3><p>{self.highligh_keywords(self.title)}</p><h3>Authors</h3><p>{self.highligh_keywords(self.authors)}</p><h3>Abstract</h3><p>{self.highligh_keywords(self.abstract)}</p><h3>Link</h3><p>{self.link}</p>"""
        else:
            return f"""<h3>Title</h3><p>{self.highligh_keywords(self.title)}</p><h3>Authors</h3><p>{self.highligh_keywords(self.authors)}</p><h3>Abstract</h3><p>{self.highligh_keywords(self.abstract)}</p><h3>Comments</h3><p>{self.highligh_keywords(self.comments)}</p><h3>Link</h3><p>{self.link}</p>"""
