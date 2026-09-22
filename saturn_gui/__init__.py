"""SATURN desktop interface for the shaftOpt rotordynamics workflow.

The GUI deliberately stays outside the numerical kernel.  It reads the same
baseline/configuration files and launches the existing Makefile targets, so the
engineering calculations remain owned by the validated shaftOpt pipeline.
"""

__all__ = ["__version__"]
__version__ = "2.0.0"
