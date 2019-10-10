"""empty message

Revision ID: 10cca4d908ed
Revises: 
Create Date: 2019-10-09 20:19:32.158033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10cca4d908ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('abouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('slogan', sa.String(length=128), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_abouts_add_time'), 'abouts', ['add_time'], unique=False)
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('slogan', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('slogan', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('isdraft', sa.Boolean(), nullable=True),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.Column('cate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cate_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_articles_add_time'), 'articles', ['add_time'], unique=False)
    op.create_index(op.f('ix_articles_url'), 'articles', ['url'], unique=False)
    op.create_table('article_tag',
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_tag')
    op.drop_index(op.f('ix_articles_url'), table_name='articles')
    op.drop_index(op.f('ix_articles_add_time'), table_name='articles')
    op.drop_table('articles')
    op.drop_table('tags')
    op.drop_table('categories')
    op.drop_index(op.f('ix_abouts_add_time'), table_name='abouts')
    op.drop_table('abouts')
    # ### end Alembic commands ###
