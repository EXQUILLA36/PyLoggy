import base64

encoded = "WzExOjI1OjMzXSBLZXk6IEtleS5zaGlmdApbMTE6MjU6MzNdIEtleTogS2V5LnNoaWZ0ClsxMToyNTozM10gS2V5OiBLZXkuc2hpZnQKWzExOjI1OjMzXSBLZXk6IEtleS5zaGlmdApbMTE6MjU6MzNdIEtleTogS2V5LnNoaWZ0ClsxMToyNTozM10gS2V5OiBLZXkuc2hpZnQKWzExOjI1OjMzXSBLZXk6IEtleS5zaGlmdApbMTE6MjU6MzNdIEtleTogS2V5LnNoaWZ0ClsxMToyNTozM10gS2V5OiBLZXkuc2hpZnQKWzExOjI1OjMzXSBLZXk6IEtleS5zaGlmdApbMTE6MjU6MzNdIEtleTogS2V5LnNoaWZ0ClsxMToyNTozM10gS2V5OiBLZXkuc2hpZnQKWzExOjI1OjMzXSBLZXk6IEtleS5zaGlmdApbMTE6MjU6MzNdIEtleTogS2V5LnNoaWZ0ClsxMToyNTozM10gS2V5OiBYClsxMToyNTozM10gS2V5OiBTClsxMToyNjowMF0gS2V5OiBLZXkuY3RybF9sCg=="
decoded_bytes = base64.b64decode(encoded)

try:
    decoded_text = decoded_bytes.decode('utf-8')
except UnicodeDecodeError:
    # fallback: decode with 'latin1' or ignore errors
    decoded_text = decoded_bytes.decode('latin1')
    # or: decoded_text = decoded_bytes.decode('utf-8', errors='ignore')

print(decoded_text)
