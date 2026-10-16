
class User:
    def __init__(self, 
                 id: int = None,
                 first_name: str = None,
                 last_name: str = None,
                 email: str = None,
                 password_hash: str = None,
                 role: str = 'user',
                 is_active: bool = True):

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active

    def __repr__(self):
        return f"""
        User(
            id={self.id},
            first_name={self.first_name},
            last_name={self.last_name},
            email={self.email},
            password_hash={self.password_hash},
            role={self.role},
            is_active={self.is_active})"""