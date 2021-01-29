import xml.etree.ElementTree as ET

data='''
<user>
   <name>J</name>
   <ph type="int">
   999999
   </ph>
   <email hide="Yes"/>
</user>'''

tree=ET.fromstring(data)
print('name',tree.find('name').text)
print('attr',tree.find('email').get('hide'))