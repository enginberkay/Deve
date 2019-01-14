from pathlib import Path
import datetime


def WriteException(exceptionMessage, caller, pyFile):
    fatalErrotPath = Path("./FatalError.txt")
    dateTime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    errorData = dateTime + " | " + caller + \
        " | " + pyFile + " | " + exceptionMessage
    with open(fatalErrotPath, "a+") as f:
        f.write("\n")
        f.write(errorData)
    f.close()
