# PDF에서 Text 추출

[Extract Text from a PDF](https://pypdf.readthedocs.io/en/stable/user/extract-text.html)를 참조하여 아래와 같이 pdf파일에서 Text 추출합니다.

```python
from pypdf import PdfReader

reader = PdfReader("example.pdf")
page = reader.pages[0]
print(page.extract_text())

# extract only text oriented up
print(page.extract_text(0))

# extract text oriented up and turned left
print(page.extract_text((0, 90)))
```

