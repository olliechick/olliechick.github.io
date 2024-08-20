""" Takes a file (chosen in main) and replaces stuff with stuff.
    For further detail, see the function nicely_format(s).
"""

def extract_str(filename):
    """returns a (stripped) string from file"""
    file = open(filename, 'r')
    s = file.read()
    file.close()
    s.strip()
    return s   

def write_to_file(filename, contents):
    
    outfile = open(filename, 'w')
    outfile.write(contents)
    outfile.close()

def nicely_format(s):
    """Adds a newline after every </item>
       Then returns the new string."""
    output = ''
    i = 0
    while i < len(s):
        c = s[i]
        if c == '<' and s[i+1:i+7] == '/item>':
            output += '</item>\n'
            i += 7
        else:
            output += c
            i += 1
    
    return output    

def main():
    filename = 'm.txt'
    output_filename = 'output.txt'
    
    s = extract_str(filename)
    
    output = nicely_format(s)
    
    write_to_file(output_filename, output)
    
main()