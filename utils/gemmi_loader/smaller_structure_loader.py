import gemmi

def load_cif_file(
    cif_filepath: str
) -> gemmi.SmallStructure:
    """
    Load cif file with fix format ("Seem not work")
    """
    # Open file
    with open(cif_filepath) as cif:
        cif_text = cif.read()
    
    # Reformat file
    lines = cif_text.split('\n')
    del lines[2]
    # Save file
    cif_filename = cif_filepath.split('/')[-1]
    with open(f".temp/{cif_filename}", "w+") as new_cif:
        new_cif.write('\n'.join(lines))

    # Reload as Gemmi
    cif_object = gemmi.read_small_structure(f".temp/{cif_filename}")
    try:
        os.remove(f".temp/{cif_filename}")
    except FileNotFoundError:
        pass
    return cif_object