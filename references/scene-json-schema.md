# Scene JSON 协议

## 目的

Scene JSON 是内容理解模型与确定性布局/渲染器之间的中间协议。模型只表达语义和约束；像素位置、文字测量、避让和连线路径交给程序计算。

## 最小结构

```json
{
  "canvas": {
    "width": 1200,
    "height": 675,
    "ratio": "16:9",
    "background": "#FFFFFF",
    "grid": 8
  },
  "intent": {
    "core_message": "AI Agent 连接数据、工具与业务场景",
    "composition": "layered-architecture",
    "focus_node": "agent"
  },
  "style": {
    "theme": "geometry-minimal",
    "accent_color": "#2F6BFF",
    "line_weight": 1,
    "corner_radius": 0
  },
  "nodes": [
    {"id": "data", "type": "plane", "label": "数据", "importance": 2},
    {"id": "agent", "type": "cube", "label": "AI Agent", "importance": 5},
    {"id": "tools", "type": "plane", "label": "工具", "importance": 2},
    {"id": "scenario", "type": "frame", "label": "业务场景", "importance": 3}
  ],
  "edges": [
    {"from": "data", "to": "agent", "relation": "input"},
    {"from": "agent", "to": "tools", "relation": "invoke"},
    {"from": "agent", "to": "scenario", "relation": "execute"}
  ]
}
```

## 字段约束

- `canvas.width`、`canvas.height` 必须为正数；默认 `1200`、`675`。
- `canvas.ratio` 只使用 `16:9`、`4:3`、`A4` 或明确记录的自定义比例。
- `canvas.background` 默认 `#FFFFFF`；避免深色背景。
- `intent.core_message` 必须是一句可核验的核心判断。
- `intent.composition` 必须是视觉系统中的八个模板 ID 之一。
- `intent.focus_node` 必须指向一个存在的节点；最多保留两个视觉重点。
- `style.accent_color` 只能有一个强调色；未指定时可省略。
- `style.corner_radius` 默认 0；不要让圆角成为默认装饰。
- `nodes[].id` 唯一且稳定；`type` 使用 `point`、`line`、`circle`、`rect`、`plane`、`cube`、`cylinder`、`dot-grid`、`frame` 等语义类型。
- `nodes[].label` 是短标签，不把段落塞入节点；单节点不超过 12 个汉字。
- `nodes[].importance` 使用 1–5 的整数；5 为核心对象。
- `edges[].from` 与 `edges[].to` 必须引用存在的节点；`relation` 使用简短关系词。
- 节点默认不超过 15 个，边默认不超过 20 条；全图文字原则上不超过 100 个汉字。

可选字段包括 `nodes[].note`、`nodes[].state`、`nodes[].accent`、`edges[].style`、`edges[].label`、`layout.orientation` 和 `annotations[]`。只有在确有表达作用时添加。

## 生成策略

1. 先生成 `intent`，再生成 `nodes` 和 `edges`；不要先堆节点。
2. 让每条边表达一种明确关系；发现孤立节点时删除或补充依据。
3. 用 `importance` 表达主次，而不是同时使用多个强颜色、阴影和大字号。
4. 不在 Scene JSON 中固化像素位置，除非用户要求锁定已有布局；默认由布局引擎根据构图计算。
5. 通过校验后再渲染；修改时尽量保持节点 ID，便于局部更新和版本比较。
