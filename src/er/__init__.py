"""Entity Resolution modules."""
from .standardize import DataStandardizer
from .blocking import BlockingEngine
from .matching import FuzzyMatcher
from .clustering import EntityClusterer
from .pipeline import EntityResolutionPipeline

__all__ = [
    "DataStandardizer",
    "BlockingEngine", 
    "FuzzyMatcher",
    "EntityClusterer",
    "EntityResolutionPipeline",
]
