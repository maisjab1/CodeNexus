from typing import Any, List, Dict, Optional, Union
from abc import ABC, abstractmethod


def my_len(s: Any) -> Optional[int]:
    c = 0
    for i in s:
        c += 1
    return c


def my_float(num: Any) -> Optional[float]:
    if not num or not isinstance(num, (str, int, float)):
        return None

    num = num.strip()
    if not num:
        return None
    try:
        n = num + 0.0
        return n
    except Exception:
        pass
    i = 0
    sign = 1
    if num[0] in ('-', '+'):
        if num[0] == '-':
            sign = -1
        i += 1
    result = 0.0
    decimal_seen = False
    decimal_place = 1.0
    digit_seen = False
    while i < my_len(num):
        if num[i] == '.':
            if decimal_seen:
                return None
            decimal_seen = True
        elif '0' <= num[i] <= '9':
            digit_seen = True
            if num[i] == '0':
                digit = 0
            elif num[i] == '1':
                digit = 1
            elif num[i] == '2':
                digit = 2
            elif num[i] == '3':
                digit = 3
            elif num[i] == '4':
                digit = 4
            elif num[i] == '5':
                digit = 5
            elif num[i] == '6':
                digit = 6
            elif num[i] == '7':
                digit = 7
            elif num[i] == '8':
                digit = 8
            elif num[i] == '9':
                digit = 9
            if decimal_seen:
                decimal_place *= 10.0
                result += digit / decimal_place
            else:
                result = result * 10.0 + digit
        else:
            return None
        i += 1
    if not digit_seen:
        return None
    return sign * result


class DataStream(ABC):
    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        self.processed_count = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "Stream ID": self.stream_id
            }


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            temps = 0
            count_temp = 0
            for data in data_batch:
                sen, val = data.split(":", 1)
                if sen == "temp":
                    val = my_float(val)
                    temps += val
                    count_temp += 1
            avg = temps / count_temp if count_temp > 0 else 0.0
            return (
                f"Sensor analysis: {my_len(data_batch)} readings processed, "
                f"avg temp: {avg:.1f}°C"
            )

        except Exception as e:
            return f"Error processing sensor data: {str(e)}"

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        if criteria == "critical":
            critical = []
            for data in data_batch:
                sen, val = data.split(":", 1)
                if sen == "temp" and my_float(val) > 40.0:
                    critical += [data]
                elif sen == "humidity" and my_float(val) > 70.0:
                    critical += [data]
                elif sen == "pressure" and my_float(val) < 1000.0:
                    critical += [data]
            return critical
        elif criteria == "normal":
            normal = []
            for data in data_batch:
                sen, val = data.split(":", 1)
                if sen == "temp" and 15.0 <= my_float(val) <= 30.0:
                    normal += [data]
                elif sen == "humidity" and 30.0 <= my_float(val) <= 70.0:
                    normal += [data]
                elif sen == "pressure" and 1000.0 <= my_float(val) <= 1020.0:
                    normal += [data]
            return normal

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "Stream ID": self.stream_id,
            "Type": "Enviromintal Data"}


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            netflow = 0
            for item in data_batch:
                tran, amount = item.split(":", 1)
                amount = my_float(amount)
                if tran == "buy":
                    netflow += amount
                elif tran == "sell":
                    netflow -= amount
            sig = "+" if netflow >= 0 else "-"
            return (
                f"Transaction analysis: {my_len(data_batch)} operations,"
                f" net flow: {sig}{netflow} "
            )
        except Exception as e:
            return f"Error processing transaction data: {str(e)}"

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        if criteria == "large":
            return [
                item for item in data_batch if
                my_float(item.split(":", 1)[1]) > 100.0
            ]
        elif criteria == "small":
            return [
                item for item in data_batch if
                my_float(item.split(":", 1)[1]) <= 50.0
            ]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"Stream ID": self.stream_id,
                "Type": "Financial Data"
                }


class EventStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            error_count = 0
            for event in data_batch:
                if "error" in event.lower():
                    error_count += 1
            return (
                f"Event analysis: {my_len(data_batch)} events , "
                f": {error_count} errors detected"
            )
        except Exception as e:
            return f"Error processing event data: {str(e)}"

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        if criteria == "error":
            return [d for d in data_batch if "error" in d.lower()]
        elif criteria == "login":
            return [d for d in data_batch if "login" in d.lower()]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"Stream ID": self.stream_id,
                "Type": "System Events"
                }


class StreamProcessor:
    def __init__(self):
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        if isinstance(stream, DataStream):
            self.streams.append(stream)
        else:
            print("Error: Invalid stream type.")

    def process_all(self, data: List[Any]) -> None:
        for i in range(my_len(self.streams)):
            stream = self.streams[i]
            stream.process_batch(data[i])
            prefix = (
                " - Sensor data" if isinstance(stream, SensorStream)
                else " - Transaction data" if isinstance(
                    stream, TransactionStream)
                else " - Event data"
            )
            stream.processed_count = + my_len(data[i])
            unit = (
                "readings" if isinstance(stream, SensorStream)
                else "operations" if isinstance(stream, TransactionStream)
                else "events"
            )
            print(f"{prefix}: {stream.processed_count}"
                  f"{unit} processed")


def main() -> None:
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    print("\nInitializing Sensor Stream...")
    sensor_stream = SensorStream("SENSOR_001")
    sensor_batch = ["temp:22.5", "humidity:65", "pressure:1013"]
    s_stats = sensor_stream.get_stats()
    print(f"Stream ID: {s_stats["Stream ID"]}, Type: {s_stats["Type"]}")
    print(f"Processing sensor batch: {sensor_batch}")
    print(sensor_stream.process_batch(sensor_batch))

    print("\nInitializing Transaction Stream...")
    tran_stream = TransactionStream("TRAN_001")
    tran_batch = ["buy:100", "sell:150", "buy:75"]
    print(f"Processing transaction batch:{tran_batch}")
    t_stats = tran_stream.get_stats()
    print(f"Stream Id: {t_stats["Stream ID"]}, Type: {t_stats["Type"]}")
    print(tran_stream.process_batch(tran_batch))

    print("\nInitializing Event Stream...")
    event_stream = EventStream("EVENT_001")
    event_batch = ["login", "error", "logout"]
    print(f"Processing event batch: {event_batch}")
    e_stats = event_stream.get_stats()
    print(f"Stream Id: {e_stats["Stream ID"]}, Type: {e_stats["Type"]}")
    print(event_stream.process_batch(event_batch))

    print("\n=== POLYMORPHIC STREAM PROCESSING  ===")
    print("Processing mixed stream types through unified interface...\n")

    processor = StreamProcessor()
    processor.add_stream(sensor_stream)
    processor.add_stream(tran_stream)
    processor.add_stream(event_stream)

    print("Batch 1 Results:")
    mixed_batches = [
        ["temp:40.1", "humidity:75.5"],
        ["buy:110", "sell:90", "buy:60", "buy:10"],
        ["login", "logout", "error"]
        ]
    processor.process_all(mixed_batches)

    print("\nStream filtering active: High-priority data only")
    filtered_sensor_data = sensor_stream.filter_data(mixed_batches[0],
                                                     "critical")
    filtered_tran_data = tran_stream.filter_data(mixed_batches[1], "large")
    filtered_event_data = event_stream.filter_data(mixed_batches[2], "error")
    print("Filtered results:", end="")
    if filtered_sensor_data:
        print(f"{my_len(filtered_sensor_data)} critical sensor alerts, ",
              end="")
    if filtered_tran_data:
        print(f"{my_len(filtered_tran_data)} large transactions, ", end="")
    if filtered_event_data:
        print(f"{my_len(filtered_event_data)} error events")
    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
