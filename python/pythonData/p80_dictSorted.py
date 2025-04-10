worldinfo = {'세탁기':50, '선풍기':30, '냉장고':60}
print(worldinfo)

myxticks = sorted(worldinfo, key=worldinfo.get, reverse=True)
print(myxticks)

reverse_key = sorted(worldinfo.keys(), reverse=True)
print(reverse_key)

chardata = sorted(worldinfo.values(), reverse=True)
print(chardata)

