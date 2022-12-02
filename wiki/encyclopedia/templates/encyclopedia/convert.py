import markdown
path = '/home/chimchimster/Downloads/wiki/wiki/entries/'
entries_list = ['CSS.md', 'Django.md', 'Git.md', 'HTML.md', 'Python.md']

for file in entries_list:
    with open(path + file, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)

    with open(file[:3]+'.html', 'w') as f:
        f.write(html)

