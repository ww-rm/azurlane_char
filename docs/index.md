---
title: azurlane_char
permalink: /index.html
---

[![Test](https://github.com/ww-rm/azurlane_char/actions/workflows/test.yaml/badge.svg)](https://github.com/ww-rm/azurlane_char/actions/workflows/test.yaml)

这是碧蓝航线小人模型资源仓库.

点击返回[网站首页](/).

## 使用方法

### 获取资源索引

请求:

`/azurlane_char/index.json`

响应:

```json
{
    "<shipName>": {
        "chName": "<舰娘中文名>",
        "hxName[可选]": "<舰娘和谐名>",
        "skins": {
            "<skinName>": {
                "chName": "<皮肤中文名>",
                "skelName": "<skel文件名>",
                "atlasName": "<atlas文件名>",
                "pages": ["<png1文件名>", "<png2文件名>"]
            }
        }
    }
}
```

Pydantic 解析示例:

```python
class Skin(BaseModel):
    chName: str
    skelName: str
    atlasName: str
    pages: List[str]

class Ship(BaseModel):
    chName: str
    hxName: Optional[str] = None
    skins: Dict[str, Skin]

class ShipData(RootModel):
    root: Dict[str, Ship]
```

访问测试:

- [/azurlane_char/index.json](/azurlane_char/index.json)

### 加载资源文件

请求:

`/azurlane_char/<shipName>/<文件名>`

访问测试:

- [/azurlane_char/lafei/lafei.atlas](/azurlane_char/lafei/lafei.atlas)
- [/azurlane_char/lafei/lafei.skel](/azurlane_char/lafei/lafei.skel)
- [/azurlane_char/lafei/lafei.png](/azurlane_char/lafei/lafei.png)
