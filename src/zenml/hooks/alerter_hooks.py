#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
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
"""Functionality for standard hooks."""

from typing import TYPE_CHECKING

from zenml.logger import get_logger

logger = get_logger(__name__)


if TYPE_CHECKING:
    from zenml.steps import BaseParameters, StepContext


def alerter_failure_hook(
    context: "StepContext", params: "BaseParameters", exception: BaseException
) -> None:
    """Standard failure hook that executes after step fails.

    This hook uses any `BaseAlerter` that is configured within the active stack to post a message.

    Args:
        context: Context of the step.
        params: Parameters used in the step.
        exception: Original exception that lead to step failing.
    """
    if context.stack and context.stack.alerter:
        message = "*Failure Hook Notification! Step failed!*" + "\n\n"
        message += f"Pipeline name: `{context.pipeline_name}`" + "\n"
        message += f"Run name: `{context.run_name}`" + "\n"
        message += f"Step name: `{context.step_name}`" + "\n"
        message += f"Parameters: `{params}`" + "\n"
        message += f"Exception: `({type(exception)}) {exception}`" + "\n\n"
        message += (
            f"Step Cache Enabled: `{'True' if context.cache_enabled else 'False'}`"
            + "\n"
        )
        context.stack.alerter.post(message)
    else:
        logger.warning(
            "Specified standard failure hook but no alerter configured in the stack. Skipping.."
        )


def alerter_success_hook(
    context: "StepContext", params: "BaseParameters"
) -> None:
    """Standard success hook that executes after step finishes successfully.

    This hook uses any `BaseAlerter` that is configured within the active stack to post a message.

    Args:
        context: Context of the step.
        params: Parameters used in the step.
    """
    if context.stack and context.stack.alerter:
        message = (
            "*Success Hook Notification! Step completed successfully*" + "\n\n"
        )
        message += f"Pipeline name: `{context.pipeline_name}`" + "\n"
        message += f"Run name: `{context.run_name}`" + "\n"
        message += f"Step name: `{context.step_name}`" + "\n"
        message += f"Parameters: `{params}`" + "\n"
        message += (
            f"Step Cache Enabled: `{'True' if context.cache_enabled else 'False'}`"
            + "\n"
        )
        context.stack.alerter.post(message)
    else:
        logger.warning(
            "Specified standard success hook but no alerter configured in the stack. Skipping.."
        )
