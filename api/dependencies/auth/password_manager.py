from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordManager:
    """
    This class is responsible for managing passwords,
    especially hashing new ones and verifying the validity.
    """

    def __init__(self, raw_password: str):
        self.__raw_password = raw_password

    def hash_password(self) -> str:
        """
        Hashes input password.
        :return: str
        """
        return pwd_context.hash(self.__raw_password)

    def verify_password(self, hashed_password: str) -> bool:
        """
        Validates given password against given algorithm.
        :param hashed_password: str
        :return: bool
        """
        return pwd_context.verify(self.__raw_password, hashed_password)
