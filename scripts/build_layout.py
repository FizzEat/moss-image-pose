#!/usr/bin/env python3
"""MOSS-Image 人像姿势布局生成器。

把「姿势 + 景别 + 站位 + 画幅」换算成 MOSS-Image 原生布局 JSON
（bbox_format=yxyx，bbox_coord_space=abs_centralized），同时输出
等价的自然语言提示词、负面提示词和推荐参数。

示例：
  python3 scripts/build_layout.py --pose stand_look_back --framing full \
      --position right --width 832 --height 1248 \
      --subject "a young woman in a beige trench coat" \
      --scene "a rainy Shanghai street at dusk, neon reflections on wet pavement" \
      --style "cinematic photo, 35mm film grain" --out examples/look_back
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSE_FILE = os.path.join(ROOT, "poses", "poses.json")

NEGATIVE = "nsfw, worst quality, bad anatomy, extra limbs, extra fingers, watermark, jpeg artifact"

# 构图张力等级：只控制机位和镜头，不涉及暴露程度
TENSION_CAMERA = {
    "T0": "eye-level shot, 50mm lens, calm balanced composition",
    "T1": "slightly angled shot, 35mm lens, natural candid composition",
    "T2": "low-angle shot, 28mm lens, dynamic diagonal composition",
    "T3": "dramatic low-angle wide shot, 24mm lens, motion frozen at the peak moment, strong diagonal lines",
}

FRAMING_TEXT = {
    "full": "full-body shot, head to toe visible",
    "knee": "medium-long shot framed from the knees up",
    "waist": "medium shot framed from the waist up",
    "close": "close-up portrait from the chest up",
}
# 景别 -> 可见身体比例（相对全身高度）
FRAMING_VISIBLE = {"full": 1.0, "knee": 0.72, "waist": 0.48, "close": 0.28}

POSITION_X = {"center": 0.0, "left": -1 / 6, "right": 1 / 6}

# 开源仓库的硬性边界：SFW 默认拦截
BLOCKED = re.compile(
    r"\b(nude|naked|nsfw|topless|nipple|genital|explicit|porn|sexual|lingerie|underwear|see[- ]through)\b"
    r"|裸|色情|情色|露点|内衣|透视装|性感身体",
    re.I,
)

# 允许私房与唯美曲线（Glamour）时的安全边界（仅拦截绝对露骨/全裸违规内容）
BLOCKED_GLAMOUR = re.compile(
    r"\b(nude|naked|topless|nipple|genital|explicit|porn|csam)\b|全裸|露点|生殖|露生殖器|色情交配",
    re.I,
)


def load_poses():
    with open(POSE_FILE, encoding="utf-8") as f:
        return {p["id"]: p for p in json.load(f)["poses"]}


def check_safe(allow_glamour, *texts):
    blocker = BLOCKED_GLAMOUR if allow_glamour else BLOCKED
    for t in texts:
        if t and blocker.search(t):
            sys.exit("拒绝生成：检测到超出安全边界的不允许内容。")


def subject_bbox(pose, framing, position, W, H, max_w_frac=0.94):
    ratio = pose["body_ratio"]  # 全身框 宽/高
    vis = FRAMING_VISIBLE[framing]
    if ratio > 1.2 and framing == "full":
        # 横向姿势（躺、趴）：按宽度定框
        w = max_w_frac * 0.94 * W
        h = min(w / ratio, 0.7 * H)
        cy = 0.12 * H  # 略低于中心
        ymin, ymax = cy - h / 2, cy + h / 2
    else:
        if framing == "full":
            h = 0.86 * H
            ymax = H / 2 - 0.04 * H
        else:
            h = 0.92 * H
            ymax = H / 2  # 下沿出画
        ymin = ymax - h
        w = h * ratio / vis if framing != "full" else h * ratio
    # 偏左/偏右时限制框宽，保证另一侧真的留白
    if position != "center":
        max_w_frac = min(max_w_frac, 0.62)
    w = min(w, max_w_frac * W)
    cx = POSITION_X[position] * W
    half = w / 2
    cx = max(-W / 2 + half, min(W / 2 - half, cx))  # 不越界
    return [int(ymin // 1), int((cx - half) // 1), -int(-ymax // 1), -int(-(cx + half) // 1)]


def build(args):
    poses = load_poses()
    pose_ids = [x.strip() for x in args.pose.split(",")]
    for pid in pose_ids:
        if pid not in poses:
            sys.exit(f"未知姿势 {pid}，用 --list 查看全部姿势")
    n = len(pose_ids)
    if n > 3:
        sys.exit("一次最多 3 个人物")
    subjects = [x.strip() for x in args.subject.split("||")]
    if len(subjects) == 1:
        subjects = subjects * n
    if len(subjects) != n:
        sys.exit("--subject 用 || 分隔，数量要和姿势数量一致")
    if args.position:
        positions = [x.strip() for x in args.position.split(",")]
    else:
        positions = {1: ["center"], 2: ["left", "right"], 3: ["left", "center", "right"]}[n]
    if len(positions) != n or any(p not in POSITION_X for p in positions):
        sys.exit("--position 数量要和姿势一致，取值 left/center/right")
    if args.width % 16 or args.height % 16:
        sys.exit("宽高必须是 16 的倍数")
    mp = args.width * args.height / 1e6
    if not 0.25 <= mp <= 4.2:
        sys.exit(f"总像素 {mp:.2f}M 超出 0.25M 到 4M 范围")
    check_safe(args.allow_glamour, args.subject, args.scene, args.style, args.extra, args.text)

    W, H = args.width, args.height
    plist = [poses[pid] for pid in pose_ids]
    order = ["T0", "T1", "T2", "T3"]
    tension = args.tension or max((p["tension"] for p in plist), key=order.index)
    max_w = 0.94 if n == 1 else 0.94 / n

    items, people = [], []
    for pose, subj, pos in zip(plist, subjects, positions):
        cap = f"{subj}, {pose['en']}"
        if args.extra and n == 1:
            cap += f", {args.extra}"
        items.append({
            "label": "character",
            "caption": cap,
            "bbox": subject_bbox(pose, args.framing, pos, W, H, max_w),
        })
        where = {"left": "on the left", "right": "on the right", "center": "in the center"}[pos]
        people.append(f"{where}, {cap}" if n > 1 else cap)

    count = {1: "", 2: "two people, ", 3: "three people, "}[n]
    summary_caption = ", ".join(
        x for x in [
            args.style,
            FRAMING_TEXT[args.framing],
            count + "; ".join(people),
            args.scene,
            TENSION_CAMERA[tension],
            args.light,
        ] if x
    )
    if args.text:
        items.append({
            "label": "text",
            "caption": "Clean bold title text at the top of the image.",
            "text": args.text,
            "bbox": [round(-H / 2 + 0.04 * H), round(-0.4 * W), round(-H / 2 + 0.14 * H), round(0.4 * W)],
        })
    pose = plist[0] if n == 1 else {"zh": " + ".join(p["zh"] for p in plist), "id": args.pose}

    layout = {
        "summary": {"meta": ["photo"], "canvas": "single", "caption": summary_caption},
        "items": items,
        "bbox_coord_space": "abs_centralized",
        "bbox_format": "yxyx",
    }

    natural = summary_caption + "."
    if args.text:
        natural += f' The title text "{args.text}" is written at the top.'

    neg = NEGATIVE if not args.allow_glamour else "worst quality, bad anatomy, extra limbs, extra fingers, watermark, jpeg artifact"
    params = {
        "width": W, "height": H, "steps": 50, "cfg": 3.0,
        "shift": 5.0, "sampler": "euler", "slg_skip_layer": 22,
        "negative_prompt": neg,
    }
    return pose, tension, layout, natural, params


def main():
    ap = argparse.ArgumentParser(description="MOSS-Image 人像姿势布局生成器")
    ap.add_argument("--list", action="store_true", help="列出全部姿势")
    ap.add_argument("--pose", help="姿势 ID，多人用逗号分隔（最多 3 人）")
    ap.add_argument("--framing", default="full", choices=list(FRAMING_TEXT))
    ap.add_argument("--position", default="", help="left/center/right，多人用逗号分隔；默认单人居中，双人左右")
    ap.add_argument("--tension", choices=list(TENSION_CAMERA), help="覆盖姿势默认的张力等级")
    ap.add_argument("--width", type=int, default=832)
    ap.add_argument("--height", type=int, default=1248)
    ap.add_argument("--subject", default="a young woman in casual everyday clothes", help="人物外观，多人用 || 分隔")
    ap.add_argument("--scene", default="")
    ap.add_argument("--style", default="realistic photo")
    ap.add_argument("--light", default="soft natural light")
    ap.add_argument("--extra", default="", help="追加到人物描述的细节（表情、发型等）")
    ap.add_argument("--text", default="", help="可选：画面顶部渲染的标题文字")
    ap.add_argument("--allow-glamour", action="store_true", help="启用私房/微性感模式（允许内衣、吊带睡裙、唯美泳装等描述，负向词自动放行）")
    ap.add_argument("--out", help="输出前缀，生成 .layout.json / .prompt.txt / .params.json")
    args = ap.parse_args()

    if args.list:
        for p in load_poses().values():
            print(f"{p['id']:<24}{p['tension']}  {p['family']:<10}{p['zh']}")
        return
    if not args.pose:
        ap.error("需要 --pose（或用 --list 查看）")

    pose, tension, layout, natural, params = build(args)
    layout_str = json.dumps(layout, ensure_ascii=False, indent=2)
    compact = json.dumps(layout, ensure_ascii=False, separators=(",", ":"))
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out + ".layout.json", "w", encoding="utf-8") as f:
            f.write(layout_str + "\n")
        with open(args.out + ".layout.min.txt", "w", encoding="utf-8") as f:
            f.write(compact + "\n")
        with open(args.out + ".prompt.txt", "w", encoding="utf-8") as f:
            f.write(natural + "\n")
        with open(args.out + ".params.json", "w", encoding="utf-8") as f:
            json.dump(params, f, ensure_ascii=False, indent=2)
    print(f"# 姿势：{pose['zh']}（{pose['id']}） 张力：{tension}")
    print(f"# 画布 {args.width}x{args.height}（先在工作台设好分辨率，再粘贴布局）")
    print("# 布局 JSON（单行，可直接粘贴为正向提示词）")
    print(compact)
    print("# 自然语言提示词")
    print(natural)
    print("# 负面提示词")
    print(params["negative_prompt"])


if __name__ == "__main__":
    main()
