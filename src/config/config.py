from ..config import temp_path

class Config:
    VERSION = "0.0.1"
    REPOSITORY_PDF = ""
    REPOSITORY_JGP = ""
    GENERIC_ERROR_CODE = 1
    SUCCESS_CODE = 0
    DATA_FILE:str = temp_path  # type: ignore
    LOG_PATH = "./log"