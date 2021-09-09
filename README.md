# Erc

## Install

You can install Erc by doing
```
pip install -U git+https://github.com/WhyDoWeLiveWithoutMeaning/Erc
```

### Code Example

```
!1 Header 1 !
!2 Header 2 !
? paragraph that **also** *handeles* __multiple__ --__different__-- __--***formats***--__ ?

T
this is a | Table
pretty cool | if you think
T

? s. ++ You are also able to have Options == ++ As if you wanted to do this alot == .s ?
```

You can format it to HTML

```python
from erc import Erc

with open("file.erc", "r") as f:
    i = Erc(f.read())
    print(i.html)
```
