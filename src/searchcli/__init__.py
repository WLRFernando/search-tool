import argparse
from dataclasses import dataclass
import math
import os
import sys
import re

results_arr=[]

#Object class for storing search results in a array
@dataclass
class ResultObject:
    """Class for keeping track of search results."""
    line_no: int
    line: str
    match: str

    #Function to get the out put of the saved result
    def output(self):
        sys.stdout.write("Line {} : \n".format(self.line_no))
        sys.stdout.write(highlight(self.match, self.line))
        return "Line {:<8} : {} \n".format(self.line_no,self.line)


def main():
    parser = argparse.ArgumentParser(description="A replacement for grep.")
    parser.add_argument("pattern", type=str, help="the pattern to search for")
    parser.add_argument("-f", "--file", type=str, help="file path")
    parser.add_argument("-v", dest="invert", default=False, 
                        action="store_true", help="invert matches")
    parser.add_argument("--max-count", "-m", type=int,
        default=math.inf, help="max number of matches to print")
    args = parser.parse_args()
    no_of_results=0

    if not args.pattern:
        parser.print_help()
        return

    if not args.file and not sys.stdin:
        sys.stdout.write("\033[31m!!! Please specify the file or stdin \n\033[0m")
        parser.print_help()
        return

    if not args.file:
        no_of_results=searchAction(sys.stdin, args.pattern, args.invert)

    elif args.file == ".":
        for path, dirs, files in os.walk(os.getcwd()):
            for filename in files:
                fullpath = os.path.join(path, filename)
                with open(fullpath, 'r') as f:
                    try: 
                        no_of_results=searchAction(f, args.pattern, args.invert)
                        #TODO - Optimize recursive search
                    except:
                        pass               
                
    else:

        file=open(args.file,"r")
        no_of_results=searchAction(file, args.pattern, args.invert)


    sys.stdout.write("Search Pattern: \033[31m{} \033[0m \nNo. of Results: {} \n\n".format(args.pattern, no_of_results))
    printResult(results_arr, args.max_count)


#Print Every single results saved in the array
def printResult(arr, count):
    matches = 0
    for result in arr:
        matches += 1
        result.output()
        if matches >= count:
            break

#General serach function 
def searchAction(file, pattern, invert):
    regex = re.compile(pattern)
    count=0
    no_of_results=0
    for line in file:
        count+=1
        if line in ['\n', '\r\n']:
            continue
        match = regex.search(line)
        
        # if regex.search(line):
        if invert != bool(regex.search(line)): 
            no_of_results+=1         
            result_object=ResultObject(count,line,match)
            results_arr.append(result_object)
    
    return no_of_results #return no of results found during the search

#Text highlight function for stdout 
#Optional function which make result of the search more readable
def highlight(match, line):
    if not match or not sys.stdout.isatty():
        return line
    return (line[:match.start()]
        + "\033[31m" # change to red
        + line[match.start():match.end()]
        + "\033[0m" # reset
        + line[match.end():])


#Invoking main function when called by the package name
if __name__ == "__main__":
    main()
