#!/usr/bin/env python3
"""
MOSS-Image-Pose Workflow Demonstration Generator
Generates an animated GIF and MP4 demonstrating the full 4-step pipeline:
1. Natural language agent prompt understanding & pose matching
2. Geometric coordinate calculation & single-line JSON generation
3. Echidna workbench one-click pasting & inference
4. Ultra-HD photorealistic result verification
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCES_DIR = os.path.join(PROJECT_ROOT, "references")
os.makedirs(REFERENCES_DIR, exist_ok=True)

WIDTH = 960
HEIGHT = 580

BG_COLOR = (13, 17, 23)        # GitHub Dark
CARD_BG = (22, 27, 34)         # GitHub Dark Secondary
BORDER_COLOR = (48, 54, 61)
TEXT_WHITE = (240, 246, 252)
TEXT_MUTED = (139, 148, 158)
ACCENT_BLUE = (88, 166, 255)
ACCENT_GREEN = (63, 185, 80)
ACCENT_PINK = (247, 120, 186)
ACCENT_YELLOW = (210, 153, 34)
CODE_BG = (10, 12, 16)

zh_font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
code_font_path = "/System/Library/Fonts/Menlo.ttc"

title_font = ImageFont.truetype(zh_font_path, 22)
header_font = ImageFont.truetype(zh_font_path, 17)
body_font = ImageFont.truetype(zh_font_path, 15)
small_font = ImageFont.truetype(zh_font_path, 13)
zh_code_small = ImageFont.truetype(zh_font_path, 12)
code_font = ImageFont.truetype(code_font_path, 13)
code_small = ImageFont.truetype(code_font_path, 11)

sample_img_path = os.path.join(PROJECT_ROOT, "examples", "sample_glamour_kneel.png")
if not os.path.exists(sample_img_path):
    raise FileNotFoundError(f"Sample image not found: {sample_img_path}")
sample_img = Image.open(sample_img_path).convert("RGB")

frames = []

def draw_window_frame(draw, title="moss-image-pose 工作流程演示"):
    draw.rectangle([0, 0, WIDTH, 40], fill=(22, 27, 34))
    draw.line([0, 40, WIDTH, 40], fill=BORDER_COLOR, width=1)
    draw.ellipse([16, 14, 28, 26], fill=(255, 95, 86))
    draw.ellipse([36, 14, 48, 26], fill=(255, 189, 46))
    draw.ellipse([56, 14, 68, 26], fill=(39, 201, 63))
    draw.text((WIDTH // 2 - 130, 11), title, fill=TEXT_MUTED, font=body_font)

# -------------------------------------------------------------
# Stage 1: Natural Language Chat / Agent Calling (18 frames)
# -------------------------------------------------------------
for i in range(18):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, "Step 1/4 · 自然语言理解与骨骼姿态匹配")
    
    # Title badge
    draw.rounded_rectangle([40, 56, 145, 84], radius=6, fill=(31, 111, 235))
    draw.text((50, 62), "Agent 技能交互", fill=TEXT_WHITE, font=small_font)
    draw.text((160, 62), "Claude Code / Cursor / Antigravity 原生调用", fill=TEXT_MUTED, font=body_font)
    
    # User message bubble
    draw.rounded_rectangle([40, 100, WIDTH - 40, 175], radius=10, fill=CARD_BG, outline=BORDER_COLOR)
    draw.rounded_rectangle([55, 112, 125, 136], radius=4, fill=(110, 40, 140))
    draw.text((63, 116), "用户指令", fill=TEXT_WHITE, font=small_font)
    draw.text((140, 115), "“帮我用 MOSS-Image 出一张私房跪趴姿态，暗酒红连体装，高级卧室，35mm电影感”", fill=TEXT_WHITE, font=body_font)
    draw.text((55, 148), "要求：人物居中前倾、腰背反弓、手肘与膝部承重受力、眼神慵懒、毛孔级写实画质", fill=TEXT_MUTED, font=small_font)
    
    # Agent response card
    draw.rounded_rectangle([40, 195, WIDTH - 40, 535], radius=10, fill=CARD_BG, outline=ACCENT_BLUE if i > 3 else BORDER_COLOR)
    draw.rounded_rectangle([55, 210, 135, 234], radius=4, fill=(35, 134, 54) if i > 3 else (45, 55, 65))
    draw.text((63, 214), "姿态匹配完成" if i > 3 else "正在解析指令...", fill=TEXT_WHITE, font=small_font)
    draw.text((150, 214), "从内置 46 款骨骼姿势库中自动命中最佳解剖姿态" if i > 3 else "分析关节结构与力学自洽性...", fill=ACCENT_GREEN if i > 3 else TEXT_MUTED, font=body_font)
    
    if i >= 4:
        draw.text((55, 255), "命中姿势 ID :", fill=TEXT_MUTED, font=body_font)
        draw.text((170, 255), "glamour_bed_kneel (私房跪趴 · T1 构图张力阶梯)", fill=ACCENT_YELLOW, font=body_font)
        
        draw.text((55, 290), "逐关节英文描述 :", fill=TEXT_MUTED, font=body_font)
        draw.rounded_rectangle([55, 320, WIDTH - 55, 395], radius=6, fill=CODE_BG, outline=BORDER_COLOR)
        draw.text((70, 330), "kneeling and leaning forward on a bed, hips tilted, lower back naturally arched,", fill=TEXT_WHITE, font=code_font)
        draw.text((70, 355), "body weight supported on the knees, looking back over shoulder with lazy alluring gaze", fill=TEXT_WHITE, font=code_font)
        
        draw.text((55, 415), "模式放行策略 :", fill=TEXT_MUTED, font=body_font)
        draw.text((170, 415), "--allow-glamour 放行 (解除负面词 nsfw 压制，完美呈现丝缎与腰臀S曲线)", fill=ACCENT_PINK, font=body_font)
        
        draw.text((55, 450), "机位构图建议 :", fill=TEXT_MUTED, font=body_font)
        draw.text((170, 450), "35mm 广角抓拍 ｜ 居中偏大构图占 88% ｜ 离底 4% 全身完整入画", fill=TEXT_WHITE, font=body_font)
        
        draw.rounded_rectangle([55, 485, 275, 518], radius=6, fill=(31, 111, 235))
        draw.text((70, 493), "准备生成原生布局 JSON ->", fill=TEXT_WHITE, font=small_font)

    frames.append(img)

# -------------------------------------------------------------
# Stage 2: Geometric Coordinate Calculation (18 frames)
# -------------------------------------------------------------
for i in range(18):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, "Step 2/4 · 空间几何换算与单行原生布局生成")
    
    draw.rounded_rectangle([40, 56, 175, 84], radius=6, fill=(31, 111, 235))
    draw.text((50, 62), "空间几何换算引擎", fill=TEXT_WHITE, font=small_font)
    draw.text((190, 62), "中心原点 abs_centralized 坐标系精确投射", fill=TEXT_MUTED, font=body_font)
    
    # Left: Terminal Execution
    draw.rounded_rectangle([40, 100, 530, 535], radius=10, fill=CODE_BG, outline=BORDER_COLOR)
    draw.text((55, 115), "$ python3 scripts/build_layout.py \\", fill=TEXT_MUTED, font=code_font)
    draw.text((75, 138), "--pose glamour_bed_kneel --allow-glamour \\", fill=ACCENT_PINK, font=code_font)
    draw.text((75, 161), "--width 832 --height 1248 --framing full", fill=ACCENT_BLUE, font=code_font)
    
    draw.line([55, 190, 515, 190], fill=BORDER_COLOR, width=1)
    draw.text((55, 202), "# 生成 MOSS-Image 原生单行布局 JSON (0.02s):", fill=TEXT_MUTED, font=zh_code_small)
    
    json_lines = [
        ('{"summary":{"meta":["photo"],"canvas":"single",', ACCENT_YELLOW),
        (' "caption":"realistic photo, full-body shot...', ACCENT_YELLOW),
        (' "items":[{"label":"character",', ACCENT_GREEN),
        ('  "bbox":[-500,-296,575,296],', (255, 120, 100)),
        ('  "caption":"kneeling and leaning forward on bed..."}],', ACCENT_GREEN),
        (' "bbox_coord_space":"abs_centralized"}', ACCENT_YELLOW)
    ]
    for line_idx, (text, col) in enumerate(json_lines):
        draw.text((55, 225 + line_idx * 21), text, fill=col, font=code_small)
        
    draw.rounded_rectangle([55, 365, 515, 518], radius=6, fill=CARD_BG, outline=BORDER_COLOR)
    draw.text((70, 380), "[!] 双层物理锁定核心优势：", fill=ACCENT_YELLOW, font=body_font)
    draw.text((70, 410), "1. 边界框 [-500,-296,575,296] 钉牢空间位置与画面比例", fill=TEXT_WHITE, font=small_font)
    draw.text((70, 435), "2. 逐关节解剖学英文描述锁死肢体力学结构，告别畸变", fill=TEXT_WHITE, font=small_font)
    draw.text((70, 460), "3. 原生单行纯文本，无需手动在网页界面繁琐拖拽拉框", fill=TEXT_WHITE, font=small_font)
    draw.text((70, 485), "4. 智能预留底部 4% 间隙，彻底根治脚踝裁断问题", fill=TEXT_WHITE, font=small_font)

    # Right: Coordinate visual box diagram
    draw.rounded_rectangle([550, 100, WIDTH - 40, 535], radius=10, fill=CARD_BG, outline=BORDER_COLOR)
    draw.text((570, 115), "画布坐标系可视化 (832×1248)", fill=TEXT_WHITE, font=body_font)
    
    c_x1, c_y1, c_x2, c_y2 = 620, 155, 840, 485
    draw.rectangle([c_x1, c_y1, c_x2, c_y2], outline=(100, 110, 120), width=2, fill=(18, 22, 28))
    mid_x = (c_x1 + c_x2) // 2
    mid_y = (c_y1 + c_y2) // 2
    draw.line([mid_x, c_y1, mid_x, c_y2], fill=(45, 55, 65), width=1)
    draw.line([c_x1, mid_y, c_x2, mid_y], fill=(45, 55, 65), width=1)
    draw.text((mid_x + 5, mid_y + 5), "(0, 0)", fill=TEXT_MUTED, font=code_small)
    
    bx1 = mid_x - int(296 * (220 / 832))
    bx2 = mid_x + int(296 * (220 / 832))
    by1 = mid_y - int(500 * (330 / 1248))
    by2 = mid_y + int(575 * (330 / 1248))
    draw.rectangle([bx1, by1, bx2, by2], outline=ACCENT_PINK, width=2)
    draw.text((bx1 + 8, by1 + 8), "character (跪趴姿势边界框)", fill=ACCENT_PINK, font=small_font)
    
    draw.text((595, 500), "底部预留 4% · 绝无截断", fill=ACCENT_GREEN, font=small_font)

    frames.append(img)

# -------------------------------------------------------------
# Stage 3: Echidna Workbench Execution (18 frames)
# -------------------------------------------------------------
for i in range(18):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, "Step 3/4 · Echidna 工作台一键粘贴与推理")
    
    draw.rounded_rectangle([40, 56, 175, 84], radius=6, fill=(31, 111, 235))
    draw.text((50, 62), "Echidna 在线工作台", fill=TEXT_WHITE, font=small_font)
    draw.text((190, 62), "OpenMOSS 5B SFT 原生扩散模型直推", fill=TEXT_MUTED, font=body_font)
    
    draw.rounded_rectangle([40, 100, WIDTH - 40, 535], radius=10, fill=CARD_BG, outline=BORDER_COLOR)
    
    # Workbench top bar
    draw.rectangle([40, 100, WIDTH - 40, 145], fill=(30, 36, 46))
    draw.text((60, 114), "Echidna 在线工作台", fill=TEXT_WHITE, font=header_font)
    draw.rounded_rectangle([250, 108, 410, 138], radius=6, fill=(40, 50, 65))
    draw.text((260, 116), "模型: MOSS-Image-SFT", fill=ACCENT_BLUE, font=small_font)
    draw.rounded_rectangle([425, 108, 535, 138], radius=6, fill=(40, 50, 65))
    draw.text((435, 116), "模式: 文生图", fill=ACCENT_GREEN, font=small_font)
    draw.rounded_rectangle([550, 108, 700, 138], radius=6, fill=(40, 50, 65))
    draw.text((560, 116), "底模: OpenMOSS 5B", fill=TEXT_MUTED, font=small_font)
    
    # Prompt input box
    draw.text((60, 162), "正向 Prompt 输入框 (整段粘贴单行 JSON):", fill=TEXT_MUTED, font=body_font)
    draw.rounded_rectangle([60, 188, WIDTH - 60, 275], radius=8, fill=CODE_BG, outline=ACCENT_GREEN)
    draw.text((75, 202), '{"summary":{"meta":["photo"],"canvas":"single","caption":"realistic photo, full-body shot,', fill=ACCENT_GREEN, font=code_font)
    draw.text((75, 226), ' kneeling and leaning forward on bed, hips tilted, arched back..."},"items":[...]}', fill=ACCENT_GREEN, font=code_font)
    draw.text((75, 252), '[OK] 原生单行 JSON 布局自动识别激活 (无需手动繁琐拖拽拉框)', fill=ACCENT_YELLOW, font=zh_code_small)
    
    # Parameters row
    draw.text((60, 292), "推荐高级推理参数：", fill=TEXT_MUTED, font=body_font)
    params = [("分辨率", "832×1248 (1M)"), ("采样步数", "50 步"), ("CFG 权重", "3.0"), ("采样器", "Euler"), ("负向跳层", "第 22 层 (关键)")]
    for p_idx, (p_name, p_val) in enumerate(params):
        px = 60 + p_idx * 165
        draw.rounded_rectangle([px, 318, px + 150, 378], radius=6, fill=CODE_BG, outline=BORDER_COLOR)
        draw.text((px + 12, 328), p_name, fill=TEXT_MUTED, font=small_font)
        draw.text((px + 12, 350), p_val, fill=TEXT_WHITE, font=body_font)
        
    # Progress bar
    draw.text((60, 408), "去噪生成进度：", fill=TEXT_MUTED, font=body_font)
    prog = min(1.0, (i + 1) / 17)
    bar_w = WIDTH - 120
    draw.rounded_rectangle([60, 438, 60 + bar_w, 468], radius=6, fill=CODE_BG, outline=BORDER_COLOR)
    draw.rounded_rectangle([60, 438, 60 + int(bar_w * prog), 468], radius=6, fill=ACCENT_GREEN)
    draw.text((WIDTH // 2 - 50, 445), f"{int(prog * 100)}% ｜ 约 35 秒", fill=TEXT_WHITE, font=small_font)
    
    draw.text((60, 492), "OpenMOSS 5B 潜空间扩散去噪完毕 · 正在输出毛孔级超清图像...", fill=ACCENT_YELLOW, font=body_font)

    frames.append(img)

# -------------------------------------------------------------
# Stage 4: Finished Ultra-HD Result (36 frames)
# -------------------------------------------------------------
crop_sample = sample_img.crop((0, 0, sample_img.width, sample_img.height))
aspect = crop_sample.width / crop_sample.height
target_h = 420
target_w = int(target_h * aspect)
sample_resized = crop_sample.resize((target_w, target_h), Image.Resampling.LANCZOS)

for i in range(36):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, "Step 4/4 · 8K 超清写实成品落地")
    
    draw.rounded_rectangle([40, 56, 175, 84], radius=6, fill=ACCENT_PINK)
    draw.text((50, 62), "实测成品效果", fill=TEXT_WHITE, font=small_font)
    draw.text((190, 62), "私房唯美跪趴 (glamour_bed_kneel) · 真实皮肤与反弓腰背", fill=TEXT_MUTED, font=body_font)
    
    draw.rounded_rectangle([40, 100, WIDTH - 40, 535], radius=10, fill=CARD_BG, outline=ACCENT_PINK)
    
    # Left sample image
    img_x = 65
    img_y = 107
    img.paste(sample_resized, (img_x, img_y))
    draw.rectangle([img_x, img_y, img_x + target_w, img_y + target_h], outline=BORDER_COLOR, width=2)
    
    # Right panel: Quality highlights
    rx = img_x + target_w + 35
    draw.text((rx, 120), "实测指标与骨骼吻合度全核验：", fill=TEXT_WHITE, font=header_font)
    
    checklist = [
        ("[OK] 骨骼完全锁定", "反弓腰背、双膝承重、眼神慵懒迷离精确复现"),
        ("[OK] 空间精准受控", "居中构图占画面88%，床品自然下陷褶皱"),
        ("[OK] 真实物理材质", "黑色亮面皮衣高光与酒红织物、金属心形腰链"),
        ("[OK] 毛孔级真实光学", "床头暖灯主光 + 细腻皮肤真实通透肌理"),
        ("[OK] 零肢体变形串色", "第 22 层跳层技术彻底杜绝多指/多肢/融色"),
        ("[OK] 单行 JSON 即用", "复制即出图，无需二次微调，彻底告别随机抽卡")
    ]
    
    for c_idx, (c_title, c_desc) in enumerate(checklist):
        cy = 160 + c_idx * 50
        draw.text((rx, cy), c_title, fill=ACCENT_GREEN if c_idx < 5 else ACCENT_YELLOW, font=body_font)
        draw.text((rx, cy + 22), c_desc, fill=TEXT_MUTED, font=small_font)
        
    draw.rounded_rectangle([rx, 472, WIDTH - 65, 510], radius=6, fill=(35, 134, 54))
    draw.text((rx + 35, 483), "开源项目：github.com/FizzEat/moss-image-pose", fill=TEXT_WHITE, font=body_font)

    frames.append(img)

# -------------------------------------------------------------
# Save frames & export via ffmpeg
# -------------------------------------------------------------
temp_dir = "/tmp/demo_frames_final"
shutil.rmtree(temp_dir, ignore_errors=True)
os.makedirs(temp_dir, exist_ok=True)

for idx, frame in enumerate(frames):
    frame.save(f"{temp_dir}/frame_{idx:03d}.png")

out_gif = os.path.join(REFERENCES_DIR, "demo_workflow.gif")
out_mp4 = os.path.join(REFERENCES_DIR, "demo_workflow.mp4")
palette = "/tmp/palette_workflow.png"

# High-quality palette with full statistics & Floyd-Steinberg dithering
os.system(f"ffmpeg -y -framerate 10 -i {temp_dir}/frame_%03d.png -vf 'palettegen=max_colors=256:stats_mode=full' {palette}")
os.system(f"ffmpeg -y -framerate 10 -i {temp_dir}/frame_%03d.png -i {palette} -lavfi 'paletteuse=dither=floyd_steinberg' {out_gif}")

# Ultra-crisp MP4 for video embedding / platforms
os.system(f"ffmpeg -y -framerate 10 -i {temp_dir}/frame_%03d.png -c:v libx264 -pix_fmt yuv420p -crf 18 {out_mp4}")

print("GIF generated at:", out_gif, f"({os.path.getsize(out_gif)} bytes)")
print("MP4 generated at:", out_mp4, f"({os.path.getsize(out_mp4)} bytes)")
