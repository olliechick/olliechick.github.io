import requests
import os 
from podcatcher import write_to_file, get_title

def main():
    
    print('Retrieving file...')
    
    url = 'https://pod.neocities.org/jmd.html'
    file = requests.get(url)
    com_file = file.text
    
    uncom_file = ''
    i = 0
    in_comment = False
    S = []
    
    print('Iterating through file...')
    
    while i < len(com_file):
        if not in_comment:
            if com_file[i:i+4] == '<!--':
                in_comment = True
                ##print('Comment', end = ' ')
                i += 3
            else:
                #if com_file[i:i+6] == '<item>':
                    #S.append('(')
                    #print('item', end = ' ')
                    #in_item = True
                #elif com_file[i:i+7] == '</item>':
                    #S.pop()
                    #print('done.')
                    #in_item = False
                uncom_file += com_file[i]
        elif in_comment and com_file[i:i+3] == '-->':
            in_comment = False
            ##print('done.')
            i += 2
        i += 1
            
    print('Done.')
    
    items = uncom_file.split('<item>')[1:]
            
    print('There are', len(items), 'items.')
    
    #write_to_file('uncommented file', uncom_file)
    
    valid_beginnings = [None]
    valid_endings = ['.mp3']
    
    urls = [None] * len(items)
    
    j = 0
    for item in items:
        line = item
        i = 0
        while i < len(item) and urls[j] == None:
            #print(i, line[i])
            if (i <= len(line)-7 and line[i:i+7] == 'http://') or (i <= len(line)-8 and line[i:i+8] == 'https://'):
                ##print('found url')
                url = ''
                wanted = False
        
                #find ending char
                if i>0:
                    starting_char = line[i-1]
                    if starting_char == '>':
                        ending_char = ['<']
                    else:
                        ending_char = [starting_char]
                else:
                    ending_char = [' ', '	', '\n']
                
                #goes through characters until ending character
                while i < len(line) and line[i] not in ending_char:
                    url += line[i]
                    i += 1
                    
                #check if it's a wanted url
                #must have at least one of the valid 
                # Note that the last valid page redirected to is chosen
                for valid_beginning in valid_beginnings:
                    if valid_beginning is not None and line[i:i+len(valid_beginning)] == valid_beginning:
                        wanted = True
                for valid_ending in valid_endings:
                    if valid_ending is not None and url[-len(valid_ending):] == valid_ending:
                        wanted=  True
                            
                if wanted:
                    urls[j] = url
            i += 1
        j += 1
        
    titles = [get_title(url)[0] + '.' + get_title(url)[1] for url in urls]
              
    #i = 0
    #for url in urls:
        #print(i, url, get_title(url)[0])
        #i += 1
        
    directory = 'C:\\Users\\ollie\\Documents\\Archives\\Podcasts\\Jay-Jay, Mike & Dom'
                    
    i = 0
    for title in titles:
        print(i, title, end = ' ')
        if os.path.isfile(directory + '\\' + title):
            #already exists
            print()
        else:
            print("DOES NOT EXIST!")
            print(urls[i])
        i += 1
        
def find_final_URLs(url_list):
    '''prints out the final urls from a list of urls'''
    for url in url_list:
        response = requests.get(url)
        print(response.url)        
    
        
url_list = ['https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/Mad09gogirlsjay.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_Usher.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/thursdayjuly17.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_AprilPhilsDay.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_InappropriateGifts.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_TaioCruz.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_StevePrice.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_AnikaMoa.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_NikeAd.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_OnaBreak.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_BoxingGloves.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_Scribe.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_WhattayaWantForTea.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_BrookeHowardSmith.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_April20.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_April21.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_Accupuncture.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_PaulyShore.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_Biebwatch.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/TheEdge/JMD10_JustinBieber.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/TheEdge/JMD10_April30th.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_ANTMWinner.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_TradeRage.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_ChanginBP.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_RoryFallon.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_Zumba.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_SaraTetro.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_AllWhitesBingo.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_May12th.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_May13th.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_KnifeThrowing.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_HugaGinga.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_May27th.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_HAGD.mp3', 'https://web.archive.org/http://podcast.mediaworks.co.nz/theedge/JMD10_May31st.mp3']

    
#main()
find_final_URLs(url_list)