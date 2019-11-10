import  xml.dom.minidom

#打开xml文档
dom = xml.dom.minidom.parseString('test.xml')

#得到文档元素对象
root = dom.documentElement
sets = root.getElementsByTagName('set')
for item in sets:
    value = item.getAttribute('value')
    date = item.getAttribute('hoverText')
    print(f'date: {date}, value: {value}')
