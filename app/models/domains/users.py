from pydantic import BaseConfig, BaseModel, EmailStr, validator


class User(BaseModel):
    email: EmailStr
    password: str
    username: str

    class Config(BaseConfig):
        anystr_strip_whitespace = True


class CreateUser(User):
    @validator("password")
    def password_is_strong(cls, password: str):
        """Enforce guidelines for strong passwords.

        Args:
            password (str): String sent from client.

        Raises:
            ValueError: If password does not meet the criteria.

        Returns:
            str: String where the value is kept partially secret.
        """
        special_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        errors: list[str] = []
        if len(password) < 8:
            errors.append("password must be at least 8 characters")
        if not any(char.isupper() for char in password):
            errors.append("password must include both uppercase and lowercase letters")
        if not any(char.islower() for char in password):
            errors.append("password must include letters and numbers")
        if not any(char in special_chars for char in password):
            errors.append("password must include at least one special character")
        if errors:
            raise ValueError("\n".join(errors))
        return password

    @validator("username")
    def username_is_alphanumeric(cls, username: str):
        """Enforce username standards.

        Args:
            username (str): String sent from client.

        Raises:
            ValueError: If username does not meet standards.

        Returns:
            str: Created username.
        """
        if not username.isalnum():
            raise ValueError("username must not contain special characters")
        return username
