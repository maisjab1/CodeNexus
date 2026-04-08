from typing import Any
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
        self.streams: list[DataProcessor] = []
        self.processed_count = {"num": 0, "text": 0, "log": 0}

    def register_processor(self, proc: DataProcessor) -> None:
        if isinstance(proc, DataProcessor):
            self.streams.append(proc)
        else:
            print("ERROR")

    def process_stream(self, stream: list[Any]) -> None:
        if stream:
            for d in stream:
                handeled = False
                for s in self.streams:
                    s.ingest(d)
                    if s.validate(d):
                        handeled = True

                if not handeled:
                    print("DataStream error - "
                          f"Can’t process element in stream: {d}")

    def print_processors_stats(self) -> None:
        if self.streams:
            for s in self.streams:
                remaining = len(s.data)
                if isinstance(s, NumericProcessor):
                    print(f"Numeric Processor: total {s.processed_count},"
                          f" remaining {remaining} on processor")
                if isinstance(s, TextProcessor):
                    print(f"Text Processor: total {s.processed_count},"
                          f" remaining {remaining} on processor")
                if isinstance(s, LogProcessor):
                    print(f"Log Processor: total {s.processed_count},"
                          f" remaining {remaining} on processor")
        else:
            print("No processor found, no data\n")


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data: Any) -> None:
        try:
            if not self.validate(data):
                return
            if isinstance(data, (int, float)):
                self.data.append(str(data))
                self.processed_count += 1
            else:
                for item in data:
                    self.data.append(str(item))
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

    def ingest(self, data: Any) -> None:
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

    def ingest(self, data: Any) -> None:
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
            print(f"Error: {str(e)}")

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
    data = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access!Use ssh instead'
            },
            {
                'log_level': 'INFO',
                'log_message': 'User wil is connected'
            }
        ],
        42,
        ['Hi', 'five']
    ]
    proc = DataStream(data)
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    proc.print_processors_stats()
    print("Registering Numeric Processor\n")
    print(f"Send first batch of data on stream:{data}")
    proc.register_processor(num_proc)

    proc.process_stream(data)
    proc.print_processors_stats()
    print("\nRegistering other data processors")
    proc.register_processor(text_proc)
    proc.register_processor(log_proc)

    print("Send the same batch again")
    print("== DataStream statistics ==")
    proc.process_stream(data)
    proc.print_processors_stats()
    print("\nConsume some elements from the data processors:"
          "Numeric 3, Text 2, Log 1")

    for i in range(3):
        num_proc.output()
    for i in range(2):
        text_proc.output()
    for i in range(1):
        log_proc.output()

    print("== DataStream statistics ==")
    proc.print_processors_stats()


if __name__ == "__main__":
    main()
