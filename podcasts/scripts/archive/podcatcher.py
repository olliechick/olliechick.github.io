"""
Extracts all URLS from a given site, and does stuff with them.
To set the valid extensions, change line 405 (valid_endings in generate_MP3_list()).
"""

import requests
import urllib.request
import os
import sys
import time

As = '==================== LOOK AT THIS -->'
Am = '<-- ====== -->'
Ae = '<-- THIS ==============='
OUTPUT_FILE = 'output'
num_of_items = 0

def write_to_file(filename, contents):
    
    outfile = open(filename, 'w')
    outfile.write(contents)
    outfile.close()
    
def append_to_file(filename, contents):
    file = open(filename, 'a')
    file.write(contents)
    file.close()
    
def println(*args, end = '\n'):
    ##print(As, end, Ae)
    ##print(args, end)
    for arg in args[:-1]:
        print(str(arg), end = ' ')
        append_to_file(OUTPUT_FILE, str(arg) + ' ')
    if len(args) == 0:
        print('', end = end)
        append_to_file(OUTPUT_FILE, end)
    else:
        print(args[-1], end = end)
        append_to_file(OUTPUT_FILE, str(args[-1]) + end)
    
def inputln(s):
    response = input(s)
    append_to_file(OUTPUT_FILE, str(s) + response)
    append_to_file(OUTPUT_FILE, '\n')
    return response
    
def setup():
    write_to_file(OUTPUT_FILE, '')
        
    
def list_to_strln(alist):
    strln = ''
    for item in alist:
        try:
            strln += item.strip() + '\n'
        except:
            strln += str(item) + '\n'
    strln.strip()
    return strln


def extract_str(filename):
    """returns a (stripped) string from file"""
    file = open(filename, 'r')
    s = file.read()
    file.close()
    s.strip()
    return s   


def download_file(file_URL, filename):
    sys.stdout.flush() #finish printing stuff before starting download
    try:
        start_time = time.clock()
        urllib.request.urlretrieve(file_URL, filename)
        total_time = time.clock() - start_time
    except:
        println("(error downloading file)")
    else:
        minutes = total_time//60
        seconds = total_time - minutes*60
        println('({0:.0f} minutes, {1:.0f} seconds)'.format(minutes, seconds))
    

    
def generate_contents(file, valid_ends, text_template, headings, traverse):
    global num_of_items
    wanted_urls = []
    wanted_full_urls = []
    invalid_urls = []
    invalid_full_urls = []
    failed_urls = []
    failed_full_urls = []
    wanted_urls_outside_item = []
    wanted_full_urls_outside_item = []
    
    valid_beginnings, valid_endings = valid_ends
    outside_item_heading, invalid_heading, failed_heading, footer = headings
    
    in_comment = False
    in_item = False
    wanted = False
    
    
    for line in file.text.split('\n'):
        if len(line) < 3:
            #nothing useful in here
            println(line)
            
        i=0        
        while i <= len(line)-3: # while i is not the last or second to last char of the line
            is_a_url = False
            failed_request = False
            
            # if it's starting a comment
            if not in_comment and (i <= len(line)-4 and line[i:i+4] == '<!--'):
                in_comment = True
                println('\n<COMMENT>\n', end='\n<!--')
                i += 4
                comment = ''
                while i < len(line) and line[i:i+3] != '-->':
                    comment += line[i]
                    i += 1
                if i == len(line):
                    #not ending a comment on the same line
                    println(comment)
            
            # if it's in a comment
            elif in_comment:
                pass
                #UNCOMMENT THIS IS YOU WANT TO SEE THE COMMENTS
                comment = ''
                while i < len(line) and line[i:i+3] != '-->':
                    comment += line[i]
                    i += 1
                if line[i:i+3] != '-->':
                    #not about to end comment
                    println(comment)
                
            # if it's ending a comment
            if in_comment and line[i:i+3] == '-->':
                in_comment = False
                println(comment + '-->\n\n</COMMENT>\n')
            
            # if it's starting an item
            elif not in_comment and i <= len(line)-6 and line[i:i+6] == '<item>':
                in_item = True
                num_of_urls_in_item = 0
                num_of_items += 1
                
            # if it's ending an item    
            elif in_item and i <= len(line)-7 and  line[i:i+7] == '</item>':
                in_item = False
                if num_of_urls_in_item == 0:
                    println("NO URLS IN ITEM.")
                
            
            # if it's a url
            elif (i <= len(line)-7 and line[i:i+7] == 'http://') or (i <= len(line)-8 and line[i:i+8] == 'https://' and i >= 16 and line[i-16:i] == '<enclosure url="'): 
                #REMOVE LAST AND STATEMENT IF YOU DON'T CARE ABOUT ENCLOSURE URL
                ##println("Found a URL!")
                is_a_url = True
                url = ''
        
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
                    
                if traverse:
                    #get the url, and the entire redirect path - stored in urls
                    ##println(url)
                    urls = []
                    try:
                        response = requests.get(url)
                        for resp in response.history:
                            urls.append(resp.url)
                        urls.append(response.url)
                    except:
                        failed_request = True
                        wanted = False
                        #check if it's a wanted url
                        #must have at least one of the valid 
                        # Note that the last valid page redirected to is chosen
                        for valid_beginning in valid_beginnings:
                            if valid_beginning is not None and line[i:i+len(valid_beginning)] == valid_beginning:
                                wanted = True
                        for valid_ending in valid_endings:
                            if valid_ending is not None and url[-len(valid_ending):] == valid_ending:
                                wanted = True 
                        
                        ##println('failed')
                else:
                    #don't bother finding redirects etc
                    urls = [url]
                    
                best_url = None
                for url in urls:
                               
                    ##println(url, end=' '*15)
                    
                    #check if it's a wanted url
                    #must have at least one of the valid 
                    # Note that the last valid page redirected to is chosen
                    for valid_beginning in valid_beginnings:
                        if valid_beginning is not None and line[i:i+len(valid_beginning)] == valid_beginning:
                            best_url = url
                    for valid_ending in valid_endings:
                        if valid_ending is not None and url[-len(valid_ending):] == valid_ending:
                            best_url = url  
                            
                if best_url:
                    url = best_url
                elif not failed_request:
                    #no good url
                    if len(urls) == 1:
                        url = urls[0]
                    else:
                        #redirections
                        url = (urls[0], urls[-1])
                        
                #Extract the title (extension is not used)
                title, extension = get_title(url)  
                
                if best_url and in_item and not failed_request and url not in wanted_urls:
                    num_of_urls_in_item += 1
                
                #Append url and full_url to appropriate list
                if wanted and failed_request and (url not in failed_urls): #failed
                    number=len(failed_urls)
                    full_url = text_template.format(url=url,title=title,number=number) + '\n'
                    failed_urls.append(url)
                    println('Failed URL found:', url)
                    failed_full_urls.append(full_url)                    
                    
                elif best_url and (url not in wanted_urls): #normal
                    number = len(wanted_urls)
                    full_url = text_template.format(url=url,title=title,number=number) + '\n'
                    wanted_urls.append(url)
                    println('URL found:', url)
                    wanted_full_urls.append(full_url)
                    if in_item and num_of_urls_in_item >= 2:
                        println("THAT WAS AN EXTRA URL!")
                        # REMOVE THIS IF YOU WANT EXTRA URLS:
                        wanted_urls.pop()
                        wanted_full_urls.pop()
                        
                elif url and not best_url and (url not in invalid_urls): #invalid
                    number=len(invalid_urls)
                    full_url = text_template.format(url=url,title=title,number=number) + '\n'
                    invalid_urls.append(url)
                    println('Invalid URL found:', url)
                    invalid_full_urls.append(full_url)
                    
                    
                        
            i+=1
                
    output = list_to_strln(wanted_full_urls)
    output += outside_item_heading
    output += list_to_strln(wanted_full_urls_outside_item)
    output += invalid_heading
    output += list_to_strln(invalid_full_urls)
    output += failed_heading
    output += list_to_strln(failed_full_urls)
    output += footer
    return output

def create_url_list(online=True, url='', output_file='output.txt',
                    text_template='', valid_ends = ([''], None), 
                    headings = ('\nOutside items\n', '\nInvalid URLs\n', '\nFailed URLs\n', ''), traverse = True):
    
    full_valid_beginnings = []
    valid_beginnings, valid_endings = valid_ends
    
        
    for valid_beginning in valid_beginnings:
        if valid_beginning is not None:
            full_valid_beginnings += ['http://'+valid_beginning, 'https://'+valid_beginning]
        
    valid_ends = full_valid_beginnings, valid_endings
    
    # Webpage
    if online:
        while url == '':
            url = inputln("Enter URL: ")
        
        try:
            file = requests.get(url)
        except:
            println("Error, couldn't get webpage at " + url)
        else:
            println('Connection successful.')
            contents = generate_contents(file, valid_ends, text_template, headings, traverse)
            write_to_file(output_file, contents)
            println('Generation complete.')    
        
    # Local file
    else:
        file = open(url, 'r')
        s = file.read()
        file.close()
        file.text = s
        contents = generate_contents(file, valid_ends, text_template, headings, traverse)
        write_to_file(output_file, contents)
        println('Generation complete.')    
        
        
        
        
def generate_podcast_feed():
    
    #online = True
    #url = 'https://pod.neocities.org/gsc.html'
    
    online = False
    url = 'Feeds/JMD.html'
    
    output_file = 'output.html'
    
    #text_template = '<a href="https://web.archive.org/save/{url}">link {number}: {url}</a><br/>'
    #text_template = 'https://web.archive.org/save/{url}\n'
    text_template = '{url}<br />'
    #text_template = """

#<item>
 #<title>{title}</title>
 #<guid>https://web.archive.org/{url}</guid>
 #<itunes:summary>{title}</itunes:summary>
 #<description>{title}</description>
 #<enclosure url="https://web.archive.org/{url}" length="17680040" type="audio/mpeg"/>
 #<category>Arts &amp; Entertainment</category>
 #<pubDate> ,  Dec 2013 10:00:00 +1200</pubDate>
#</item>"""   
    #text_template = """

#<item>
#<title>Sharyn &amp; Guy's podcast for day December </title>
 #<guid>{url}</guid>
 #<itunes:summary></itunes:summary>
 #<description></description>
 #<enclosure url="{url}" length="17680040" type="audio/mpeg"/>
 #<category>Arts &amp; Entertainment</category>
 #<pubDate> ,  Dec 2013 10:00:00 +1200</pubDate>
#</item>"""

    valid_beginnings =  ['web.archive.org/']
    #valid_beginnings = [None]#['podcast.mediaworks.co.nz/', 'audio.mediaworks.nz/', 'feeds.feedburner.com/~r']
    valid_endings = ['.mp3']
    
    valid_ends = valid_beginnings, valid_endings
    
    outside_item_heading = '<!--\n\n==Valid URLs outside item==\n\n'    
    invalid_heading = '\n\n==Invalid URLs==\n\n'
    failed_heading = '\n\n==Failed URLs==\n\n'
    footer = '-->'
    
    headings = outside_item_heading, invalid_heading, failed_heading, footer    
    traverse = False
    
    create_url_list(online, url, output_file, text_template, valid_ends, headings, traverse)
    
    
def generate_MP3_list(online, url, output_file, traverse):
    '''Takes the webpage at url (or local file if online = False), 
       and generates a list of MP3 links at output_file.
    '''
    text_template = '{url}<br />'
    
    valid_beginnings = [None]
    valid_endings = ['.mp3']
    valid_ends = valid_beginnings, valid_endings
    
    outside_item_heading = '\n<h2>Valid URLs outside item</h2>\n'
    invalid_heading = '\n<h2>Invalid URLs</h2>\n'
    failed_heading = '\n<h2>Failed URLs</h2>\n'
    footer = ''
    
    headings = outside_item_heading, invalid_heading, failed_heading, footer
    
    println('Generating URL list.')
    create_url_list(online, url, output_file, text_template, valid_ends, headings, traverse)
    
        
        
def download_files_from_URL(feed_url, directory, treat_dupes, test_mode, traverse):
    '''Analyses the feed at feed_url, exports the URL list to a file (this
       file is named the title of the feed+.html), and downloads each file
       at the valid URLs to the directory.
    '''
    
    if test_mode:
        online = False
        output_file = 'test output.html'
        generate_MP3_list(online, feed_url, output_file, traverse)    
    else:
        online = True
        title, extension = get_title(feed_url)
        try:
            write_to_file(title + '.html', '')
        except:
            title = 'my file'
        output_file = title + '.html'
     
        if inputln("Generate list from feed (y/n)? ") == 'y':
            generate_MP3_list(online, feed_url, output_file, traverse)
    
    MP3_list_string = extract_str(output_file)
    urls = MP3_list_string.split('\n<h2>')[0].split('<br />\n')[:-1]
    
    println('URLs to download:')
    i = 0
    for url in urls:
        println(i, url)
        i+=1;
    println()
        
    i = 0
    for url in urls:
        title, extension = get_title(url)
        ##println(As, url, Am, title, Am, extension, Ae) 
        filename = title + '.' + extension
        println('Downloading file {}: {}'.format(i, filename), end = ' ')
        
        filedir = directory + '/' + filename
        
        if os.path.exists(directory):
            #directory exists, so some of the files may exist
            if os.path.isfile(filedir):
                #this file already exists
                if treat_dupes == 'number':
                    j = 0
                    while os.path.isfile(directory + '/' + title + ' ({}).'.format(j) + extension):
                        j += 1
                    download_file(url, directory + '/' + title + ' ({}).'.format(j) + extension)
                elif treat_dupes == 'ignore':
                    println('(ignored)')
                elif treat_dupes == 'overwrite':
                    download_file(url, filedir)
            else:
                #file doesn't exist
                download_file(url, filedir)
        else:
            #directory doesn't exist - create it
            #obviously files downloaded can't overwrite anything
            os.makedirs(directory)
            download_file(url, filedir)
                
        
        i+=1
        
    println('Done.')



def download_podcasts():
    '''Downloads all the podcast episodes from feed_url to directory'''
    global num_of_items
    
    user_input = extract_str('input.txt')
    test_modeRESP, feed_url, directory, treat_dupes, traverseRESP = user_input.split('\n')[:5]
    
    test_mode = test_modeRESP == 'y'
        
    if test_mode:
        feed_url = 'test.txt'
        directory = 'Testing'
        treat_dupes = 'number'
        traverse = True
    else:
        traverse = traverseRESP == 'y'
        
    download_files_from_URL(feed_url, directory, treat_dupes, test_mode, traverse)
    println(num_of_items)
    
    

def main():
    
    setup() #for writing println() and inputln() to output
    
    #Pick one:
    # generate_podcast_feed()
    download_podcasts()
      
      
 
if __name__  ==  "__main__":
    main()