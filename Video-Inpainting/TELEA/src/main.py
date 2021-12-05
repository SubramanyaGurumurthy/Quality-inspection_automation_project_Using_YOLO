
# # Overwiew
#
#  This script is executed by Docker as an entrypoint.
#  The purpose of this script is to run other scripts within the docker container.

# ## Import Libraries

import sys
import os

if __name__ == "__main__" :
    
    # No scripts provided as argument
    if len(sys.argv) == 1 :
        print("No scripts to run")

    for arg in sys.argv[1:] :
        print(f"Executing script: {arg}")
        os.system(f"python -u {arg}")

