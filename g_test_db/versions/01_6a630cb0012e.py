"""empty message

Revision ID: 6a630cb0012e
Revises: 
Create Date: 2022-01-06 16:55:05.971069

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6a630cb0012e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authuser',
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('userid'),
    sa.UniqueConstraint('email'),
    schema='_Production'
    )
    op.create_table('business',
    sa.Column('businessid', sa.Integer(), nullable=False),
    sa.Column('businessname', sa.String(), nullable=False),
    sa.Column('chainname', sa.String(), nullable=False),
    sa.Column('addressline1', sa.String(), nullable=False),
    sa.Column('addressline2', sa.String(), nullable=True),
    sa.Column('addressline3', sa.String(), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=8, scale=6), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=9, scale=6), nullable=True),
    sa.Column('zipcode', sa.String(), nullable=True),
    sa.Column('businessphone', sa.String(), nullable=True),
    sa.Column('businessurl', sa.String(length=500), nullable=True),
    sa.Column('is_closed', sa.Boolean(), nullable=False),
    sa.Column('distancetocounty', sa.Integer(), nullable=True),
    sa.Column('cityid', sa.Integer(), nullable=True),
    sa.Column('countyid', sa.Integer(), nullable=True),
    sa.Column('stateid', sa.Integer(), nullable=True),
    sa.Column('paymentlevelid', sa.Integer(), nullable=True),
    sa.Column('lasteditedwhen', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('businessid'),
    schema='_Production'
    )
    op.create_table('businessholding',
    sa.Column('businessholdingid', sa.Integer(), nullable=False),
    sa.Column('businessid', sa.Integer(), nullable=False),
    sa.Column('businessrating', sa.Numeric(precision=2, scale=1), nullable=True),
    sa.Column('reviewcount', sa.Integer(), nullable=True),
    sa.Column('closedate', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['businessid'], ['_Production.business.businessid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('businessholdingid'),
    schema='_Production'
    )
    op.drop_table('transactiontype')
    op.drop_index('ix_businessholding_businessid', table_name='businessholding')
    op.drop_index('ix_businessholding_closedate', table_name='businessholding')
    op.drop_table('businessholding')
    op.drop_table('paymentlevel')
    op.drop_table('businesstransactionbridge')
    op.drop_table('businesscategorybridge')
    op.drop_table('businesscategory')
    op.drop_table('city')
    op.drop_table('country')
    op.drop_table('state')
    op.drop_table('authuser')
    op.drop_table('county')
    op.drop_index('ix_business_chainname', table_name='business')
    op.drop_index('ix_business_cityid', table_name='business')
    op.drop_index('ix_business_countyid', table_name='business')
    op.drop_index('ix_business_paymentlevelid', table_name='business')
    op.drop_index('ix_business_stateid', table_name='business')
    op.drop_table('business')
    op.drop_table('eventcategory')
    op.drop_table('review')
    op.drop_table('user')
    op.drop_table('event')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('eventid', sa.INTEGER(), server_default=sa.text('nextval(\'"Event2_eventid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('businessid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('eventname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('attending', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('costofattending', sa.NUMERIC(precision=16, scale=2), autoincrement=False, nullable=True),
    sa.Column('is_free', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('eventdescription', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('interested', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cityid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('latitude', sa.NUMERIC(precision=8, scale=6), autoincrement=False, nullable=True),
    sa.Column('longitude', sa.NUMERIC(precision=9, scale=6), autoincrement=False, nullable=True),
    sa.Column('zipcode', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('starttime', postgresql.TIMESTAMP(timezone=True, precision=3), autoincrement=False, nullable=True),
    sa.Column('endtime', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.Column('ticketsurl', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('eventsiteurl', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('canceldate', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('officialdate', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('createdat', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['businessid'], ['business.businessid'], name='fk_event_business', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['cityid'], ['city.cityid'], name='fk_event_city'),
    sa.PrimaryKeyConstraint('eventid', name='Event2_pkey')
    )
    op.create_table('user',
    sa.Column('userid', sa.INTEGER(), server_default=sa.text('nextval(\'"User2_userid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('userprofileurl', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('userimageurl', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('firstname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lastnameinitial', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('userid', name='User2_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('review',
    sa.Column('reviewid', sa.INTEGER(), server_default=sa.text('nextval(\'"Review2_reviewid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('reviewurl', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('reviewextract', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('reviewrating', sa.NUMERIC(precision=28, scale=0), autoincrement=False, nullable=True),
    sa.Column('userid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('businessid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('createdat', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('insertedat', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['businessid'], ['business.businessid'], name='fk_review_business', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], name='fk_review_user', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('reviewid', name='Review2_pkey')
    )
    op.create_table('eventcategory',
    sa.Column('eventcategoryid', sa.INTEGER(), server_default=sa.text('nextval(\'"EventCategory2_eventcategoryid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('eventcategoryname', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('eventcategoryid', name='EventCategory2_pkey')
    )
    op.create_table('business',
    sa.Column('businessid', sa.INTEGER(), server_default=sa.text('nextval(\'"Business2_businessid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('businessname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('chainname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('addressline1', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('addressline2', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('addressline3', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('latitude', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('longitude', sa.NUMERIC(), autoincrement=False, nullable=True),
    sa.Column('zipcode', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('businessphone', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('businessurl', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('is_closed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('distancetocounty', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cityid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('countyid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('stateid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('paymentlevelid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=6), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cityid'], ['city.cityid'], name='fk_business_city', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['countyid'], ['county.countyid'], name='fk_business_county'),
    sa.ForeignKeyConstraint(['paymentlevelid'], ['paymentlevel.paymentlevelid'], name='fk_business_paymentlevel', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['stateid'], ['state.stateid'], name='fk_business_state'),
    sa.PrimaryKeyConstraint('businessid', name='Business2_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_business_stateid', 'business', ['stateid'], unique=False)
    op.create_index('ix_business_paymentlevelid', 'business', ['paymentlevelid'], unique=False)
    op.create_index('ix_business_countyid', 'business', ['countyid'], unique=False)
    op.create_index('ix_business_cityid', 'business', ['cityid'], unique=False)
    op.create_index('ix_business_chainname', 'business', ['chainname'], unique=False)
    op.create_table('county',
    sa.Column('countyid', sa.INTEGER(), server_default=sa.text('nextval(\'"County2_countyid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('countyname', sa.VARCHAR(length=85), autoincrement=False, nullable=True),
    sa.Column('stateid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['stateid'], ['state.stateid'], name='fk_county_state', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('countyid', name='County2_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('authuser',
    sa.Column('userid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('password', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(precision=6), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('userid', name='authuser_pkey')
    )
    op.create_table('state',
    sa.Column('stateid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('statename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('abrvstate', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('countryid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['countryid'], ['country.countryid'], name='fk_state_country', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('stateid', name='pk_state_stateid'),
    postgresql_ignore_search_path=False
    )
    op.create_table('country',
    sa.Column('countryid', sa.INTEGER(), server_default=sa.text("nextval('country2_countryid_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('countryname', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('countryid', name='country2_pkey'),
    sa.UniqueConstraint('countryname', name='country2_countryname_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('city',
    sa.Column('cityid', sa.INTEGER(), server_default=sa.text('nextval(\'"City2_cityid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('cityname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('stateid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('countyid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['countyid'], ['county.countyid'], name='fk_city_county'),
    sa.ForeignKeyConstraint(['stateid'], ['state.stateid'], name='fk_city_state', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('cityid', name='City2_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('businesscategory',
    sa.Column('categoryid', sa.INTEGER(), server_default=sa.text('nextval(\'"BusinessCategory2_categoryid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('categoryname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('categoryid', name='BusinessCategory2_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('businesscategorybridge',
    sa.Column('businessid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('categoryid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['businessid'], ['business.businessid'], name='fk_businesscategorybridge_business', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['categoryid'], ['businesscategory.categoryid'], name='fk_businesscategorybridge_businesscategory', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('businessid', 'categoryid', name='pk_businesscategorybridge_businessid_categoryid')
    )
    op.create_table('businesstransactionbridge',
    sa.Column('businessid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('transactionid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['businessid'], ['business.businessid'], name='fk_businesstransactionbridge_business', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['transactionid'], ['transactiontype.transactionid'], name='fk_businesstransactionbridge_transactiontype', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('businessid', 'transactionid', name='pk_businesstransactionbridge_businessid_transactionid')
    )
    op.create_table('paymentlevel',
    sa.Column('paymentlevelid', sa.INTEGER(), server_default=sa.text('nextval(\'"PaymentLevel2_paymentlevelid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('paymentlevelsymbol', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('paymentlevelname', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('paymentlevelid', name='PaymentLevel2_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('businessholding',
    sa.Column('businessholdingid', sa.INTEGER(), server_default=sa.text('nextval(\'"BusinessHolding2_businessholdingid_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('businessid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('businessrating', sa.NUMERIC(precision=2, scale=1), autoincrement=False, nullable=True),
    sa.Column('reviewcount', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('closedate', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['businessid'], ['business.businessid'], name='fk_businessholding_business', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('businessholdingid', name='BusinessHolding2_pkey')
    )
    op.create_index('ix_businessholding_closedate', 'businessholding', ['closedate'], unique=False)
    op.create_index('ix_businessholding_businessid', 'businessholding', ['businessid'], unique=False)
    op.create_table('transactiontype',
    sa.Column('transactionid', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('transactionname', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('lasteditedwhen', postgresql.TIMESTAMP(precision=3), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('transactionid', name='transactiontype2_pkey'),
    sa.UniqueConstraint('transactionname', name='transactiontype2_transactionname_key')
    )
    op.drop_table('businessholding', schema='_Production')
    op.drop_table('business', schema='_Production')
    op.drop_table('authuser', schema='_Production')
    # ### end Alembic commands ###