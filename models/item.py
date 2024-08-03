class Item:
    def __init__(self, name: str, weight: float = None):
        self.name = name
        self.weight = weight

    def get_weight(self) -> float:
        return self.weight

    def set_weight(self, weight: float):
        self.weight = weight

    def get_name(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name