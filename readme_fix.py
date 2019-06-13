
with open('README.rst', 'rb') as f:
    content = f.read()

start = 0
end = 0
count = 0
while count < 100:
    try:
        start = content[end:].index(b'(') + end
        end = content[start:].index(b')') + start
        #print(start, end)
    except:
        break
    else:
        count += 1
        old = content[start:end]
        new = content[start:end].replace(b'**', b'')
        if len(old) != len(new):
            content = content[:start] + new + content[end:]
            end = end - (len(old) - len(new))

with open('README.rst', 'wb') as f:
    f.write(content)

