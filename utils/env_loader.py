class EnvLoader:
    def __init__(self, file, nospace=False):
        file_data = []
        with open(file, "r") as fl:
            file_data = fl.read().split("\n")
        # remove the space from before and after each words
        self.__variables = {
            line[:line.index("=")].strip() if nospace else line[:line.index("=")]:
            line[line.index("=")+1:].strip() if nospace else line[line.index("=")+1:]
            for line in file_data
        }

    def get_all(self):
        return self.__variables

    def get(self, key):
        return self.__variables.get(key, None)
