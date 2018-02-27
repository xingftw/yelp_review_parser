#
# a = 'python'
# print('python'[0:-2])
#
# f = open('scores.txt','r')
# L = []
# for line in f:
#     L = L + map(float,str.split(line[:-1],','))
# print(L)
#
# reduce()

a =  [[240, 240, 239],
      [250, 249, 237],
      [242, 239, 237],
      [240, 234, 233]]
print(zip(a))

print(zip(*a))