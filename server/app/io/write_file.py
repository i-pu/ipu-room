class WriteFile:
    def __init__(self, file_name, code: str):
        # 読込むファイルのパスを宣言する
        self.__file_path = "./run_space/"
        try:
            file = open(self.__file_path + file_name, operation)
            file.write(code)
        except Exception as e:
            print(e)
        finally:
            file.close()