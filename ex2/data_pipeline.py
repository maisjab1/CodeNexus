from typing import Any, Protocol
from abc import ABC, abstractmethod


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CSV:
    def process_output(self, data: list[tuple[int, str]]) -> None:

        for i in range(len(data)):
            if i == len(data) - 1:
                print(f"{data[i][1]}", end="")
            else:
                print(f"{data[i][1]}", end=",")


class JSON:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("{", end="")
        for i in range(len(data)):
            if i == len(data)-1:
                print(f'item_{data[i][0]}: "{data[i][1]}"', end="")
            else:
                print(f'item_{data[i][0]}: "{data[i][1]}"', end=", ")
        print("}", end="")


class DataProcessor(ABC):
    def __init__(self):
        self.data = []
        self.processed_count = 0
        self.rank = 0
        self.item = 0

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def output(self) -> tuple[int, str]:
        self.item += 1
        if not self.data:
            raise IndexError("No data available")

        value = self.data.pop(0)
        return value


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
                    print(f"DataStream error - "
                          f"Can't process element in stream: {d}")

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
        if isinstance(plugin, CSV):
            kind = "CSV"
        else:
            kind = "JSON"
        for proc in self.streams:
            data = []
            print(f"{kind} output:")
            for i in range(nb):
                try:
                    data.append(proc.output())
                except Exception:
                    break
            plugin.process_output(data)

            print()


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def ingest(self, data: Any) -> None:
        try:
            if not self.validate(data):
                return
            if isinstance(data, (int, float)):
                self.data.append((self.rank, str(data)))
                self.processed_count += 1
                self.rank += 1
            else:
                for item in data:
                    self.data.append((self.rank, str(item)))
                    self.processed_count += 1
                    self.rank += 1
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
                self.data.append((self.rank, data))
                self.processed_count += 1
                self.rank += 1
            else:
                for word in data:
                    self.data.append((self.rank, word))
                    self.processed_count += 1
                    self.rank += 1
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
                self.data.append((self.rank, f"{
                    data['log_level']}: {data['log_message']}"))
                self.rank += 1
                self.processed_count += 1
            else:
                for item in data:
                    self.data.append((
                        self.rank, f"{item['log_level']}: {
                            item['log_message']}"))
                    self.processed_count += 1
                    self.rank += 1
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
    print("\n== DataStream statistics ==")
    proc.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin")
    csv = CSV()
    proc.output_pipeline(3, csv)
    print("== DataStream statistics ==")
    proc.print_processors_stats()
    data2 = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {
                'log_level': 'ERROR', 'log_message': '500 server crash'
            },
            {
                'log_level': 'NOTICE', 'log_message':
                'Certificate expires in 10 days'
            }
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello'
    ]
    print(f"\nSend another batch of data: {data2}")
    print("\n== DataStream statistics ==")
    proc.process_stream(data2)
    proc.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    json = JSON()
    proc.output_pipeline(5, json)
    print("\n== DataStream statistics ==")
    proc.print_processors_stats()


if __name__ == "__main__":
    main()
