#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
""" A client library for accessing IVCAP """

# read version from installed package
try:  # Python < 3.10 (backport) 
    from importlib_metadata import version 
except ImportError: 
    from importlib.metadata import version 
__version__ = version("ivcap_client")

from .ivcap import IVCAP
from .service import Service
from .order import Order
from .artifact import Artifact
from .metadata import Metadata

# __all__ = (
#     "IVCAP",
# )
