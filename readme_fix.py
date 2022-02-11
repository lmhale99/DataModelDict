with open('top_of_README.rst', 'r', encoding='UTF-8') as f:
    content = f.read()

with open('README.rst', 'r', encoding='UTF-8') as f:
    content += f.read()

with open('README.rst', 'w', encoding='UTF-8', newline='\n') as f:
    f.write(content)

