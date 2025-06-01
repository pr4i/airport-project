"""add full_name and passport to checkins

Revision ID: 01881cc2be12
Revises: 6443f78e3568
Create Date: 2025-06-01 21:46:28.281314
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '01881cc2be12'
down_revision = '6443f78e3568'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('airports', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.create_unique_constraint('uq_airports_code', ['code'])

    with op.batch_alter_table('checkins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.String(length=128), nullable=False))
        batch_op.add_column(sa.Column('passport', sa.String(length=32), nullable=False))
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)

    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('airplane_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('price',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_unique_constraint('uq_flights_flight_number', ['flight_number'])

    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('flight_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key('fk_tickets_user_id', 'users', ['user_id'], ['id'])

def downgrade():
    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tickets_user_id', type_='foreignkey')
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('flight_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('flights', schema=None) as batch_op:
        batch_op.drop_constraint('uq_flights_flight_number', type_='unique')
        batch_op.alter_column('price',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('airplane_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    with op.batch_alter_table('checkins', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
        batch_op.drop_column('passport')
        batch_op.drop_column('full_name')

    with op.batch_alter_table('airports', schema=None) as batch_op:
        batch_op.drop_constraint('uq_airports_code', type_='unique')
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
