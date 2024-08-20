filename = 'output.html'

file = open(filename, 'r')
s = file.read()
file.close()

s = s.split('<!--')[0].split('\n')
o = ''

i = 0
for l in s:
    if i%20 == 0:
        #every 20 items
        o += '\n\t\t\tGroup '+str(i//20)+'\n'
    o += l + '\n'
    i += 1
    
print(o)