
class Category:
    def __init__(self,
                 id: int = None,
                 name: str = None,
                 type: str = None,
                 is_active: bool = True):

        self.id = id
        self.name = name
        self.type = type
        self.is_active = is_active

    def __repr__(self):
        return f"""
        Category(
            id={self.id},
            name={self.name},
            type={self.type},
            is_active={self.is_active})
        """
        