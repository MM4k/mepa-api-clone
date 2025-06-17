import logging
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

logger = logging.getLogger("tasks")


class Command(BaseCommand):
    help = "Backup the database."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--max_backups", type=int, default=7)

    def handle(self, *args, **options) -> None:
        logger.info("-" * 90)
        logger.info("Backup database - Starting...")
        start_time = timezone.now()

        max_backups = options["max_backups"]
        backup_path = settings.BASE_DIR / "backups"
        backup_path.mkdir(parents=True, exist_ok=True)

        db_name = settings.DATABASES["default"]["NAME"]
        timestamp = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = backup_path / f"bkp_{db_name}_{timestamp}.dump.gz"
        logger.info(f"Backup path: {backup_file}")

        self.perform_backup(backup_file)
        self.clean_backups(backup_path, max_backups)

        duration = timezone.now() - start_time
        logger.info(f"Time elapsed: {duration.total_seconds()} seconds")

    def perform_backup(self, backup_file) -> None:
        logger.info("Running backup command...")

        db_config = settings.DATABASES["default"]

        pg_dump_cmd = [
            "pg_dump",
            "-h",
            db_config["HOST"],
            "-U",
            db_config["USER"],
            "-d",
            db_config["NAME"],
            "-p",
            str(db_config["PORT"]),
            "-F",
            "c",  # Utilizar pg_restore para restaurar
            "--no-password",
        ]

        try:
            self._run_pg_dump(pg_dump_cmd, db_config, backup_file)
        except subprocess.CalledProcessError as e:
            logger.error(f"pg_dump command failed: {e}")
            logger.error(f"Command output: {e.stdout}")
            logger.error(f"Command error: {e.stderr}")
            raise

    def _run_pg_dump(self, pg_dump_cmd, db_config, backup_file):
        with open(backup_file, "wb") as file_out:
            pg_dump_process = subprocess.Popen(
                pg_dump_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={"PGPASSWORD": db_config["PASSWORD"]},
            )

            gzip_process = subprocess.Popen(
                ["gzip", "-c"],
                stdin=pg_dump_process.stdout,
                stderr=subprocess.PIPE,
                stdout=file_out,
            )

            pg_dump_process.stdout.close()
            gzip_process.wait()
            pg_dump_process.wait()

        db_size = backup_file.stat().st_size
        db_size = round(db_size / 1024, 2)
        logger.info(f"Backup completed successfully. File size: {db_size:} KB")

    def clean_backups(self, backup_path, max_backups) -> None:
        logger.info("Verifying old backups...")
        backups = sorted(backup_path.glob("*.dump.gz"), reverse=True)

        if len(backups) <= max_backups:
            logger.info("No old backups to remove.")
            return

        for backup in backups[max_backups:]:
            logger.info(f"Removing old backup: {backup.name}")
            backup.unlink()
