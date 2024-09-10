origin = "/Collider/scripts_2208/data/clean/"

file1 = f"{origin}/no_opti_photons4_ZH.txt"
file2 = f"{origin}/opti_photons4_ZH.txt"

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        # Read lines from both files
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        # Compare line by line and count differences
        diff_count = sum(1 for line1, line2 in zip(lines1, lines2) if line1 != line2)

        # If the files have different lengths, count the extra lines
        diff_count += abs(len(lines1) - len(lines2))

    print(f"Number of differing lines: {diff_count}")

compare_files(file1, file2)
