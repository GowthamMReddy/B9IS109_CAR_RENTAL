"""empty message

Revision ID: f3f5a4e87234
Revises: db7d694cbbca
Create Date: 2023-03-14 00:04:13.210671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3f5a4e87234'
down_revision = 'db7d694cbbca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_booking')
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('booking_from_date',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('booking_to_date',
               existing_type=sa.DATETIME(),
               nullable=False)

    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.add_column(sa.Column('car_capacity', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('car_type', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('car_price', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('location_Id', sa.Integer(), nullable=True))
        batch_op.alter_column('car_modelid',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('car_name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
        batch_op.alter_column('car_no',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_car_car_modelid'), ['car_modelid'])
        batch_op.create_unique_constraint(batch_op.f('uq_car_car_no'), ['car_no'])
        batch_op.create_foreign_key(batch_op.f('fk_car_location_Id_location'), 'location', ['location_Id'], ['id'])
        batch_op.drop_column('car_features')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('contact',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])
        batch_op.drop_column('dob')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dob', sa.DATETIME(), nullable=True))
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('contact',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.drop_column('age')

    with op.batch_alter_table('car', schema=None) as batch_op:
        batch_op.add_column(sa.Column('car_features', sa.VARCHAR(length=500), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_car_location_Id_location'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('uq_car_car_no'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_car_car_modelid'), type_='unique')
        batch_op.alter_column('car_no',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('car_name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.alter_column('car_modelid',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.drop_column('location_Id')
        batch_op.drop_column('car_price')
        batch_op.drop_column('car_type')
        batch_op.drop_column('car_capacity')

    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('booking_to_date',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('booking_from_date',
               existing_type=sa.DATETIME(),
               nullable=True)

    op.create_table('_alembic_tmp_booking',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('booking_date', sa.DATETIME(), nullable=True),
    sa.Column('booking_from_date', sa.DATETIME(), nullable=False),
    sa.Column('booking_to_date', sa.DATETIME(), nullable=False),
    sa.Column('car_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
