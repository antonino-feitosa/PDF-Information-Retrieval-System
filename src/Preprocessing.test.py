
import re

test = '''
Example 1 http://www.businesswire.com/news/home/20210217005928/en.-AAAAA-santaclara
Example 2 text1 text2 http://url.com/bla1/blah1/ text3 text4 http://url.com/bla2/blah2/ text5 text6
Example 3 this is a test https://sdfs.sdfsdf.com/sdfsdf/sdfsdf/sd/sdfsdfs?bob=%20tree&jef=man lets see this too https://sdfsdf.fdf.com/sdf/f end
Example 4 "this https://sdfs-sdfsdf.com yo")) -> this is a test -sdfsdf.com yo
'''

result = re.sub(r'\S*https?:\S*', '', test)
print(result)
