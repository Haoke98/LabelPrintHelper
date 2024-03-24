import os.path
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
import math

# A4纸的尺寸，单位是像素
A4_SIZE = (2480, 3508)

CORNER_RADIUS = 45
COLUMN_COUNT = 2
ROW_COUNT = 5

LABEL_MARGIN = 10
HORIZONTAL_MARGIN = LABEL_MARGIN
VERTICAL_MARGIN = LABEL_MARGIN

# 标签的尺寸和样式
LABEL_WIDTH = A4_SIZE[0] / COLUMN_COUNT - HORIZONTAL_MARGIN
LABEL_HEIGHT = A4_SIZE[1] / ROW_COUNT - VERTICAL_MARGIN

# 字体设置
font1 = ImageFont.truetype("/Users/shadikesadamu/Library/Fonts/simkai.ttf", 64)
font2 = ImageFont.truetype("/Users/shadikesadamu/Library/Fonts/simkai.ttf", 104)
font3 = ImageFont.truetype("/Users/shadikesadamu/Library/Fonts/simkai.ttf", 160)


# 生成标签的函数
def create_label(draw, x, y, label_text):
    # 绘制圆角矩形
    draw.rounded_rectangle([x, y, x + LABEL_WIDTH, y + LABEL_HEIGHT], 45, outline="black")
    # 由于无法使用textsize，手动计算文本位置
    # 绘制文本
    label_start = x + LABEL_WIDTH * 0.1
    value_start = x + LABEL_WIDTH * 0.7
    label_align = "left"
    value_align = "center"
    label_anchor = None
    value_anchor = "mm"
    draw.text((label_start, y + LABEL_HEIGHT * 0.1), "单位名称:", fill="gray", font=font1, anchor=label_anchor,
              align=label_align)
    draw.text((value_start, y + LABEL_HEIGHT * 0.15), "Demo公司", fill="black", font=font2, anchor="mm",
              align=value_align)
    start_point = (x + LABEL_WIDTH * 0.1, y + LABEL_HEIGHT * 0.3)
    end_point = (x + LABEL_WIDTH * 0.9, y + LABEL_HEIGHT * 0.3)
    draw.line((start_point, end_point), fill="gray", width=8)
    draw.text((label_start, y + LABEL_HEIGHT * 0.4), "编号:", fill="gray", font=font1, anchor=label_anchor,
              align=label_align)
    draw.text((value_start, y + LABEL_HEIGHT * 0.45), label_text, fill="black", font=font3, anchor="mm",
              align=value_align)
    draw.text((label_start, y + LABEL_HEIGHT * 0.6), "使用部门:", fill="gray", font=font1, anchor=label_anchor,
              align=label_align)
    draw.text((value_start, y + LABEL_HEIGHT * 0.65), "技术部", fill="gray", font=font1, anchor="mm", align=value_align)
    draw.text((label_start, y + LABEL_HEIGHT * 0.8), "固定资产名称:", fill="gray", font=font1, anchor=label_anchor,
              align=label_align)
    draw.text((value_start, y + LABEL_HEIGHT * 0.85), "高性能弹性服务器", fill="gray", font=font1, anchor="mm",
              align=value_align)
    # text_x = x + (LABEL_WIDTH / 3) * 2
    # text_y = y + (LABEL_HEIGHT / 3) * 2
    # draw.text((text_x, text_y), label_text, fill="gray", font=font, anchor="mm")
    # draw.text((text_x, text_y), "公共资产", fill="black", font=font, anchor="mm")


def generate_labels():
    room_index = [1, 2]
    cabinet_index = [1, 10]
    slot_index = [1, 10]
    res = []
    for room in range(room_index[0], room_index[1] + 1):
        for cabinet in range(cabinet_index[0], cabinet_index[1] + 1):
            for slot in range(slot_index[0], slot_index[1] + 1):
                res.append(f"S{room}{str(cabinet).zfill(2)}{str(slot).zfill(2)}")
    return res


if __name__ == '__main__':
    output_dir = os.path.join("output", datetime.now().strftime("%Y%m%d-%H%M"))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 计算每行可以放置多少个标签
    per_page_max_cols = COLUMN_COUNT
    per_page_max_rows = ROW_COUNT
    per_page_max_count = per_page_max_rows * per_page_max_cols
    print(f"Per Page:{per_page_max_rows}x{per_page_max_cols}={per_page_max_count}")
    # 创建标签
    labels = generate_labels()
    # 创建一个A4大小的白色画布
    image = None
    draw = None
    for i, label in enumerate(labels):
        page = i // per_page_max_count
        if i % per_page_max_count == 0:
            # 显示图片
            if image is not None:
                image.save(os.path.join(output_dir, f"{page}.png"), "PNG")
                if page == 1:
                    image.show()
                    a = input("继续生成吗?")
                    print("Input:", a)
            print("Page {0}".format(page))
            # 创建一个A4大小的白色画布
            image = Image.new("RGBA", A4_SIZE)
            draw = ImageDraw.Draw(image)
            # draw.text((1240, 3480), f"Page {page}", fill="black", font=font, anchor="mm")
        col = i % per_page_max_cols
        row = (i - (page * per_page_max_count)) // per_page_max_cols
        print(" " * 10, f"{i}", "-" * 10, row, col, label)
        x = col * (LABEL_WIDTH + LABEL_MARGIN) + LABEL_MARGIN
        y = row * (LABEL_HEIGHT + LABEL_MARGIN) + LABEL_MARGIN
        create_label(draw, x, y, label)
    page += 1
    image.save(os.path.join(output_dir, f"{page}.png"), "PNG")
