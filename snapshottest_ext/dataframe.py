import json
from io import BytesIO

import pandas as pd
from snapshottest.formatter import Formatter
from snapshottest.formatters import BaseFormatter


def get_timestamp_columns(df):
    object_cols = [
        col for col, dtype in df.dtypes.items() if dtype == 'object'
    ]
    timestamp_cols = [
        col for col in object_cols if isinstance(
            df[col].iloc[0], pd.Timestamp)]
    return timestamp_cols


def pandas_to_bytes(df: pd.DataFrame) -> str:
    buffer = BytesIO()
    df.to_parquet(buffer, use_deprecated_int96_timestamps=True)
    buffer.seek(0)
    buffer_bytes = buffer.read()
    dtypes_str = json.dumps(df.dtypes.astype(str).to_dict())
    return buffer_bytes + bytes(f'//SEP?//{dtypes_str}', 'utf-8')


def bytes_to_pandas(raw_bytes) -> pd.DataFrame:
    data_bytes, dtypes_bytes = raw_bytes.split(bytes('//SEP?//', 'utf-8'))
    df = pd.read_parquet(BytesIO(data_bytes))
    dtypes = json.loads(dtypes_bytes.decode())
    return df.astype(dtypes)


class PandasSnapshot(object):
    def __init__(self, value):
        self.value = value


class PandasFormatter(BaseFormatter):
    def can_format(self, value):
        """
        dispatcher, decide which format to use
        https://github.com/syrusakbary/snapshottest/blob/master/snapshottest/formatter.py
        @staticmethod
        def get_formatter(value):
            for formatter in Formatter.formatters:
                if formatter.can_format(value):
                    return formatter
        :param value:
        :return:
        """
        return isinstance(value, PandasSnapshot)

    def store(self, formatter, pandas_snap: PandasSnapshot):
        """ store pd.DataFrame as bytes in snapshot file"""
        return pandas_to_bytes(pandas_snap.value)

    def assert_value_matches_snapshot(
            self,
            test,
            test_value: PandasSnapshot,
            snapshot_value,
            formatter):
        """
        :param test:
        :param test_value: the value in snapshot.assert_mach(value)
        :param snapshot_value: the value of format.store (after load)
        """
        prev_df = bytes_to_pandas(
            snapshot_value)  # deserialize from bytes to pd.DataFrame
        timestamp_columns = get_timestamp_columns(test_value.value)
        nontimestamp_columns = list(
            set(test_value.value.columns).difference(timestamp_columns))

        pd.testing.assert_frame_equal(
            test_value.value[nontimestamp_columns],
            prev_df[nontimestamp_columns])


Formatter.register_formatter(PandasFormatter())
