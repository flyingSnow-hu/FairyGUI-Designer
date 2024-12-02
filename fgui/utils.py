import hashlib


def get_id_hash(id_str:str):
    return f'f{id_str.replace(':','s')}{'x' * (7-len(id_str))}'

def to_hex(r, g, b, a):
    return f'#{c2x(a)}{c2x(r)}{c2x(g)}{c2x(b)}'

def c2x(color):
    # 将小数颜色值乘以 255 并转换为整数
    color_int = int(color * 255)
    # 将整数转换为十六进制字符串
    color_hex = hex(color_int)[2:].lower()
    # 如果十六进制字符串只有一位，则在前面补零
    if len(color_hex) == 1:
        color_hex = '0' + color_hex
    return color_hex

def get_part_before_colon(string):
    parts = string.split(':', 1)
    if len(parts) > 0:
        return parts[0]
    else:
        return string

if __name__ == '__main__':
    print(to_hex(0.85, 0.85, 0.85, 1))