# Read the contents of the first file
with open("pi1.txt", "r") as file1:
    lines1 = file1.readlines()

# Read the contents of the second file
with open("pi2.txt", "r") as file2:
    lines2 = file2.readlines()

# Check for differences and count differing lines
differing_lines_count = sum(1 for line1, line2 in zip(lines1, lines2) if line1.strip() != line2.strip())

# Print the count of differing lines if there are any
if differing_lines_count > 0:
    print(f"There are {differing_lines_count} lines that are different.")
else:
    print("All lines in the files are the same.")



