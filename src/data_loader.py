import csv

# Input and output file paths (using raw strings to avoid backslash issues)
input_file = r'..\data\anime_with_synopsis.csv'
output_file = r'..\data\output.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # Write header
    writer.writerow(['anime'])

    for row in reader:
        # Clean fields to remove extra commas or newlines that may break CSV
        name = row['Name'].replace('\n', ' ').replace(',', ' ')
        genres = row['Genres'].replace('\n', ' ').replace(',', ' ')
        synopsis = row['sypnopsis'].replace('\n', ' ').replace(',', ' ')

        anime_entry = (
            f"anime_name:{name}, "
            f"anime_genres:{genres}, "
            f"anime_sypnopsis:{synopsis}"
        )

        writer.writerow([f"anime:{anime_entry}"])
