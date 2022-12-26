import argparse
from dataclasses import dataclass
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

    def output(self):
        out="Line {:<8} : {} \n"
        sys.stdout.write(out.format(self.line_no, highlight(self.match, self.line)))
        return "Line {:<8} : {} \n".format(self.line_no,self.line)

def main():
    parser = argparse.ArgumentParser(description="A replacement for grep.")
    parser.add_argument("pattern", type=str, help="the pattern to search for")
    args = parser.parse_args()
    regex = re.compile(args.pattern)
    count=0
    for line in sys.stdin:
        match = regex.search(line)
        count+=1
        if regex.search(line):          
            result_object=ResultObject(count,line,match)
            results_arr.append(result_object)
            # result_object.output()

    printResult()

def printResult():
    for result in results_arr:
        result.output()

def highlight(match, line):
    if not match or not sys.stdout.isatty():
        return line
    return (line[:match.start()]
        + "\033[31m" # change to red
        + line[match.start():match.end()]
        + "\033[0m" # reset
        + line[match.end():])





if __name__ == "__main__":
    main()
