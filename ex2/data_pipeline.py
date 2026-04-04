from typing import Any, List, Dict, Protocol
from abc import ABC, abstractmethod


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CSV(ExportPlugin):
    def __init__(self):
        self.comma = True

    def process_output(self, data: tuple[int, str]) -> None:
        if not self.comma:
            print(",", end="")
        print(data[1], end="")
        self.comma = False

    def reset(self):
        self.comma = True


class JSON(ExportPlugin):
    def process_output(self, data: tuple[int, str]) -> None:
        print(f'{{"value": "{data[1]}"}}', end=",")


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
            for d in stream:
                handeled = False
                for s in self.streams:
                    s.ingest(d)
                    if s.validate(d):
                        handeled = True

                if not handeled:
                    print(f"DataStream error - "
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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.streams:
            plugin.reset()
            for _ in range(nb):
                try:
                    data = proc.output()
                    plugin.process_output(data)
                except IndexError:
                    break
            print()


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data:  int | float | List[int] | list[float]) -> None:
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
    print("=== Code Nexus - Data Pipeline ===\n")
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
    print("Registering Processors\n")
    print(f"Send first batch of data on stream:{data}")
    proc.register_processor(num_proc)
    proc.register_processor(text_proc)
    proc.register_processor(log_proc)
    proc.process_stream(data)
    print("== DataStream statistics ==")
    proc.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin")
    csv = CSV()
    print("csv output:")
    proc.output_pipeline(3, csv)
    print("== DataStream statistics ==")
    proc.print_processors_stats()


if __name__ == "__main__":
    main()
