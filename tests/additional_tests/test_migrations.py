import os
import pytest
import subprocess


@pytest.mark.skipif(not os.getenv("DATABASE_URL"), reason="DATABASE_URL is not set")
def test_alembic_migration_runs():
    """Test if alembic migration runs without error using the current DATABASE_URL."""
    try:
        # Run 'alembic upgrade head' as subprocess
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "Running upgrade" in result.stdout or result.returncode == 0
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Alembic migration failed:\n{e.stderr}")

