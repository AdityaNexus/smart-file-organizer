import sys
import argparse
#print(sys.argv) #sys.argv is a list containing the command-line arguments.

def main():
    parser = argparse.ArgumentParser(     # create parser
        description = "A simple greeting CLI" # description your application 
    )

    parser.add_argument(   # dfine accepted arguments
        "name",            # defines a positional argument called "name"
        help = "person to greet"
    )
    parser.add_argument(
        "--greeting",      # defines an optional argument called "--greeting"
        default = "Hello", # sets a default value for the greeting
        help = "custom greeting message" # provides a help message for the argument
    )
    args = parser.parse_args()   # reads and validates the command-line arguments and returns them as an object with attributes corresponding to the argument names.
    print(f"{args.greeting}, {args.name}!") # retrieves the value of the "name" argument from the args object and prints a greeting message to the console.

def lession_2():
    parser = argparse.ArgumentParser(
        description = "A configurable task runner"
    )

    parser.add_argument(
        "task",
        help = "name of the task to excute"
    )
    
    parser.add_argument(
        "--mode",
        choices = ["fast" , "safe"],  #restricts the allowed values for the --mode argument to either "fast" or "safe"
        default = "safe",
        help = "execution mode"
    )

    parser.add_argument(
        "--count",
        type = int, #type of the argument is specified as int, which means that the value provided for --count will be converted to an integer.
        default = 1,
        help = "number of times to run the task"
    )

    parser.add_argument(
        "--output",
        required = True, # specifies that the --output argument is required, meaning that the user must provide a value for this argument when running the script.
        help = "output file path"
    )

    parser.add_argument(
        "--verbose",
        action = "store_true", # specifies that the --verbose argument is a flag that does not require a value. If the user includes --verbose in the command line, the corresponding attribute in the args object will be set to True; otherwise, it will be False.
        help = "enable verbose output"
    )

    args = parser.parse_args()
    print(f"Task: {args.task}")
    print(f"Mode: {args.mode}")
    print(f"Count: {args.count}")
    print(f"Output: {args.output}")
    if args.verbose:
        print("Verbose output enabled")

if __name__ == "__main__":
   # main()
   lession_2()