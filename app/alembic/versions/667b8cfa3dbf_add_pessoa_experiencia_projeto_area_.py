"""Add Pessoa, Experiencia, Projeto, Area, Papel, TipoAcordo and dependencies

Revision ID: 667b8cfa3dbf
Revises: 
Create Date: 2020-08-25 13:19:36.764309-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '667b8cfa3dbf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.Column('area_pai_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['area_pai_id'], ['tb_area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tb_area_id'), 'tb_area', ['id'], unique=False)
    op.create_table('tb_papel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tb_papel_id'), 'tb_papel', ['id'], unique=False)
    op.create_table('tb_pessoa',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('senha', sa.String(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('data_nascimento', sa.Date(), nullable=True),
    sa.Column('telefone', sa.String(), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=True),
    sa.Column('superusuario', sa.Boolean(), nullable=True),
    sa.Column('colaborador_id', sa.Integer(), nullable=True),
    sa.Column('idealizador_id', sa.Integer(), nullable=True),
    sa.Column('aliado_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['aliado_id'], ['tb_pessoa.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['colaborador_id'], ['tb_pessoa.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['idealizador_id'], ['tb_pessoa.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('usuario')
    )
    op.create_index(op.f('ix_tb_pessoa_email'), 'tb_pessoa', ['email'], unique=True)
    op.create_index(op.f('ix_tb_pessoa_id'), 'tb_pessoa', ['id'], unique=False)
    op.create_table('tb_projeto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.Column('visibilidade', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tb_projeto_id'), 'tb_projeto', ['id'], unique=False)
    op.create_table('tb_tipo_acordo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tb_tipo_acordo_id'), 'tb_tipo_acordo', ['id'], unique=False)
    op.create_table('tb_experiencia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.Column('organizacao', sa.String(), nullable=True),
    sa.Column('data_inicio', sa.Date(), nullable=True),
    sa.Column('data_fim', sa.Date(), nullable=True),
    sa.Column('pessoa_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pessoa_id'], ['tb_pessoa.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tb_experiencia_id'), 'tb_experiencia', ['id'], unique=False)
    op.create_table('tb_pessoa_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pessoa_id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['area_id'], ['tb_area.id'], ),
    sa.ForeignKeyConstraint(['pessoa_id'], ['tb_pessoa.id'], ),
    sa.PrimaryKeyConstraint('id', 'pessoa_id', 'area_id')
    )
    op.create_index(op.f('ix_tb_pessoa_area_id'), 'tb_pessoa_area', ['id'], unique=False)
    op.create_table('tb_pessoa_projeto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pessoa_id', sa.Integer(), nullable=True),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.Column('papel_id', sa.Integer(), nullable=True),
    sa.Column('projeto_id', sa.Integer(), nullable=True),
    sa.Column('tipo_acordo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['tb_area.id'], ),
    sa.ForeignKeyConstraint(['papel_id'], ['tb_papel.id'], ),
    sa.ForeignKeyConstraint(['pessoa_id'], ['tb_pessoa.id'], ),
    sa.ForeignKeyConstraint(['projeto_id'], ['tb_projeto.id'], ),
    sa.ForeignKeyConstraint(['tipo_acordo_id'], ['tb_tipo_acordo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tb_pessoa_projeto_id'), 'tb_pessoa_projeto', ['id'], unique=False)
    op.create_table('tb_projeto_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('projeto_id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['area_id'], ['tb_area.id'], ),
    sa.ForeignKeyConstraint(['projeto_id'], ['tb_projeto.id'], ),
    sa.PrimaryKeyConstraint('id', 'projeto_id', 'area_id')
    )
    op.create_index(op.f('ix_tb_projeto_area_id'), 'tb_projeto_area', ['id'], unique=False)
    op.create_table('tb_area_pessoa_projeto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('pessoa_projeto_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['area_id'], ['tb_area.id'], ),
    sa.ForeignKeyConstraint(['pessoa_projeto_id'], ['tb_pessoa_projeto.id'], ),
    sa.PrimaryKeyConstraint('id', 'area_id', 'pessoa_projeto_id')
    )
    op.create_index(op.f('ix_tb_area_pessoa_projeto_id'), 'tb_area_pessoa_projeto', ['id'], unique=False)
    op.create_table('tb_experiencia_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('experiencia_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['area_id'], ['tb_area.id'], ),
    sa.ForeignKeyConstraint(['experiencia_id'], ['tb_experiencia.id'], ),
    sa.PrimaryKeyConstraint('id', 'area_id', 'experiencia_id')
    )
    op.create_index(op.f('ix_tb_experiencia_area_id'), 'tb_experiencia_area', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tb_experiencia_area_id'), table_name='tb_experiencia_area')
    op.drop_table('tb_experiencia_area')
    op.drop_index(op.f('ix_tb_area_pessoa_projeto_id'), table_name='tb_area_pessoa_projeto')
    op.drop_table('tb_area_pessoa_projeto')
    op.drop_index(op.f('ix_tb_projeto_area_id'), table_name='tb_projeto_area')
    op.drop_table('tb_projeto_area')
    op.drop_index(op.f('ix_tb_pessoa_projeto_id'), table_name='tb_pessoa_projeto')
    op.drop_table('tb_pessoa_projeto')
    op.drop_index(op.f('ix_tb_pessoa_area_id'), table_name='tb_pessoa_area')
    op.drop_table('tb_pessoa_area')
    op.drop_index(op.f('ix_tb_experiencia_id'), table_name='tb_experiencia')
    op.drop_table('tb_experiencia')
    op.drop_index(op.f('ix_tb_tipo_acordo_id'), table_name='tb_tipo_acordo')
    op.drop_table('tb_tipo_acordo')
    op.drop_index(op.f('ix_tb_projeto_id'), table_name='tb_projeto')
    op.drop_table('tb_projeto')
    op.drop_index(op.f('ix_tb_pessoa_id'), table_name='tb_pessoa')
    op.drop_index(op.f('ix_tb_pessoa_email'), table_name='tb_pessoa')
    op.drop_table('tb_pessoa')
    op.drop_index(op.f('ix_tb_papel_id'), table_name='tb_papel')
    op.drop_table('tb_papel')
    op.drop_index(op.f('ix_tb_area_id'), table_name='tb_area')
    op.drop_table('tb_area')
    # ### end Alembic commands ###