from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    show_validation = True

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
            if not self.validate(data):
                raise ValueError("Invalid data")
            total = sum(data)
            avg = total / len(data)
            return (
                f"Processed {len(data)} numeric values,"
                f"sum = {total}, Avg: {avg}"
                )

        except Exception as e:
            return f"Error: {str(e)}"

    def validate(self, data: Any) -> bool:
        try:
            sum(data)
            if self.show_validation:
                print("Validation: Numeric data verified")
            return True
        except Exception:
            print("Validation failed: Not numeric data")
            return False


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid data")
            word_count = len(data.split())
            return (
                 f"Processed text:{len(data)} characters,"
                 f" {word_count} words"
            )
        except Exception as e:
            return f"Error: {str(e)}"

    def validate(self, data: Any) -> bool:
        try:
            data.split()
            if self.show_validation:
                print("Validation: Text data verified")
            return True
        except Exception:
            print("Validation failed: Not a string")
            return False


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid data")
            level, msg = data.split(":", 1)

            return f"[ALERT]  {level} level detected: {msg}"
        except Exception as e:
            return f"Error: {str(e)}"

    def validate(self, data: Any) -> bool:
        try:
            level, msg = data.split(":", 1)
            if self.show_validation:
                print("Validation: Log entry verified")
            return True
        except Exception:
            print("Validation failed: Not valid log entry")
            return False


def polymorphic_demo() -> None:
    print("\n=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    processor = [NumericProcessor(), TextProcessor(), LogProcessor()]
    test_data = [[1, 2, 3], "Hello World", "Info:System ready"]
    for i in range(len(processor)):
        processor[i].show_validation = False
        result = processor[i].process(test_data[i])
        print(f"Result {i + 1}: {result} ")


def main():
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print("\nInitializing Numeric Processor...")
    num_proc = NumericProcessor()
    print("Processing data: [1, 2, 3, 4, 5]")
    result = num_proc.process([1, 2, 3, 4, 5])
    print(num_proc.format_output(result))

    print("\nInitializing Text Processor...")
    text_proc = TextProcessor()
    print("Processing data: \"Hello Nexus World\"")
    result = text_proc.process("Hello Nexus World")
    print(text_proc.format_output(result))

    print("\nInitializing Log Processor...")
    log_proc = LogProcessor()
    print("Processing data: 'ERROR: Connection timeout'")
    result = log_proc.process("ERROR: Connection timeout")
    print(log_proc.format_output(result))
    polymorphic_demo()

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
