import xmltodict

d = dict()
with open('samples/sample_1.xml') as f:
    d = xmltodict.parse(f.read())

print(d)
pass