#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Models representing secrets."""

from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, SecretStr

from zenml.enums import (
    GenericFilterOps,
    LogicalOperators,
    SecretScope,
    SorterOps,
)
from zenml.models.base_models import (
    WorkspaceScopedRequestModel,
    WorkspaceScopedResponseModel,
    update_model,
)
from zenml.models.constants import STR_FIELD_MAX_LENGTH
from zenml.models.filter_models import WorkspaceScopedFilterModel

# ---- #
# BASE #
# ---- #


class SecretBaseModel(BaseModel):
    """Base model for secrets."""

    name: str = Field(
        title="The name of the secret.",
        max_length=STR_FIELD_MAX_LENGTH,
    )

    scope: SecretScope = Field(
        SecretScope.WORKSPACE, title="The scope of the secret."
    )

    values: Dict[str, Optional[SecretStr]] = Field(
        default_factory=dict, title="The values stored in this secret."
    )

    @property
    def secret_values(self) -> Dict[str, str]:
        """A dictionary with all un-obfuscated values stored in this secret.

        The values are returned as strings, not SecretStr. If a value is
        None, it is not included in the returned dictionary. This is to enable
        the use of None values in the update model to indicate that a secret
        value should be deleted.

        Returns:
            A dictionary containing the secret's values.
        """
        return {
            k: v.get_secret_value()
            for k, v in self.values.items()
            if v is not None
        }

    def add_secret(self, key: str, value: str) -> None:
        """Adds a secret value to the secret.

        Args:
            key: The key of the secret value.
            value: The secret value.
        """
        self.values[key] = SecretStr(value)

    def remove_secret(self, key: str) -> None:
        """Removes a secret value from the secret.

        Args:
            key: The key of the secret value.
        """
        del self.values[key]

    def remove_secrets(self) -> None:
        """Removes all secret values from the secret but keep the keys."""
        self.values = {k: None for k in self.values.keys()}


# -------- #
# RESPONSE #
# -------- #


class SecretResponseModel(SecretBaseModel, WorkspaceScopedResponseModel):
    """Secret response model with user and workspace hydrated."""

    ANALYTICS_FIELDS: ClassVar[List[str]] = ["scope"]


# ------ #
# FILTER #
# ------ #


class SecretFilterModel(WorkspaceScopedFilterModel):
    """Model to enable advanced filtering of all Secrets."""

    FILTER_EXCLUDE_FIELDS: ClassVar[List[str]] = [
        *WorkspaceScopedFilterModel.FILTER_EXCLUDE_FIELDS,
        "values",
    ]

    name: Optional[str] = Field(
        default=None,
        description="Name of the secret",
    )

    scope: Optional[Union[SecretScope, str]] = Field(
        default=None,
        description="Scope in which to filter secrets",
    )

    workspace_id: Optional[Union[UUID, str]] = Field(
        default=None, description="Workspace of the Secret"
    )

    user_id: Optional[Union[UUID, str]] = Field(
        None, description="User that created the Secret"
    )

    @staticmethod
    def _get_filtering_value(value: Optional[Any]) -> str:
        """Convert the value to a string that can be used for lexicographical filtering and sorting.

        Args:
            value: The value to convert.

        Returns:
            The value converted to string format that can be used for
            lexicographical sorting and filtering.
        """
        if value is None:
            return ""
        str_value = str(value)
        if isinstance(value, datetime):
            str_value = value.strftime("%Y-%m-%d %H:%M:%S")
        return str_value

    def secret_matches(self, secret: SecretResponseModel) -> bool:
        """Checks if a secret matches the filter criteria.

        Args:
            secret: The secret to check.

        Returns:
            True if the secret matches the filter criteria, False otherwise.
        """
        for filter in self.list_of_filters:
            column_value: Optional[Any] = None
            if filter.column == "workspace_id":
                column_value = secret.workspace.id
            elif filter.column == "user_id":
                column_value = secret.user.id if secret.user else None
            else:
                column_value = getattr(secret, filter.column)

            # Convert the values to strings for lexicographical comparison.
            str_column_value = self._get_filtering_value(column_value)
            str_filter_value = self._get_filtering_value(filter.value)

            # Compare the lexicographical values according to the operation.
            if filter.operation == GenericFilterOps.EQUALS:
                result = str_column_value == str_filter_value
            elif filter.operation == GenericFilterOps.CONTAINS:
                result = str_filter_value in str_column_value
            elif filter.operation == GenericFilterOps.STARTSWITH:
                result = str_column_value.startswith(str_filter_value)
            elif filter.operation == GenericFilterOps.ENDSWITH:
                result = str_column_value.endswith(str_filter_value)
            elif filter.operation == GenericFilterOps.GT:
                result = str_column_value > str_filter_value
            elif filter.operation == GenericFilterOps.GTE:
                result = str_column_value >= str_filter_value
            elif filter.operation == GenericFilterOps.LT:
                result = str_column_value < str_filter_value
            elif filter.operation == GenericFilterOps.LTE:
                result = str_column_value <= str_filter_value

            # Exit early if the result is False for AND and True for OR
            if self.logical_operator == LogicalOperators.AND:
                if not result:
                    return False
            else:
                if result:
                    return True

        # If we get here, all filters have been checked and the result is
        # True for AND and False for OR
        if self.logical_operator == LogicalOperators.AND:
            return True
        else:
            return False

    def sort_secrets(
        self, secrets: List[SecretResponseModel]
    ) -> List[SecretResponseModel]:
        """Sorts a list of secrets according to the filter criteria.

        Args:
            secrets: The list of secrets to sort.

        Returns:
            The sorted list of secrets.
        """
        column, sort_op = self.sorting_params
        sorted_secrets = sorted(
            secrets,
            key=lambda secret: self._get_filtering_value(
                getattr(secret, column)
            ),
            reverse=sort_op == SorterOps.DESCENDING,
        )

        return sorted_secrets


# ------- #
# REQUEST #
# ------- #


class SecretRequestModel(SecretBaseModel, WorkspaceScopedRequestModel):
    """Secret request model."""

    ANALYTICS_FIELDS: ClassVar[List[str]] = ["scope"]


# ------ #
# UPDATE #
# ------ #


@update_model
class SecretUpdateModel(SecretRequestModel):
    """Secret update model."""

    scope: Optional[SecretScope] = Field(  # type: ignore[assignment]
        None, title="The scope of the secret."
    )
