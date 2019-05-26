"""Added moods and default mood template data

Revision ID: 6a44006bdc40
Revises: 51d8287f4f55
Create Date: 2019-05-02 19:35:41.879250

"""
import uuid
from alembic import op, context
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy_utils import ColorType
from colour import Color


# revision identifiers, used by Alembic.
revision = '6a44006bdc40'
down_revision = '51d8287f4f55'
branch_labels = None
depends_on = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'mood',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('public_id', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('colour', ColorType(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['mood_template.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('public_id')
    )
    # ### end Alembic commands ###


def schema_downgrades():
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mood')
    # ### end Alembic commands ###


def data_upgrades():
    """ get the mood template table"""
    template = table(
        'mood_template',
        column('id', sa.Integer),
        column('public_id', sa.String),
        column('name', sa.String)
    )
    op.bulk_insert(
        template,
        [
            {
                'public_id': str(uuid.uuid4()),
                'name': 'Default Mood Template'
            }
        ]
    )

    """ get the mood table"""
    mood = table(
        'mood',
        column('id', sa.Integer),
        column('public_id', sa.String),
        column('name', sa.String),
        column('colour', ColorType),
        column('template_id', sa.Integer)
    )
    op.bulk_insert(
        mood,
        [
            {
                'public_id': str(uuid.uuid4()),
                'name': 'Amazing',
                'colour': Color('#53d192'),
                'template_id': 1
            },
            {
                'public_id': str(uuid.uuid4()),
                'name': 'Great',
                'colour': Color('#5e95ed'),
                'template_id': 1
            },
            {
                'public_id': str(uuid.uuid4()),
                'name': 'Okay',
                'colour': Color('#ede357'),
                'template_id': 1
            },
            {
                'public_id': str(uuid.uuid4()),
                'name': 'Poor',
                'colour': Color('#e28f53'),
                'template_id': 1
            },
            {
                'public_id': str(uuid.uuid4()),
                'name': 'Awful',
                'colour': Color('#e05f4e'),
                'template_id': 1
            }
        ]
    )


def data_downgrades():
    op.execute("delete from mood;")
    op.execute("delete from mood_template;")
