import os
import sys

from pyffi.formats.nif import NifFormat


def extract_pixel_data(nif_file_path):
    # Load the NIF file
    nif_data = NifFormat.Data()
    with open(nif_file_path, 'rb') as file:
        nif_data.read(file)

    # Find the NiPixelData node at index 0
    pixel_data_node = None
    for root_block in nif_data.roots:
        for block in root_block.tree():
            if isinstance(block, NifFormat.NiPixelData):
                pixel_data_node = block
                break
        if pixel_data_node:
            break

    if not pixel_data_node:
        print("No NiPixelData node found.")
        return


    # Get the base and extension parts of the file path
    base_path, current_extension = os.path.splitext(nif_file_path)

    # Create the new file path with the ".dds" extension
    new_file_path = base_path + ".dds"

    print(new_file_path)

    # Save the DDS file
    with open(new_file_path, 'wb') as dds_file:
        pixel_data_node.save_as_dds(dds_file)


if __name__ == "__main__":
    # Ensure a filename is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    # Extract the filename from the command line arguments
    nif_file_path = sys.argv[1]

    if os.path.exists(nif_file_path):
        extract_pixel_data(nif_file_path)
    else:
        print(f"File not found: {nif_file_path}")

