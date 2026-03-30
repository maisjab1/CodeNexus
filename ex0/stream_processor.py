from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            print(f"Processing data: {data}")
            if not self.validate(data):
                raise ValueError("Invalid data")
            total = sum(data)
            avg = total / len(data)
            return f"Processed {len(data)} numeric values,sum= {total}"
            f", Avg: {avg}"

        except Exception as e:
            return f"Error: {str(e)}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, list) and all(isinstance(i, (int, float)
                                                     ) for i in data):
            return True
        print("Validation failed: Not numeric data")
        return False


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            print(f"Processing data: {data}")
            if not self.validate(data):
                raise ValueError("Invalid data")
            word_count = len(data.split())
            return f"Processed text:{len(data)} characters,"
            f"{word_count} words"
        except Exception as e:
            return f"Error: {str(e)}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        print("Validation failed: Not a string")
        return False


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            print(f"Processing data: {data}")
            if not self.validate(data):
                raise ValueError("Invalid data")
            level, msg = data.split(":", 1)

            return f"[{level}] {level} level detected: {msg}"
        except Exception as e:
            return f"Error: {str(e)}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str) and ":" in data:
            return True
        print("Validation failed: Not a list of strings")
        return False


def polymorphic_demo() -> None:
    print("\n=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    processor = [NumericProcessor(), TextProcessor(), LogProcessor()]
    test_data = [[1, 2, 3], "Hello World", "Info:System ready"]
    i = 1
    for i in range(len(processor)):
        result = processor[i].process(test_data[i])
        print(f"Result {i}: {result} ")


def main():
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print("\nInitializing Numeric Processor...")
    num_proc = NumericProcessor()
    result = num_proc.process([1, 2, 3, 4, 5])
    print(num_proc.format_output(result))  
    print("\nInitializing Text Processor...")
    text_proc = TextProcessor()
    result = text_proc.process("Hello world! This is a test.")
    print(text_proc.format_output(result))
    print("\nInitializing Log Processor...")
    log_proc = LogProcessor()
    result = log_proc.process("ERROR: Connection timeout")
    print(log_proc.format_output(result))
    polymorphic_demo()

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
