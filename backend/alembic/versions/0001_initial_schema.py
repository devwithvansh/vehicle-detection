"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-31 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("admin", "operator", name="userrole"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vehicle_number", sa.String(length=32), nullable=False),
        sa.Column("driver_name", sa.String(length=120), nullable=False),
        sa.Column("unit_name", sa.String(length=120), nullable=False),
        sa.Column("vehicle_type", sa.String(length=80), nullable=False),
        sa.Column("purpose", sa.String(length=160), nullable=False),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("operator_name", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vehicles_id"), "vehicles", ["id"], unique=False)
    op.create_index(op.f("ix_vehicles_vehicle_number"), "vehicles", ["vehicle_number"], unique=True)

    op.create_table(
        "camera_locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("stream_url", sa.String(length=500), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_camera_locations_id"), "camera_locations", ["id"], unique=False)

    op.create_table(
        "captured_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("original_path", sa.String(length=500), nullable=False),
        sa.Column("processed_path", sa.String(length=500), nullable=True),
        sa.Column("detected_number", sa.String(length=32), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("camera_location_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["camera_location_id"], ["camera_locations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_captured_images_detected_number"), "captured_images", ["detected_number"], unique=False)
    op.create_index(op.f("ix_captured_images_id"), "captured_images", ["id"], unique=False)

    op.create_table(
        "vehicle_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=False),
        sa.Column("operator_id", sa.Integer(), nullable=False),
        sa.Column("camera_location_id", sa.Integer(), nullable=True),
        sa.Column("captured_image_id", sa.Integer(), nullable=True),
        sa.Column("movement_type", sa.Enum("entry", "exit", name="movementtype"), nullable=False),
        sa.Column("entry_time", sa.DateTime(), nullable=True),
        sa.Column("exit_time", sa.DateTime(), nullable=True),
        sa.Column("confidence_score", sa.Float(), nullable=True),
        sa.Column("audit_note", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["camera_location_id"], ["camera_locations.id"]),
        sa.ForeignKeyConstraint(["captured_image_id"], ["captured_images.id"]),
        sa.ForeignKeyConstraint(["operator_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vehicle_logs_id"), "vehicle_logs", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_vehicle_logs_id"), table_name="vehicle_logs")
    op.drop_table("vehicle_logs")
    op.drop_index(op.f("ix_captured_images_id"), table_name="captured_images")
    op.drop_index(op.f("ix_captured_images_detected_number"), table_name="captured_images")
    op.drop_table("captured_images")
    op.drop_index(op.f("ix_camera_locations_id"), table_name="camera_locations")
    op.drop_table("camera_locations")
    op.drop_index(op.f("ix_vehicles_vehicle_number"), table_name="vehicles")
    op.drop_index(op.f("ix_vehicles_id"), table_name="vehicles")
    op.drop_table("vehicles")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
