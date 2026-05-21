import csv



def  load_data(filename):
    data = {}

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            mother = row["mother"] or None
            father = row["father"] or None
            trait = (True if row["trait"] == "1" else
                     False if row["trait"] == "0" else None)

            data[name] = {
                "name": name,
                "mother": mother,
                "father": father,
                "trait": trait
            }

    return data



"""
FUNCTION load_data(filename):
    data ← empty dictionary

    OPEN filename as CSV file:
        FOR each row in CSV:
            name   ← row["name"]
            mother ← row["mother"]  OR None if blank
            father ← row["father"]  OR None if blank
            trait  ← True  if row["trait"] == "1"
                     False if row["trait"] == "0"
                     None  otherwise (unknown)

            data[name] ← { name, mother, father, trait }

    RETURN data
"""