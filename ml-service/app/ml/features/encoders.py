class SimpleLabelEncoder:
    def __init__(self) -> None:
        self.mapping: dict[str, int] = {}

    def encode(self, value: str | None) -> int:
        if value is None:
            return -1

        if value not in self.mapping:
            self.mapping[value] = len(self.mapping)

        return self.mapping[value]