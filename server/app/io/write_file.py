import os
class WriteFile:
    def __init__(self, file_name, code: str):
        self.__file_path = os.getcwd() + "../local/"
        try:
            file = open(self.__file_path + file_name, operation)
            file.write(code)
        except Exception as e:
            print(e)
        finally:
            file.close()