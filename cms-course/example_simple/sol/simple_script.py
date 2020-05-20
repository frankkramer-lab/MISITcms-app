# Read data from file
with open("input.txt", "r") as rs:
    text = rs.read() # read text string from file including newline at the end

# Do some stuff
final = text + "... some additional stuff"

# Print out string to sys.out
print(final)
