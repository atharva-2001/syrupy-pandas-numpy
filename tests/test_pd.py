"""Custom tests."""
from typing import Any, List, Tuple
import pytest
import numpy as np
from syrupy.data import SnapshotCollection
from syrupy.extensions.single_file import SingleFileSnapshotExtension
import pandas as pd
from syrupy.location import PyTestLocation
from syrupy.types import SerializableData, SerializedData, SnapshotIndex
from gettext import gettext


class PandasSnapshotExtenstion(SingleFileSnapshotExtension):
    _file_extension = "hdf"

    def matches(self, *, serialized_data, snapshot_data):
        try:
            if pd.testing.assert_frame_equal(
                serialized_data, snapshot_data
            )  is not None:
                return False
            else: return True
            
        except:
            return False

    def _read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str, session_id: str
    ):
        # see https://github.com/tophat/syrupy/blob/f4bc8453466af2cfa75cdda1d50d67bc8c4396c3/src/syrupy/extensions/base.py#L139
        try:
            return pd.read_hdf(snapshot_location)
        except OSError:
            return None

    @classmethod
    def _write_snapshot_collection(
        cls, *, snapshot_collection: SnapshotCollection
    ) -> None:
        # see https://github.com/tophat/syrupy/blob/f4bc8453466af2cfa75cdda1d50d67bc8c4396c3/src/syrupy/extensions/base.py#L161
        filepath, data = (
            snapshot_collection.location,
            next(iter(snapshot_collection)).data,
        )
        data.to_hdf(filepath, "/blah")

    def serialize(self, data: SerializableData, **kwargs: Any) -> str:
        return data


@pytest.fixture
def snapshot_pandas(snapshot):
    return snapshot.use_extension(PandasSnapshotExtenstion)


def test_pd(snapshot_pandas):
    data = [30,40,60]
    assert snapshot_pandas == pd.DataFrame(data, columns=['Numbers'])
