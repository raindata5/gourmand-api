"""verified flag

Revision ID: c8cdc2770046
Revises: 060f6cb78efd
Create Date: 2023-10-13 04:07:50.714723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8cdc2770046'
down_revision = '060f6cb78efd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authuser', sa.Column('verified', sa.Boolean(), server_default=sa.text('false'), nullable=False), schema='_Production')
    op.create_foreign_key('fk_business_paymentlevel', 'business', 'paymentlevel', ['paymentlevelid'], ['paymentlevelid'], source_schema='_Production', referent_schema='_Production', ondelete='CASCADE')
    op.create_foreign_key('fk_business_city', 'business', 'city', ['cityid'], ['cityid'], source_schema='_Production', referent_schema='_Production', ondelete='CASCADE')
    op.create_foreign_key('fk_business_state', 'business', 'state', ['stateid'], ['stateid'], source_schema='_Production', referent_schema='_Production')
    op.create_foreign_key('fk_business_county', 'business', 'county', ['countyid'], ['countyid'], source_schema='_Production', referent_schema='_Production')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('authuser', 'verified', schema='_Production')
    op.drop_constraint('fk_business_county', 'business', schema='_Production', type_='foreignkey')
    op.drop_constraint('fk_business_state', 'business', schema='_Production', type_='foreignkey')
    op.drop_constraint('fk_business_city', 'business', schema='_Production', type_='foreignkey')
    op.drop_constraint('fk_business_paymentlevel', 'business', schema='_Production', type_='foreignkey')
    
    # ### end Alembic commands ###
