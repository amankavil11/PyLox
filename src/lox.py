import sys
import scanner

class Lox:
    def __init__(self):
        self.had_error = False
    
    def run_file(self, path):
        with open(path) as f:
            source = f.read()
        self.run(source)

        if self.had_error: sys.exit(65)
    
    def run_prompt(self):
        while True:
            try:
                line = input("pylox> ")
                if line == "exit" or line == "exit()":
                    break
            except EOFError:
                print("\r")
                break
            
            self.run(line)
            self.had_error = False
    
    def run(self, source):
        local_scanner = scanner.Scanner(self, source)
        tokens = list(local_scanner.scan_tokens())

        for token in tokens:
            print(token)


    def error(self, line, where='', message=None):
        self.report(line, where, message)

    def report(self, line, where, message):
        print(f'[line {line}] Error {where}: {message}')
        self.had_error = True
    

        

def main():
    py_lox = Lox()
    num_args = len(sys.argv) - 1
    if num_args > 1:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif num_args == 1:
        py_lox.run_file(sys.argv[1])
    else:
        py_lox.run_prompt()


if __name__ == '__main__':
    main()