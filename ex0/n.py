
from abc import ABC, abstractmethod
from typing import Any


# =========================
# Abstract Base Class
# =========================
class DataProcessor(ABC):
    def __init__(self):
        self.data: list[str] = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.data:
            raise IndexError("No data available")

        value = self.data.pop(0)
        return 0, value


# =========================
# Numeric Processor
# =========================
class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
            return True
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, (int, float)):
            self.data.append(str(data))
        else:
            for item in data:
                self.data.append(str(item))


# =========================
# Text Processor
# =========================
class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return True
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Invalid text data")

        if isinstance(data, str):
            self.data.append(data)
        else:
            for item in data:
                self.data.append(item)


# =========================
# Log Processor
# =========================
class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return (
                "log_level" in data
                and "log_message" in data
                and isinstance(data["log_level"], str)
                and isinstance(data["log_message"], str)
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and "log_level" in item
                and "log_message" in item
                and isinstance(item["log_level"], str)
                and isinstance(item["log_message"], str)
                for item in data
            )

        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, dict):
            self.data.append(f"{data['log_level']}: {data['log_message']}")
        else:
            for item in data:
                self.data.append(f"{item['log_level']}: {item['log_message']}")


# =========================
# Testing (Main)
# =========================
if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    # -------- Numeric Processor --------
    print("Testing Numeric Processor...")
    num_proc = NumericProcessor()

    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest("foo")  # type: ignore
    except Exception as e:
        print(f"Got exception: {e}")

    print("Processing data: [1, 2, 3, 4, 5]")
    num_proc.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for i in range(3):
        idx, value = num_proc.output()
        print(f"Numeric value {idx}: {value}")

    # -------- Text Processor --------
    print("Testing Text Processor...")
    text_proc = TextProcessor()

    print(f"Trying to validate input '42': {text_proc.validate(42)}")

    print("Processing data: ['Hello', 'Nexus', 'World']")
    text_proc.ingest(["Hello", "Nexus", "World"])

    print("Extracting 1 value...")
    idx, value = text_proc.output()
    print(f"Text value {idx}: {value}")

    # -------- Log Processor --------
    print("Testing Log Processor...")
    log_proc = LogProcessor()

    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")

    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]

    print(f"Processing data: {logs}")
    log_proc.ingest(logs)

    print("Extracting 2 values...")
    for i in range(2):
        idx, value = log_proc.output()
        print(f"Log entry {idx}: {value}")

