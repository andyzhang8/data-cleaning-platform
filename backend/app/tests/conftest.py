import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, get_db
from unittest.mock import patch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Set up an in-memory SQLite database for testing
@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)  # Create schema
    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)  # Drop schema


@pytest.fixture(scope="function")
def mock_get_db(test_db):
    def _get_db():
        db = test_db()
        try:
            yield db
        finally:
            db.close()

    with patch("app.models.database.get_db", _get_db):
        yield
