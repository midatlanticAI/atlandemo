from src.cog_config import CogConfig
from src.temporal_cognition import TemporalCognitionEngine


def test_dog_bark_schema():
    cfg = CogConfig(
        deterministic=True,
        seed=123,
        consolidation_threshold=0.5,  # relaxed for unit test
        schema_support_threshold=3,
        save_frequency=1000,
        store_backend="json",
        store_path=":memory:",
    )

    engine = TemporalCognitionEngine(config=cfg)

    # Feed enough frames to surpass support threshold reliably
    for _ in range(10):
        engine.live_experience(visual=["dog"], auditory=["bark"])

    schemas = engine.experience_stream.schemas
    assert ("bark", "dog") in schemas or ("dog", "bark") in schemas
    sch = schemas.get(("bark", "dog")) or schemas.get(("dog", "bark"))
    assert sch.count >= cfg.schema_support_threshold 