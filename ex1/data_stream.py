from typing import Any, List, Dict
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self):
        self.data = []
        self.processed_count = 0

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def output(self) -> tuple[int, str]:
        if not self.data:
            raise IndexError("No data available")

        value = self.data.pop(0)
        return 0, value


class DataStream:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.streams = []
        self.processed_count = {"num": 0, "text": 0, "log": 0}

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self.streams.append(proc)
        else:
            print("ERROR")

    def process_stream(self, stream: list[Any]) -> None:
        if stream:
            for d in self.data:
                    handeled = False
                    for s in stream:
                        if isinstance(s, NumericProcessor):
                            type = "num"
                        elif isinstance(s, TextProcessor):
                            type = "text"
                        else:
                            type = "log"
                        s.ingest(d)
                        self.processed_count[type] = s.processed_count
                        if s.validate(d):
                            handeled = True

            if not handeled:
                print("DataStream error - Can’t process element in stream:")

    def print_processors_stats(self) -> None:
        if self.streams:
            print(f"{self.streams} total {self.processed_count}")
        else:
            print("No processor found, no data\n")


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
    def ingest(self, data:  int | float | List[int] | list[float]) -> None:
        try:
            if not self.validate(data):
                return
            if isinstance(data, (int, float)):
                self.data += (str(data))
                self.processed_count += 1
            else:
                for item in data:
                    self.data += (str(item))
                    self.processed_count += 1
            

        except ValueError as e:
            print(f"{str(e)}")

    def validate(self, data: Any) -> bool:
        try:
            if isinstance(data, (int, float)):
                return True

            if isinstance(data, list) and all(
               isinstance(n, (int, float)) for n in data):
                return True
            return False
        except Exception:
            return False


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
    def ingest(self, data: str | list[str]) -> None:
        try:
            if not self.validate(data):
                return
            if isinstance(data, str):
                self.data.append(data)
                self.processed_count += 1
            else:
                for word in data:
                    self.data.append(word)
                    self.processed_count += 1
        except Exception as e:
            print(str(e))

    def validate(self, data: Any) -> bool:
        try:
            if isinstance(data, str):
                return True
            elif isinstance(data, list) and all(
                 isinstance(i, str)for i in data):
                return True
            return False
        except Exception:
            return False


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data: dict[str, str] | List[Dict[str, str]]) -> None:
        try:
            if not self.validate(data):
                return
            if isinstance(data, dict):
                self.data.append(f"{data['log_level']}: {data['log_message']}")
                self.processed_count += 1
            else:
                for item in data:
                    self.data.append(
                        f"{item['log_level']}: {item['log_message']}")
                    self.processed_count += 1
        except Exception as e:
            return f"Error: {str(e)}"

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
def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    print("== DataStream statistics ==")
    data = ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING', 'log_message': 'Telnet access!Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 42, ['Hi', 'five']]
    proc = DataStream(data)
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    proc.print_processors_stats()
    print("Registering Numeric Processor\n")
    print(f"Send first batch of data on stream:{data}")
    proc.register_processor(num_proc)

    proc.process_stream(proc.streams)
    proc.print_processors_stats()
    print("\nRegistering other data processors")
    proc.register_processor(text_proc)
    proc.register_processor(log_proc)
    print("Send the same batch again")
    print("== DataStream statistics ==")
    proc.process_stream(proc.streams)
    proc.print_processors_stats()



if __name__ == "__main__":
    main()