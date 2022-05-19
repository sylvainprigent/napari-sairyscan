"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/plugins/guides.html?#sample-data

Replace code below according to your needs.
"""
from __future__ import annotations

from sairyscan.data import celegans


def make_sample_data():
    """load SAiryscan data"""
    return [(celegans().detach().numpy(), {"name": "C. elegans"})]
