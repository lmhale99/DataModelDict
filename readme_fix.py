# Standard Python libraries
from __future__ import print_function, unicode_literals
import io

with io.open('README.rst', 'r', encoding='UTF-8') as f:
    content = f.read()

start = 0
end = 0
count = 0
while count < 100:
    try:
        start = content[end:].index('(') + end
        end = content[start:].index(')') + start
        #print(start, end)
    except:
        break
    else:
        count += 1
        old = content[start:end]
        new = content[start:end].replace('**', '')
        if len(old) != len(new):
            content = content[:start] + new + content[end:]
            end = end - (len(old) - len(new))

with io.open('README.rst', 'w', encoding='UTF-8', newline='\n') as f:
    f.write(content)

