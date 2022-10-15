from PIL import Image, ImageDraw, ImageFont
import kusodekaSettings
import numToAlpha
import csv


def draw_transparent_text(src_canvas, text, pos, font, fill, alpha):
    mask = Image.new("L", src_canvas.size, 1)
    text_canvas = Image.new("RGB", src_canvas.size, "#000000")
    text_canvas.putalpha(mask)

    draw = ImageDraw.Draw(text_canvas)
    draw.text(pos, text, font=font, fill=fill)
    del draw

    src_canvas.putalpha(mask)
    return Image.blend(src_canvas, text_canvas, alpha).convert("RGB")


if __name__ == '__main__':
    print("Program Start")
    # マップサイズ読込
    with open(kusodekaSettings.mapFile, encoding="utf_8") as f:
        reader = csv.reader(f)
        l = [row for row in reader]

    # print(len(l))
    # print(len(l[0]))
    xMax = len(l[0])
    yMax = len(l)
    cellSize = 600
    midashiSize = 150
    xSize = xMax * cellSize + midashiSize
    ySize = yMax * cellSize + midashiSize
    lineWidth = 15
    fontsize = 120

    im = Image.new('RGB', (xSize, ySize), (255, 255, 255))
    backgrouwnIm = Image.open(kusodekaSettings.backgroundImg)
    im.paste(backgrouwnIm, (midashiSize, midashiSize))
    draw = ImageDraw.Draw(im)
    draw.line((0, 0, 0, ySize), fill=(0, 0, 0), width=lineWidth)
    draw.line((0, 0, xSize, 0), fill=(0, 0, 0), width=lineWidth)
    font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', fontsize)

    # 升目描画
    for x in range(xMax + 1):
        xZahyo = x * cellSize + midashiSize
        draw.line((xZahyo, 0, xZahyo, ySize), fill=(0, 0, 0), width=lineWidth)

    for y in range(yMax + 1):
        yZahyo = y * cellSize + midashiSize
        draw.line((0, yZahyo, xSize, yZahyo), fill=(0, 0, 0), width=lineWidth)

    # 文字描画
    num = 1
    for x in range(xMax):
        xPoint = midashiSize + (cellSize / 2) + (x * cellSize)
        yPoint = midashiSize / 2
        w, h = draw.textsize(str(num), font)
        # print(w)
        # print(h)
        draw.text((xPoint - (w / 2), yPoint - (h / 2) - 12), str(num + kusodekaSettings.startZahyoX), fill=(0, 0, 0), font=font)
        num = num + 1

    num = 1
    for y in range(yMax):
        xPoint = (midashiSize / 2)
        yPoint = midashiSize + (cellSize / 2) + (y * cellSize)
        alphaNum = numToAlpha.numToAlphaOne(num + kusodekaSettings.startZahyoY)
        w, h = draw.textsize(alphaNum, font)
        draw.text((xPoint - (w / 2), yPoint - (h / 2) - 12), alphaNum, fill=(0, 0, 0), font=font)
        num = num + 1

    # 地形読込
    for y in range(yMax):
        for x in range(xMax):
            cellFontsize = 600
            font = ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc', cellFontsize)
            mapText = l[y][x]
            w, h = draw.textsize(mapText, font)
            xPoint = midashiSize + (cellSize / 2) + (x * cellSize)
            yPoint = midashiSize + (cellSize / 2) + (y * cellSize)
            xPoint2 = xPoint - (w / 2)
            yPoint2 = yPoint - (h / 2) - 90
            draw.text((xPoint - (w / 2), yPoint - (h / 2) - 90), mapText, fill=(0, 0, 0), font=font)

    im.save(kusodekaSettings.outputImg)
    print("Program End")