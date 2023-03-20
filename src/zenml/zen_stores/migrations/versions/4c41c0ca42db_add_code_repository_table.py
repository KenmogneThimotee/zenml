"""Add code repository table [4c41c0ca42db].

Revision ID: 4c41c0ca42db
Revises: 0.35.1
Create Date: 2023-02-21 13:53:23.479592

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "4c41c0ca42db"
down_revision = "0.36.0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "code_repository",
        sa.Column(
            "workspace_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("config", sa.TEXT(), nullable=False),
        sa.Column("source", sa.TEXT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name="fk_code_repository_user_id_user",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspace.id"],
            name="fk_code_repository_workspace_id_workspace",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "code_reference",
        sa.Column(
            "workspace_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column(
            "code_repository_id", sqlmodel.sql.sqltypes.GUID(), nullable=False
        ),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column(
            "commit", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "subdirectory", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["code_repository_id"],
            ["code_repository.id"],
            name="fk_code_reference_code_repository_id_code_repository",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspace.id"],
            name="fk_code_reference_workspace_id_workspace",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("pipeline_deployment", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "code_reference_id",
                sqlmodel.sql.sqltypes.GUID(),
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            "fk_pipeline_deployment_code_reference_id_code_reference",
            "code_reference",
            ["code_reference_id"],
            ["id"],
            ondelete="SET NULL",
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("code_repository")
    with op.batch_alter_table("pipeline_deployment", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_pipeline_deployment_code_reference_id_code_reference",
            type_="foreignkey",
        )
        batch_op.drop_column("code_reference_id")

    op.drop_table("code_reference")
    # ### end Alembic commands ###
