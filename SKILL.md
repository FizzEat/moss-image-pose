---
name: moss-image-pose
description: 为 MOSS-Image（OpenMOSS 5B 文生图模型，含 Echidna 在线工作台）生成人像姿势与构图提示词。用户想用 MOSS-Image 出指定姿势、景别、站位的人像照片或插画（含双人、三人），或要人像布局 JSON 时使用。只做 SFW 内容。通用海报、文字排版类需求交给官方 moss-image-prompt-enhancer。
---

# MOSS-Image 人像姿势与构图 skill

把「我想要一个人怎么站、站在画面哪里、用什么机位」翻译成 MOSS-Image 能稳定执行的布局 JSON。
手段是两层锁定：边界框把人物钉在画面指定位置，逐关节的英文描述锁定姿势。

与官方 `moss-image-prompt-enhancer` 的分工：官方负责通用扩写和海报、文字排版布局；本 skill 只做人像，提供姿势库、景别和站位到边界框的自动换算、多人分框。两者输出同一种布局 JSON，可以混用。

## 0. 内容边界与模式

- **默认 SFW 模式**：负面提示词包含 `nsfw`，适用于大众街拍、运动、日常与职业写真。
- **Glamour 私房与唯美曲线模式**：支持私房人像写真、泳装沙滩、丝缎吊带睡裙、卧榻反弓美背等摄影级艺术构图（`--allow-glamour`）。
- **底线红线**：严格禁止全裸、露骨色情、生殖露点及任何违规违法内容。
- **肖像保护**：不生成可识别的真实公众人物或特定个人的肖像。

## 1. 推荐参数（官方 USERGUIDE + Echidna 实测）

| 项 | 值 |
|---|---|
| 分辨率 | 约 1M 像素，宽高为 16 的倍数：竖版 832×1248，横版 1248×832，方图 1024×1024 |
| 步数 | 50 |
| CFG | 3（提示词很短时提到 4 到 6） |
| Shift | 5 |
| 采样器 | Euler |
| 跳层 | 第 22 层，仅负向 |
| 负面 | `nsfw, worst quality, bad anatomy, extra limbs, extra fingers, watermark, jpeg artifact` |
| 语言 | 描述用英文；画面内要渲染的中文文字直接写中文 |

Echidna 实测单张 1M 像素 50 步约 35 秒。

## 2. 在 Echidna 上使用（实测确认的流程）

1. 进入「生成」页，模型选 MOSS-Image-SFT，停在「文生图」标签。
2. **先定分辨率**：「画面与采样」里用「宽高比」下拉选比例，再点「1M」。宽高必须与生成布局时用的一致。
3. 把脚本输出的**单行布局 JSON** 整段粘进「正向 Prompt」，反向 Prompt 填负面词。
4. 打开「高级设置」核对：50 步、CFG 3、Shift 5、跳层 22。点过「标准 / 极致」等预设或改过分辨率后，CFG 可能被改成 5，要改回 3。
5. 提交生成。

实测要点：
- 「文生图」模式直接粘布局 JSON 就生效，不必进「布局生图」编辑器。
- 「布局生图」编辑器适合手动拖框微调：在「布局 JSON」框粘贴后点「导入布局」，改完点「保存并应用」再生成。**改分辨率时编辑器会把所有框按比例拉伸**，所以要先定分辨率再导入；导入后不要点「转换格式」到 scene.v1，会丢掉 label 字段。

## 3. 布局 JSON 格式

```json
{"summary":{"meta":["photo"],"canvas":"single","caption":"整体：风格、景别、人物与姿势、场景、机位、光线"},
 "items":[{"label":"character","caption":"人物外观 + 姿势逐关节描述","bbox":[y_min,x_min,y_max,x_max]}],
 "bbox_coord_space":"abs_centralized","bbox_format":"yxyx"}
```

坐标以画布中心为原点，x 向右为正，y 向下为正。832×1248 画布的范围是 x∈[-416, 416]、y∈[-624, 624]。
左上角原点的像素坐标换算：x 减 W/2，y 减 H/2。不要手算，用脚本。

## 4. 提示词结构（每条都要写满）

`summary.caption` 按顺序拼：风格媒介 → 景别 → 人物外观与姿势（多人时用 on the left / on the right 标明）→ 场景与道具 → 机位镜头 → 光线。
`character.caption` 只写这个人的外观和姿势，不写场景。

姿势要写「哪个肢体在什么位置」，至少覆盖重心、双腿、双臂、头部朝向四项：
- ✗ `doing a contrapposto pose`
- ✓ `weight shifted onto the right leg, hips tilted, left hand resting on the hip, head turned toward the left shoulder`

服装和姿势要自洽：插兜就写 pockets，别让毛衣上出现 coat pockets。

## 5. 构图张力阶梯 T0 到 T3

只由机位、镜头、肢体伸展幅度决定，与暴露无关。

| 等级 | 机位镜头 | 适合姿势族 |
|---|---|---|
| T0 | 平视，50mm，平衡构图 | 站立、坐姿、托腮、趴着看书 |
| T1 | 微侧角，35mm，抓拍感 | 回眸、靠墙、侧坐、蹲姿 |
| T2 | 低机位，28mm，对角线构图 | 慢跑、转圈、拉伸、击掌 |
| T3 | 低机位广角，24mm，动作峰值定格 | 腾空跳、舞蹈伸展、投篮 |

用户说「更有冲击力」「更动感」升一级；说「更安静」「证件照感」降一级。多人时取所有姿势中最高的等级。

## 6. 景别、站位与框（脚本自动处理）

- 全身：框高约 86% 画布，脚底离下沿 4%。
- 膝上 / 腰上 / 胸上：框下沿贴画布下沿（出画），框加宽容纳上半身。
- 横向姿势（躺、趴）：按画布宽定框，放中心略偏下，用横版画幅。
- 单人站位 left / right：落在三分线，框宽上限 62%，保证另一侧真正留白。
- 多人：每人一个 character 框，框宽各占画布的 1/人数，框之间自然留缝，避免肢体粘连。最多 3 人。

## 7. 工作流程

1. 确认：姿势、景别、站位、画幅、人物外观、场景。没说的用默认（全身、居中、832×1248）。
2. 用户给的是描述不是姿势 ID：在 `poses/poses.json` 找最接近的；没有就按第 4 节现写逐关节描述，补进 poses.json。
3. 运行脚本：

```bash
# 单人
python3 scripts/build_layout.py --pose stand_look_back --position right \
  --width 832 --height 1248 \
  --subject "a young woman in a beige trench coat and white sneakers" \
  --scene "a rainy city street at dusk, neon reflections on wet pavement" \
  --style "cinematic street photo, 35mm film grain" \
  --light "cool blue dusk light mixed with warm neon" --out outputs/look_back

# 双人：姿势逗号分隔，外观用 || 分隔，默认左右站位
python3 scripts/build_layout.py --pose stand_arms_crossed,stand_hands_pockets \
  --width 1248 --height 832 \
  --subject "a young man in a black leather jacket || a young woman in a cream knit sweater" \
  --scene "a brick-walled alley with string lights" --out outputs/duo
```

4. 交付 `.layout.min.txt` 的内容（直接粘贴用）、负面词、分辨率，按第 2 节流程操作。
5. 出图不对按第 8 节排查，一次只改一个变量。

`python3 scripts/build_layout.py --list` 列出全部姿势。

## 8. 常见问题排查

| 现象 | 改法 |
|---|---|
| 姿势对不上 | 姿势描述补足四项关节；最关键的一句放到 character.caption 最前 |
| 人物位置不对 | 核对工作台分辨率是否与生成布局时一致；在布局编辑器里看框是否被拉伸 |
| 全身图脚被裁 | 框下沿离画布下沿至少 4%；caption 保留 head to toe visible |
| 手指崩 | 保持跳层 22；负面含 extra fingers；手部动作写简单些 |
| 太像 AI、太油 | 跳层改 24 或 26；风格加 candid photo, natural skin texture |
| 双人肢体粘连 | 确认是两个 character 框，框之间有空隙 |
| 构图太平 | 张力升一级（--tension T2） |
