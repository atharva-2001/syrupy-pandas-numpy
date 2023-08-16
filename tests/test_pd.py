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
        try:
            # return np.loadtxt(snapshot_location).tolist()
            return pd.read_hdf(snapshot_location)
        except OSError:
            return None

    @classmethod
    def _write_snapshot_collection(
        cls, *, snapshot_collection: SnapshotCollection
    ) -> None:
        filepath, data = (
            snapshot_collection.location,
            next(iter(snapshot_collection)).data,
        )
        # np.savetxt(filepath, data)
        print(data, type(data))
        data.to_hdf(filepath, "/blah")

    def serialize(self, data: SerializableData, **kwargs: Any) -> str:
        return data


@pytest.fixture
def snapshot_pandas(snapshot):
    return snapshot.use_extension(PandasSnapshotExtenstion)


def test_pd(snapshot_pandas):
    data = [10,20,30,40,50,60]
    assert snapshot_pandas == pd.DataFrame(data, columns=['Numbers'])
