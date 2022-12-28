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
    #Every search result is capable of printing out their value when output() is called
    def output(self):
        sys.stdout.write("Line {} : \n".format(self.line_no))
        sys.stdout.write(highlight(self.match, self.line))
        return "Line {:<8} : {} \n".format(self.line_no,self.line)


def main():
    #argparse python package to parse the command line arguments
    parser = argparse.ArgumentParser(description="A replacement for grep.")
    parser.add_argument("pattern", type=str, help="the pattern to search for")
    parser.add_argument("-f", "--file", type=str, help="file path")
    # invert search flag - boolean value (default flase)
    parser.add_argument("-v", dest="invert", default=False, 
                        action="store_true", help="invert matches") 
    # max count argument default value infinity                     
    parser.add_argument("--max-count", "-m", type=int,
        default=math.inf, help="max number of matches to print") 
    args = parser.parse_args()
    #No of results shown in stdout
    no_of_results=0

    #Error handling - If pattern is not defined by the user
    if not args.pattern:
        parser.print_help()
        return

    if not args.file and not sys.stdin:
        sys.stdout.write("\033[31m!!! Please specify the file or stdin \n\033[0m")
        parser.print_help()
        return

    #If file argument is not defined tool will check for standard input
    if not args.file:
        no_of_results=searchAction(sys.stdin, args.pattern, args.invert)

    #if the '.' passed in the file argument it will search recursivly
    elif args.file == ".":
        for path, dirs, files in os.walk(os.getcwd()):
            for filename in files:
                fullpath = os.path.join(path, filename)
                with open(fullpath, 'r') as f:
                    try: 
                        sys.stdout.write(fullpath)
                        sys.stdout.write("\n")
                        no_of_results+=searchAction(f, args.pattern, args.invert)
                        printResult(results_arr, args.max_count)
                        results_arr.clear()
                    except:
                        pass
        return               

    #Read the file defined in the file argument           
    else:

        file=open(args.file,"r")
        no_of_results=searchAction(file, args.pattern, args.invert)

    #Print final result
    sys.stdout.write("Search Pattern: \033[31m{} \033[0m \nNo. of Results: {} \n\n".format(args.pattern, no_of_results))
    printResult(results_arr, args.max_count)


#Print Every single results saved in the array
def printResult(arr, count): 
    matches = 0
    for result in arr:
        matches += 1
        result.output()
        #Max results count argument check
        if matches >= count:
            break

#General serach function 
def searchAction(file, pattern, invert):
    regex = re.compile(pattern)
    count=0
    no_of_results=0
    for line in file:
        count+=1
        #Ignore white lines(empty lines)
        if line in ['\n', '\r\n']:
            continue
        match = regex.search(line)
        
        # Check for invert search flag
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
