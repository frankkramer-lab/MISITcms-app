import argparse

# Implement an Argument Parser
parser = argparse.ArgumentParser()
# Add arguments to the Argument Parser
parser.add_argument("-a", action="store", type=int)
parser.add_argument("-b", action="store", type=int)
parser.add_argument("--shout", action="store", type=str, required=True)

# Parse arguments
args = parser.parse_args()

# Do some stuff
if args.a is not None and args.b is not None:
    c = args.a * args.b
    output = args.shout + " " + str(c)
else:
    output = args.shout

# Print out string to file: output.txt
with open("output.txt", "w") as fw:
    fw.write(output)
