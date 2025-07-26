import re
import csv
from collections import defaultdict


def parse_pubmed_citations(file_path, output_csv_path):
    """
    Parse PubMed citations from a text file and convert to UTF-8 CSV format.

    Args:
        file_path (str): Path to the input text file containing PubMed citations
        output_csv_path (str): Path to the output UTF-8 CSV file
    """

    # Read input file with UTF-8 encoding
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except UnicodeDecodeError:
        # Try with different encodings if UTF-8 fails
        print("UTF-8 decoding failed, trying latin-1...")
        with open(file_path, "r", encoding="latin-1") as file:
            content = file.read()

    # Split by double newlines to separate citations
    citations = content.strip().split("\n\n")

    all_records = []
    all_columns = set()

    for citation in citations:
        if not citation.strip():
            continue

        record = defaultdict(list)
        lines = citation.strip().split("\n")

        current_field = None
        current_value = ""

        for line in lines:
            # Check if line starts with a field code (letters/numbers followed by space and dash)
            field_match = re.match(r"^([A-Z][A-Z0-9]*)\s*-\s*(.*)$", line)

            if field_match:
                # Save previous field if it exists
                if current_field and current_value.strip():
                    process_field(
                        record, current_field, current_value.strip(), all_columns
                    )

                # Start new field
                current_field = field_match.group(1)
                current_value = field_match.group(2)
            else:
                # Continuation of previous field
                if current_field:
                    current_value += " " + line.strip()

        # Don't forget the last field
        if current_field and current_value.strip():
            process_field(record, current_field, current_value.strip(), all_columns)

        # Convert defaultdict to regular dict and add to records
        if record:
            all_records.append(dict(record))

    # Write to UTF-8 CSV with BOM for Excel compatibility
    write_csv(all_records, list(all_columns), output_csv_path)
    print(
        f"Parsed {len(all_records)} citations and saved to UTF-8 CSV: {output_csv_path}"
    )
    print(f"Total columns: {len(all_columns)}")
    print("Note: CSV file uses UTF-8 encoding with BOM for maximum compatibility")


def process_field(record, field_code, value, all_columns):
    """Process individual fields and handle special cases."""

    if field_code == "IS":  # ISSN handling
        # Extract ISSN type from parentheses
        if "(Electronic)" in value:
            issn = value.replace("(Electronic)", "").strip()
            record["issn_electronic"].append(issn)
            all_columns.add("issn_electronic")
        elif "(Print)" in value:
            issn = value.replace("(Print)", "").strip()
            record["issn_print"].append(issn)
            all_columns.add("issn_print")
        elif "(Linking)" in value:
            issn = value.replace("(Linking)", "").strip()
            record["issn_linking"].append(issn)
            all_columns.add("issn_linking")
        else:
            record["issn_other"].append(value)
            all_columns.add("issn_other")

    elif field_code == "PHST":  # Publication history dates
        # Extract date type from square brackets
        if "[pubmed]" in value:
            date = value.replace("[pubmed]", "").strip()
            record["phst_pubmed"].append(date)
            all_columns.add("phst_pubmed")
        elif "[medline]" in value:
            date = value.replace("[medline]", "").strip()
            record["phst_medline"].append(date)
            all_columns.add("phst_medline")
        elif "[entrez]" in value:
            date = value.replace("[entrez]", "").strip()
            record["phst_entrez"].append(date)
            all_columns.add("phst_entrez")
        elif "[pmc-release]" in value:
            date = value.replace("[pmc-release]", "").strip()
            record["phst_pmc_release"].append(date)
            all_columns.add("phst_pmc_release")
        elif "[received]" in value:
            date = value.replace("[received]", "").strip()
            record["phst_received"].append(date)
            all_columns.add("phst_received")
        elif "[accepted]" in value:
            date = value.replace("[accepted]", "").strip()
            record["phst_accepted"].append(date)
            all_columns.add("phst_accepted")
        else:
            record["phst_other"].append(value)
            all_columns.add("phst_other")

    else:
        # Handle regular fields - convert field code to lowercase
        field_name = field_code.lower()
        record[field_name].append(value)
        all_columns.add(field_name)


def write_csv(records, columns, output_path):
    """Write records to CSV file with UTF-8 encoding."""

    # Sort columns to have PMID first, then alphabetically
    sorted_columns = sorted(columns)
    if "pmid" in sorted_columns:
        sorted_columns.remove("pmid")
        sorted_columns.insert(0, "pmid")

    # Write CSV with explicit UTF-8 encoding and BOM for Excel compatibility
    with open(output_path, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        # Write header
        writer.writerow(sorted_columns)

        # Write data
        for record in records:
            row = []
            for col in sorted_columns:
                if col in record and record[col]:
                    # Join multiple values with semicolon
                    cell_value = "; ".join(record[col])
                    row.append(cell_value)
                else:
                    row.append("")
            writer.writerow(row)


def main():
    """Main function to run the parser."""

    # Example usage
    input_file = "pubmed_tte_20250726.nbib"  # Change this to your input file path
    output_file = "pubmed_tte_20250726.csv"  # Change this to your desired output path

    try:
        parse_pubmed_citations(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
        print("Please make sure the file exists and the path is correct.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
