from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

def delta_e(hex1, hex2):
    rgb1: LabColor = convert_color(sRGBColor.new_from_rgb_hex(hex1), LabColor)
    rgb2: LabColor = convert_color(sRGBColor.new_from_rgb_hex(hex2), LabColor)
    return delta_e_cie2000(rgb1, rgb2)
