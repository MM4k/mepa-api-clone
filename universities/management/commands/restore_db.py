import logging
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

logger = logging.getLogger("tasks")


class Command(BaseCommand):
    help = "Restore database."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("backup_file", type=str)

    def handle(self, *args, **options) -> None:
        logger.info("-" * 90)
        logger.info("Restore database - Starting")
        start_time = timezone.now()

        backup_file = options["backup_file"]
        backup_file = settings.BASE_DIR / "backups" / backup_file
        db_config = settings.DATABASES["default"]

        if not backup_file.exists():
            logger.error(f"Backup file not found: {backup_file}")
            return

        try:
            self.drop_db(db_config)
            self.create_db(db_config)
            self.perform_restore(backup_file, db_config)
            logger.info("Restore completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed: {e}")
            raise

        duration = timezone.now() - start_time
        logger.info(f"Time elapsed: {duration.total_seconds()} seconds")

    def drop_db(self, db_config) -> None:
        logger.info("Dropping existing database:")

        drop_db_cmd = [
            "dropdb",
            "-h",
            db_config["HOST"],
            "-U",
            db_config["USER"],
            "--if-exists",
            db_config["NAME"],
            "--no-password",
        ]

        subprocess.run(drop_db_cmd, check=True, env={"PGPASSWORD": db_config["PASSWORD"]})
        logger.info(f"Database <{db_config['NAME']}> dropped successfully")

    def create_db(self, db_config) -> None:
        logger.info("Creating new database:")

        create_db_cmd = [
            "createdb",
            "-h",
            db_config["HOST"],
            "-U",
            db_config["USER"],
            db_config["NAME"],
            "--no-password",
        ]

        subprocess.run(create_db_cmd, check=True, env={"PGPASSWORD": db_config["PASSWORD"]})
        logger.info(f"New database {db_config['NAME']} created successfully")

    def perform_restore(self, backup_file, db_config) -> None:
        logger.info(f"Restoring database from backup: {backup_file.name}")

        pg_restore_cmd = [
            "pg_restore",
            "-h",
            db_config["HOST"],
            "-U",
            db_config["USER"],
            "-d",
            db_config["NAME"],
            "-p",
            str(db_config["PORT"]),
            "--no-password",
        ]

        if backup_file.suffix == ".gz":
            logger.info("Backup file is gzipped. Unzipping before restoring...")
            gunzip_process = subprocess.Popen(
                ["gunzip", "-c", str(backup_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            pg_restore_process = subprocess.Popen(
                pg_restore_cmd,
                stdin=gunzip_process.stdout,
                stderr=subprocess.PIPE,
                env={"PGPASSWORD": db_config["PASSWORD"]},
            )

            gunzip_process.stdout.close()
            gunzip_process.wait()
            pg_restore_process.wait()

            if gunzip_process.returncode != 0:
                raise Exception(f"Gunzip failed: {gunzip_process.stderr.read().decode()}")
            if pg_restore_process.returncode != 0:
                raise Exception(f"Restore failed: {pg_restore_process.stderr.read().decode()}")

        else:
            pg_restore_cmd.append(str(backup_file))
            pg_restore_process = subprocess.Popen(
                pg_restore_cmd,
                stderr=subprocess.PIPE,
                env={"PGPASSWORD": db_config["PASSWORD"]},
            )

            pg_restore_process.wait()
            if pg_restore_process.returncode != 0:
                raise Exception(f"Restore failed: {pg_restore_process.stderr.read().decode()}")
