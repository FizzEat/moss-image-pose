# moss-image-pose

**MOSS-Image 人像姿势与构图 skill（非官方）**：说清要什么姿势、站哪、什么机位，自动生成 MOSS-Image 原生布局 JSON，粘进 Echidna 工作台直接出图。

适用：Claude Code / Codex / Cursor 等 agent（读 `SKILL.md`），也可以手动跑脚本。只做 SFW 内容。

## 和官方 enhancer 的关系

OpenMOSS 官方仓库带了一个通用的 `moss-image-prompt-enhancer`，负责扩写描述和海报、文字排版类布局，不涉及人像姿势。
本仓库只做人像这一块，两者输出同一种布局 JSON，可以一起装：

| | 官方 enhancer | 本仓库 |
|---|---|---|
| 场景 | 通用：海报、信息图、文字排版 | 人像：单人、双人、三人 |
| 姿势 | 无 | 38 个逐关节描述的姿势库 |
| 框怎么来 | agent 自己按像素画 | 姿势 + 景别 + 站位自动换算 |
| 构图张力 | 无 | T0 到 T3 机位阶梯 |

## 快速开始

```bash
python3 scripts/build_layout.py --list

python3 scripts/build_layout.py --pose stand_look_back --position right \
  --width 832 --height 1248 \
  --subject "a young woman in a beige trench coat and white sneakers" \
  --scene "a rainy city street at dusk, neon reflections on wet pavement" \
  --style "cinematic street photo, 35mm film grain" --out outputs/look_back
```

然后在 Echidna：先把分辨率设成 832×1248，把 `outputs/look_back.layout.min.txt` 的内容粘进「文生图」的正向 Prompt，负面填输出的负面词，50 步、CFG 3、Shift 5、跳层 22，生成。

## 实测（Echidna，MOSS-Image-SFT，2026-10-21）

| 用例 | 设置 | 结果 |
|---|---|---|
| 回眸，站右三分线 | 832×1248，T1 | 人物落在右侧，左侧留白，回眸角度正确 |
| 腾空跳跃 | 832×1248，T3 | 双脚离地、双臂上举，动作定格 |
| 双人：抱臂 + 插兜 | 1248×832，两个框 | 左右站位正确，姿势各自对应，无肢体粘连 |
| 趴着看书 | 1248×832，横向框 | 撑肘、小腿抬起交叉，全身入画 |

实测结论：「文生图」模式直接粘布局 JSON 即生效；「布局生图」编辑器改分辨率时会按比例拉伸所有框，所以一定先定分辨率再粘布局。

## 致谢

- 模型与布局格式：[OpenMOSS/MOSS-Image](https://github.com/OpenMOSS/MOSS-Image)（Apache-2.0）
- 结构参考：qwen21-nsfw-pose-skill 的「提示词配方 + 姿势库」思路（本仓库只保留 SFW 部分）

本项目与 OpenMOSS 官方无关。作者：韦小宝@nicebabycat
