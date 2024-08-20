months = [('Jan', '01'), ('Feb', '02'), ('Mar', '03'), ('Apr', '04'), ('May', '05'), ('June', '06'), ('July', '07'), ('Aug', '08'), ('Sep', '09'), ('Oct', '10'), ('Nov', '11'), ('Dec', '12')]

for month, num in months:
    print(month)
    for i in range(1,32):
        if i < 10:
            i = '0' + str(i)
        print('http://podcast.mediaworks.co.nz/TheEdge/Audio/GuySharynClint/GSC_'+str(i)+num+'16_podcast.mp3')
    print()