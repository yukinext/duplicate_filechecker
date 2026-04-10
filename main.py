import sys

from duplicate_filechecker.cli import app, maintenance_purge_missing

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "maintenance" and sys.argv[2] == "purge-missing":
        db_path = "duplicates.db"
        if "--db-path" in sys.argv:
            i = sys.argv.index("--db-path")
            if i + 1 < len(sys.argv):
                db_path = sys.argv[i + 1]
        maintenance_purge_missing(db_path)
    else:
        app()
