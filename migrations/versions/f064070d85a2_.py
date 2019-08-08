"""Initial DB Migration

Revision ID: f064070d85a2
Revises:
Create Date: 2019-08-09 19:33:29.832680

"""
import uuid
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.sql import table, column
from sqlalchemy_utils import ColorType
from alembic import op, context
from colour import Color


# revision identifiers, used by Alembic.
revision = "f064070d85a2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get("data", None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get("data", None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "mood_template",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "team",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "team_role",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "membership",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["team_role.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["team.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "mood",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column(
            "colour", sqlalchemy_utils.types.color.ColorType(length=20), nullable=False
        ),
        sa.Column("template_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["template_id"], ["mood_template.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "team_member_mood",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=100), nullable=False),
        sa.Column("mood_id", sa.Integer(), nullable=True),
        sa.Column("team_member_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["mood_id"], ["mood.id"]),
        sa.ForeignKeyConstraint(["team_member_id"], ["membership.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    # ### end Alembic commands ###


def schema_downgrades():
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("team_member_mood")
    op.drop_table("mood")
    op.drop_table("membership")
    op.drop_table("user")
    op.drop_table("team_role")
    op.drop_table("team")
    op.drop_table("mood_template")
    # ### end Alembic commands ###


def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    team_role = table(
        "team_role",
        column("id", sa.Integer),
        column("public_id", sa.String),
        column("name", sa.String),
    )
    op.bulk_insert(
        team_role,
        [
            {"public_id": str(uuid.uuid4()), "name": "Admin"},
            {"public_id": str(uuid.uuid4()), "name": "Member"},
        ],
    )
    """ get the mood template table"""
    template = table(
        "mood_template",
        column("id", sa.Integer),
        column("public_id", sa.String),
        column("name", sa.String),
    )
    op.bulk_insert(
        template, [{"public_id": str(uuid.uuid4()), "name": "Default Mood Template"}]
    )

    """ get the mood table"""
    mood = table(
        "mood",
        column("id", sa.Integer),
        column("public_id", sa.String),
        column("name", sa.String),
        column("colour", ColorType),
        column("template_id", sa.Integer),
    )
    op.bulk_insert(
        mood,
        [
            {
                "public_id": str(uuid.uuid4()),
                "name": "Amazing",
                "colour": Color("#53d192"),
                "template_id": 1,
            },
            {
                "public_id": str(uuid.uuid4()),
                "name": "Great",
                "colour": Color("#5e95ed"),
                "template_id": 1,
            },
            {
                "public_id": str(uuid.uuid4()),
                "name": "Okay",
                "colour": Color("#ede357"),
                "template_id": 1,
            },
            {
                "public_id": str(uuid.uuid4()),
                "name": "Poor",
                "colour": Color("#e28f53"),
                "template_id": 1,
            },
            {
                "public_id": str(uuid.uuid4()),
                "name": "Awful",
                "colour": Color("#e05f4e"),
                "template_id": 1,
            },
        ],
    )


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
