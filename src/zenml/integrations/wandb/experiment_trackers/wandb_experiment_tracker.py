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
"""Implementation for the wandb experiment tracker."""

import os
from contextlib import contextmanager
from typing import Iterator, Optional, Tuple, cast

import wandb

from zenml.experiment_trackers.base_experiment_tracker import (
    BaseExperimentTracker,
)
from zenml.integrations.wandb.flavors.wandb_experiment_tracker_flavor import (
    WandbExperimentTrackerConfig,
)
from zenml.logger import get_logger

logger = get_logger(__name__)


WANDB_API_KEY = "WANDB_API_KEY"


class WandbExperimentTracker(BaseExperimentTracker):
    """Stores wandb configuration options.

    ZenML should take care of configuring wandb for you, but should you still
    need access to the configuration inside your step you can do it using a
    step context:
    ```python
    from zenml.steps import StepContext

    @enable_wandb
    @step
    def my_step(context: StepContext, ...)
        context.stack.experiment_tracker  # get the tracking_uri etc. from here
    ```
    """

    @property
    def config(self) -> WandbExperimentTrackerConfig:
        """Returns the `WandbExperimentTrackerConfig` config.

        Returns:
            The configuration.
        """
        return cast(WandbExperimentTrackerConfig, self._config)

    def prepare_step_run(self) -> None:
        """Sets the wandb api key."""
        os.environ[WANDB_API_KEY] = self.config.api_key

    @contextmanager
    def activate_wandb_run(
        self,
        run_name: str,
        tags: Tuple[str, ...] = (),
        settings: Optional[wandb.Settings] = None,
    ) -> Iterator[None]:
        """Activates a wandb run for the duration of this context manager.

        Anything logged to wandb that is run while this context manager is
        active will automatically log to the same wandb run configured by the
        run name passed as an argument to this function.

        Args:
            run_name: Name of the wandb run to create.
            tags: Tags to attach to the wandb run.
            settings: Additional settings for the wandb run.

        Yields:
            None
        """
        try:
            logger.info(
                "Initializing wandb with project name: "
                f"{self.config.project_name}, run_name: {run_name}, entity: "
                f"{self.config.entity}."
            )
            wandb.init(
                project=self.config.project_name,
                name=run_name,
                entity=self.config.entity,
                settings=settings,
                tags=tags,
            )
            yield
        finally:
            wandb.finish()
