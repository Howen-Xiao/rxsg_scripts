def str2hex(s):
    # s: '0x4B'
    s = s[2:]   # 去掉’0x‘
    odata = 0
    su = s.upper()
    for c in su:
        tmp = ord(c)    # ACSII码
        if tmp <= ord('9') :
            odata = odata << 4  # 高位的数值乘以2^4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata

data = str2hex("0x00048a")
print("%#x"%data)