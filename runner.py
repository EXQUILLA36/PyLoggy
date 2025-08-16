import marshal
import types

with open("DevelopmentTest.cpython-313.pyc", "rb") as f:
    f.read(16)  # skip .pyc header
    code = marshal.load(f)

exec(code)
