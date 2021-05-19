from pathlib import Path

settings_file = Path.cwd() / "settings.yml"
done_path = Path.cwd() / "done"
not_done_path = Path.cwd() / "not_done"
names_txt_path = Path.cwd() / "names.txt"

default_settings = \
    """# Please enter the maximum points available here (key = exercise Nr., value = max points)
"Maximum Points":
    1: 3
    2: 4
    3: 4
    4: 4
    5: 3
    6: 3
    7: 3
    8: 2
    9: 2
    10: 4
    11: 4
    12: 3
    13: 3
    14: 4
    15: 4
# select what to happen after done correcting one hand in
# Possible choices:
# - "NOTHING" = Do nothing, leave the original there (not recommended, the show command will not diplay properly)
# - "REMOVE" = Default value, remove the original pdf from "not_done" so that it registers as "done".
#              Use this if you manually save the pdf to "done" and don't edit the pdf in place.
# - "RENAME" = Move the corrected PDF to the "done" folder and add a "_copy" to the end.
#              Use this if you edit the pdf in place and want it moved.
"After Finish": "REMOVE"
    """
