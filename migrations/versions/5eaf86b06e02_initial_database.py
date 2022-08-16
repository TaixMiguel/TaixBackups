"""Restore database

Revision ID: 5eaf86b06e02
Revises: 
Create Date: 2022-06-16 18:04:50.413049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eaf86b06e02'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dbackup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('server', sa.String(length=8), nullable=False),
    sa.Column('source_dir', sa.String(length=256), nullable=False),
    sa.Column('destination_dir', sa.String(length=256), nullable=False),
    sa.Column('user', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('n_backups_max', sa.Integer(), nullable=True),
    sa.Column('sw_sensor_mqtt', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('hbackup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_backup_fk', sa.Integer(), nullable=False),
    sa.Column('backup_name', sa.String(), nullable=False),
    sa.Column('backup_size', sa.Float(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('duration', sa.Float(), nullable=True),
    sa.Column('audit_date', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['id_backup_fk'], ['dbackup.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hbackup')
    op.drop_table('dbackup')
    # ### end Alembic commands ###
