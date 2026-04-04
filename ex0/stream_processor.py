from abc import ABC, abstractmethod
from typing import Any, List, Dict


class DataProcessor(ABC):
    def __init__(self):
        self.data = []
    show_validation = True

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def output(self) -> tuple[int, str]:
        if self.data:
            item = self.data.pop(0)
            index = 0 
            return index, item

class NumericProcessor(DataProcessor):
    def ingest(self, data:  int | float | List[int] | list[float]) -> None:
        try:
            if not self.validate(data):
                raise ValueError("Got exception: Improper numeric data")
            if isinstance(data,(int, float)):
                self.data+=(str(data))
            else:
                for item in data:
                    self.data+=(str(item))
           
            return (
                    self.data
                )
            
        except ValueError as e:
            return f"{str(e)}"

    def validate(self, data: Any) -> bool:
        try:
            if isinstance(data, (int, float)):
                if self.show_validation:
                    print("Validation: Numeric data verified")
                return True

            if isinstance(data, list) and all(isinstance(n, (int, float)) for n in data):
                if self.show_validation:
                    print("Validation: Numeric data verified")
                return True
            return False
        except Exception:
            print("Got exception: Improper numeric data")
            return False


class TextProcessor(DataProcessor):
    def ingest(self, data: str | list[str]) -> None:
        try:
            if not self.validate(data):
                raise ValueError("Invalid data")
            if isinstance(data, str):
                self.data.append(data)
            else:
                for word in data:
                    self.data.append(word)
            return (self.data)
        except Exception as e:
            return str({e})
    def validate(self, data: Any) -> bool:
        try:
            if isinstance(data, str):
                return True
            elif isinstance(data, list) and all(isinstance(i, str)for i in data):
                return True
            return False
        except Exception:
            return False


class LogProcessor(DataProcessor):
    def ingest(self, data: dict[str, str] | List[Dict[str, str]] | str) -> None:
        try:
            if not self.validate(data):
                raise ValueError(" Improper log data")
            if isinstance(data, dict):
                self.data.append(str(data.values()))
            else:
                for item in data:
                    self.data.append(str(item.values()))
                return self.data        
        except Exception as e:
            return f"Error: {str(e)}"

    def validate(self, data: Any) -> bool:
        try:
            if isinstance(data, str):
                return ":" in data
            if isinstance(data, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
                return True
            if isinstance(data, list) and all(
                isinstance(item, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in item.items())
                for item in data
            ):
                return True
            return False
        except Exception:
            return False

def main():
    print("=== CODE NEXUS - DATA PROCESSOR  ===")
    print("\nTesting Numeric Processor...")
    num_proc = NumericProcessor()
    print("Trying to validate input 42 :",num_proc.validate(42))
    print("Trying to validate input Hello :",num_proc.validate("Hello"))
    print("Test invalid ingestion of string ’foo’ without prior validation:")
    print(num_proc.ingest("foo"))
    print("Processing data: [1, 2, 3, 4, 5]")
    result = num_proc.ingest([1, 2, 3, 4, 5])
    num_output = num_proc.output()
    for item in num_output:
        print(f"Numeric value {num_output.index(item)}: {item}")

    print("\nTesting Text Processor...")
    text_proc = TextProcessor()
    print("Trying to validate input 42 :",text_proc.validate(42))
    print("Processing data: \"Hello Nexus World\"")
    result = text_proc.ingest(['Hello', 'Nexus', 'World'])
    text_output=text_proc.output()
    for item in text_output:
        print(f"Text value {text_output.index(item)}: {item}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()
    print("Trying to validate input Hello :",log_proc.validate("Hello"))
    print('Processing data: [{"log_level": "NOTICE", "log_message": "Connection to server"}, {"log_level": "ERROR", "log_message": "Unauthorized access!!"}]')
    result = log_proc.ingest([{"log_level": "NOTICE", "log_message": "Connection to server"}, {"log_level": "ERROR", "log_message": "Unauthorized access!!"}])
    print(log_proc.output())


if __name__ == "__main__":
    main()
