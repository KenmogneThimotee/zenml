---
description: How to test the data and models used in your pipelines with Deepchecks test suites
---

The Deepchecks [Data Validator](./data-validators.md) flavor
provided with the ZenML integration uses [Deepchecks](https://deepchecks.com/)
to run data integrity, data drift, model drift and model performance tests
on the datasets and models circulated in your ZenML pipelines. The test results
can be used to implement automated corrective actions in your pipelines or to
render interactive representations for further visual interpretation, evaluation
and documentation.

## When would you want to use it?

[Deepchecks](https://deepchecks.com/) is an open-source library that you can use
to run a variety of data and model validation tests, from data integrity tests
that work with a single dataset to model evaluation tests to data drift analyses
and model performance comparison tests. All this can be done with minimal
configuration input from the user, or customized with specialized conditions
that the validation tests should perform.

Deepchecks works with both tabular data and computer vision data (currently in
beta). For tabular, the supported dataset format is `pandas.DataFrame` and
the supported model format is `sklearn.base.ClassifierMixin`. For computer
vision, the supported dataset format is `torch.utils.data.dataloader.DataLoader`
and supported model format is `torch.nn.Module`.

You should use the Deepchecks Data Validator when you need the following data
and/or model validation features that are possible with Deepchecks:

* Data Integrity Checks [for tabular](https://docs.deepchecks.com/en/stable/checks_gallery/tabular.html#data-integrity)
or [computer vision](https://docs.deepchecks.com/en/stable/checks_gallery/vision.html#data-integrity)
data: detect data integrity problems within a single dataset (e.g. missing
values, conflicting labels, mixed data types etc.).

* Data Drift Checks [for tabular](https://docs.deepchecks.com/en/stable/checks_gallery/tabular.html#train-test-validation)
or [computer vision](https://docs.deepchecks.com/en/stable/checks_gallery/vision.html#train-test-validation)
data: detect data skew and data drift problems by comparing a target dataset 
against a reference dataset (e.g. feature drift, label drift, new labels etc.).

* Model Performance Checks [for tabular](https://docs.deepchecks.com/en/stable/checks_gallery/tabular.html#model-evaluation)
or [computer vision](https://docs.deepchecks.com/en/stable/checks_gallery/vision.html#model-evaluation)
data: evaluate a model and detect problems with its performance (e.g. confusion 
matrix, boosting overfit, model error analysis)

You should consider one of the other [Data Validator flavors](./data-validators.md#data-validator-flavors)
if you need a different set of data validation features.

## How do you deploy it?

The Deepchecks Data Validator flavor is included in the Deepchecks ZenML
integration, you need to install it on your local machine to be able to register
a Deepchecks Data Validator and add it to your stack:

```shell
zenml integration install deepchecks -y
```

The Data Validator stack component does not have any configuration parameters.
Adding it to a stack is as simple as running e.g.:

```shell
# Register the Deepchecks data validator
zenml data-validator register deepchecks_data_validator --flavor=deepchecks

# Register and set a stack with the new data validator
zenml stack register custom_stack -dv deepchecks_data_validator ... --set
```

## How do you use it?

The ZenML integration restructures the way Deepchecks validation checks are
organized in four categories, based on the type and number of input parameters
that they expect as input. This makes it easier to reason about them when you
decide which tests to use in your pipeline steps:

* **data integrity checks** expect a single dataset as input. These correspond
one-to-one to the set of Deepchecks data integrity checks [for tabular](https://docs.deepchecks.com/en/stable/checks_gallery/tabular.html#data-integrity)
and [computer vision](https://docs.deepchecks.com/en/stable/checks_gallery/vision.html#data-integrity)
data

* **data drift checks** require two datasets as input: target and reference. 
These correspond one-to-one to the set of Deepchecks train-test checks 
[for tabular data](https://docs.deepchecks.com/stable/checks_gallery/tabular.html#train-test-validation) and [for computer vision](https://docs.deepchecks.com/stable/checks_gallery/vision.html#train-test-validation).

* **model validation checks** require a single dataset and a mandatory model as
input. This list includes a subset of the model evaluation checks provided by
Deepchecks [for tabular data](https://docs.deepchecks.com/en/stable/checks_gallery/tabular.html#model-evaluation)
and [for computer vision](https://docs.deepchecks.com/stable/checks_gallery/vision.html#model-evaluation)
that expect a single dataset as input.

* **model drift checks** require two datasets and a mandatory model as input.
This list includes a subset of the model evaluation checks provided by
Deepchecks [for tabular data](https://docs.deepchecks.com/en/stable/checks_gallery/tabular.html#model-evaluation)
and [for computer vision](https://docs.deepchecks.com/stable/checks_gallery/vision.html#model-evaluation)
that expect two datasets as input: target and reference.

This structure is directly reflected in how Deepchecks can be used with ZenML:
there are four different Deepchecks standard steps and four different [ZenML enums for Deepchecks checks](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.validation_checks).
[The Deepchecks Data Validator API](#the-deepchecks-data-validator) is also
modeled to reflect this same structure.

A notable characteristic of Deepchecks is that you don't need to customize the
set of Deepchecks tests that are part of a test suite. Both ZenML and Deepchecks
provide sane defaults that will run all available Deepchecks tests in a given
category with their default conditions if a custom list of tests and conditions
are not provided.

There are three ways you can use Deepchecks in your ZenML pipelines that allow
different levels of flexibility:

* instantiate, configure and insert one or more of [the standard Deepchecks steps](#the-deepchecks-standard-steps)
shipped with ZenML into your pipelines. This is the easiest way and the
recommended approach, but can only be customized through the supported step
configuration parameters.
* call the data validation methods provided by [the Deepchecks Data Validator](#the-deepchecks-data-validator)
in your custom step implementation. This method allows for more flexibility
concerning what can happen in the pipeline step, but you are still limited 
to the functionality implemented in the Data Validator.
* [use the Deepchecks library directly](#call-deepchecks-directly) in
your custom step implementation. This gives you complete freedom in how you are
using Deepchecks' features.

Outside of the pipeline workflow, you can use [the ZenML Deepchecks visualizer](#the-deepchecks-zenml-visualizer)
to display and interact with the Deepchecks test results generated by your
pipelines. 

## Warning! Usage in remote orchestrators

The current ZenML version has a limitation in its base Docker image that 
requires a workaround for *all* pipelines using Deepchecks with a remote 
orchestrator (e.g. [Kubeflow](../orchestrators/kubeflow.md), 
[Vertex](../orchestrators/vertex.md)). The limitation being that the 
base Docker image needs to be extended to include binaries that are required by 
`opencv2`, which is a package that Deepchecks requires.

While these binaries might be available on most operating systems out of the 
box (and therefore not a problem with the default local orchestrator), we need 
to tell ZenML to add them to the containerization step when running in remote 
settings. Here is how:

First, create a file called `deepchecks-zenml.Dockerfile` and place it on the 
same level as your runner script (commonly called `run.py`). The contents of 
the Dockerfile are as follows:

```shell
ARG ZENML_VERSION=0.20.0
FROM zenmldocker/zenml:${ZENML_VERSION} AS base

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
```

Then, place the following snippet above your pipeline definition. Note that 
the path of the `dockerfile`  are relative to where the pipeline definition 
file is. Read [the containerization guide](../../advanced-guide/pipelines/containerization.md) for more details:

```python
import zenml
from zenml.pipelines import pipeline
from zenml.config import DockerSettings
from pathlib import Path 
import sys 

docker_settings = DockerSettings(
    dockerfile="deepchecks-zenml.Dockerfile",
    build_options={
        "buildargs": {
            "ZENML_VERSION": f"{zenml.__version__}"
        },
    },
)

@pipeline(settings={"docker": docker_settings})
def my_pipeline(...):
    # same code as always
    ...
```

From here on, you can continue to use the deepchecks integration as is 
explained below.

### The Deepchecks standard steps

ZenML wraps the Deepchecks functionality for tabular data in the form of four
standard steps:

* [`DeepchecksDataIntegrityCheckStep`](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.steps.deepchecks_data_drift.DeepchecksDataDriftCheckStep):
use it in your pipelines to run data integrity tests on a single dataset
* [`DeepchecksDataDriftCheckStep`](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.steps.deepchecks_data_integrity.DeepchecksDataIntegrityCheckStep):
use it in your pipelines to run data drift tests on two datasets as input:
target and reference.
* [`DeepchecksModelValidationCheckStep`](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.steps.deepchecks_model_validation.DeepchecksModelValidationCheckStep):
class DeepchecksModelDriftCheckStep(BaseStep):
use it in your pipelines to run model performance tests using a single dataset
and a mandatory model artifact as input
* [`DeepchecksModelDriftCheckStep`](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.steps.deepchecks_model_drift.DeepchecksModelDriftCheckStep):
use it in your pipelines to run model comparison/drift tests using a mandatory
model artifact and two datasets as input: target and reference.

The integration doesn't yet include standard steps for computer vision, but you
can still write your own custom steps that call [the Deepchecks Data Validator API](#the-deepchecks-data-validator)
or even [call the Deepchecks library directly](#call-deepchecks-directly).

All four standard steps behave similarly regarding the configuration parameters
and returned artifacts, with the following differences:

* the type and number of input artifacts are different, as mentioned above
* each step expects a different enum data type to be used when explicitly
listing the checks to be performed via the `check_list` configuration attribute.
See the [`zenml.integrations.deepchecks.validation_checks`](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.validation_checks)
module for more details about these enums (e.g. the data integrity step expects
a list of `DeepchecksDataIntegrityCheck` values).

This section will only cover how you can use the data integrity step, with
a similar usage to be easily inferred for the other three steps. 

To instantiate a data integrity step that will run all available Deepchecks
data integrity tests with their default configuration, e.g.:

```python
from zenml.integrations.deepchecks.steps import (
    DeepchecksDataIntegrityCheckStepParameters,
    deepchecks_data_integrity_check_step,
)

data_validator = deepchecks_data_integrity_check_step(
    step_name="data_validator",
    params=DeepchecksDataIntegrityCheckStepParameters(),
)
```

The step can then be inserted into your pipeline where it can take in a
dataset, e.g.:

```python
@pipeline(required_integrations=[DEEPCHECKS, SKLEARN])
def data_validation_pipeline(
    data_loader,
    data_validator,
):
    df_train, df_test = data_loader()
    data_validator(dataset=df_train)

pipeline = data_validation_pipeline(
    data_loader=data_loader(),
    data_validator=data_validator,
)
pipeline.run()
```

As can be seen from the [step definition](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.steps.deepchecks_data_integrity.DeepchecksDataIntegrityCheckStepParameters),
the step takes in a dataset and it returns a Deepchecks `SuiteResult` object
that contains the test results:

```python
class DeepchecksDataIntegrityCheckStep(BaseStep):
    """Deepchecks data integrity validator step."""

    def entrypoint(  # type: ignore[override]
        self,
        dataset: pd.DataFrame,
        params: DeepchecksDataIntegrityCheckStepParameters,
    ) -> SuiteResult:
        ...
```

If needed, you can specify a custom list of data integrity Deepchecks tests to
be executed by supplying a `check_list` argument to the step configuration:

```python
from zenml.integrations.deepchecks.validation_checks import DeepchecksDataIntegrityCheck
from zenml.integrations.deepchecks.steps import (
    DeepchecksDataIntegrityCheckStepParameters,
    deepchecks_data_integrity_check_step,
)

data_validator = deepchecks_data_integrity_check_step(
    step_name="data_validator",
    params=DeepchecksDataIntegrityCheckStepParameters(
        check_list=[
            DeepchecksDataIntegrityCheck.TABULAR_MIXED_DATA_TYPES,
            DeepchecksDataIntegrityCheck.TABULAR_DATA_DUPLICATES,
            DeepchecksDataIntegrityCheck.TABULAR_CONFLICTING_LABELS,
        ],
    ),
)
```

You should consult [the official Deepchecks documentation](https://docs.deepchecks.com/en/stable/checks_gallery/tabular.html)
for more information on what each test is useful for.

For more customization, the `DeepchecksDataIntegrityCheckStepParams` step
configuration also allows for additional keyword arguments to be supplied to be
passed transparently to the Deepchecks library:

* `dataset_kwargs`: Additional keyword arguments to be passed to the Deepchecks
`tabular.Dataset` or `vision.VisionData` constructor. This is used to pass
additional information about how the data is structured, e.g.:

    ```python
    params=DeepchecksDataIntegrityCheckStepParameters(
        dataset_kwargs=dict(label='class', cat_features=['country', 'state']),
    ),
    ```

* `check_kwargs`: Additional keyword arguments to be passed to the Deepchecks
check object constructors. Arguments are grouped for each check and indexed
using the full check class name or check enum value as dictionary keys, e.g.:

    ```python
    params=DeepchecksDataIntegrityCheckStepParameters(
        check_list=[
            DeepchecksDataIntegrityCheck.TABULAR_OUTLIER_SAMPLE_DETECTION,
            DeepchecksDataIntegrityCheck.TABULAR_STRING_LENGTH_OUT_OF_BOUNDS,
            DeepchecksDataIntegrityCheck.TABULAR_STRING_MISMATCH,
        ],
        check_kwargs={
            DeepchecksDataIntegrityCheck.TABULAR_OUTLIER_SAMPLE_DETECTION: dict(
                nearest_neighbors_percent=0.01,
                extent_parameter=3,
            ),
            DeepchecksDataIntegrityCheck.TABULAR_STRING_LENGTH_OUT_OF_BOUNDS: dict(
                num_percentiles=1000,
                min_unique_values=3,
            ),
        },
    )
    ```

* `run_kwargs`: Additional keyword arguments to be passed to the Deepchecks
Suite `run` method.

The `check_kwargs` attribute can also be used to customize 
[the conditions](https://docs.deepchecks.com/en/stable/user-guide/general/deepchecks_hierarchy.html#condition)
configured for each Deepchecks test. ZenML attaches a special meaning to all
check arguments that start with `condition_` and have a dictionary as value.
This is required because there is no declarative way to specify conditions for
Deepchecks checks. For example, the following step configuration:

```python
params=DeepchecksDataIntegrityCheckStepParameters(
    check_list=[
        DeepchecksDataIntegrityCheck.TABULAR_OUTLIER_SAMPLE_DETECTION,
        DeepchecksDataIntegrityCheck.TABULAR_STRING_LENGTH_OUT_OF_BOUNDS,
    ],
    dataset_kwargs=dict(label='class', cat_features=['country', 'state']),
    check_kwargs={
        DeepchecksDataIntegrityCheck.TABULAR_OUTLIER_SAMPLE_DETECTION: dict(
            nearest_neighbors_percent=0.01,
            extent_parameter=3,
            condition_outlier_ratio_less_or_equal=dict(
                max_outliers_ratio=0.007,
                outlier_score_threshold= 0.5,
            ),
            condition_no_outliers=dict(
                outlier_score_threshold=0.6,
            )
        ),
        DeepchecksDataIntegrityCheck.TABULAR_STRING_LENGTH_OUT_OF_BOUNDS: dict(
            num_percentiles=1000,
            min_unique_values=3,
            condition_number_of_outliers_less_or_equal=dict(
                max_outliers=3,
            )
        ),
    },
)
```

is equivalent to running the following Deepchecks tests:

```python
import deepchecks.tabular.checks as tabular_checks
from deepchecks.tabular import Suite
from deepchecks.tabular import Dataset

train_dataset = Dataset(
    reference_dataset,
    label='class',
    cat_features=['country', 'state']
)

suite = Suite(name="custom")
check = tabular_checks.OutlierSampleDetection(
    nearest_neighbors_percent=0.01,
    extent_parameter=3,
)
check.add_condition_outlier_ratio_less_or_equal(
    max_outliers_ratio=0.007,
    outlier_score_threshold= 0.5,
)
check.add_condition_no_outliers(
    outlier_score_threshold=0.6,
)
suite.add(check)
check = tabular_checks.StringLengthOutOfBounds(
    num_percentiles=1000,
    min_unique_values=3,
)
check.add_condition_number_of_outliers_less_or_equal(
    max_outliers=3,
)
suite.run(train_dataset=train_dataset)
```

You can view [the complete list of configuration parameters](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.steps.deepchecks_data_integrity.DeepchecksDataIntegrityCheckStepParameters) in the API
docs.

You can also check out our examples pages for working examples that use the
Deepchecks standard steps:

- [Data and model validation with Deepchecks](https://github.com/zenml-io/zenml/tree/main/examples/deepchecks_data_validation)

### The Deepchecks Data Validator

The Deepchecks Data Validator implements the same interface as do all Data
Validators, so this method forces you to maintain some level of compatibility
with the overall Data Validator abstraction, which guarantees an easier
migration in case you decide to switch to another Data Validator.

All you have to do is call the Deepchecks Data Validator methods when you need
to interact with Deepchecks to run tests, e.g.:

```python

import pandas as pd
from deepchecks.core.suite import SuiteResult
from zenml.integrations.deepchecks.data_validators import DeepchecksDataValidator
from zenml.integrations.deepchecks.validation_checks import DeepchecksDataIntegrityCheck
from zenml.steps import step

@step
def data_integrity_check(
    dataset: pd.DataFrame,
) -> SuiteResult:
    """Custom data integrity check step with Deepchecks

    Args:
        dataset: input Pandas DataFrame

    Returns:
        Deepchecks test suite execution result
    """

    # validation pre-processing (e.g. dataset preparation) can take place here

    data_validator = DeepchecksDataValidator.get_active_data_validator()
    suite = data_validator.data_validation(
        dataset=dataset,
        check_list=[
            DeepchecksDataIntegrityCheck.TABULAR_OUTLIER_SAMPLE_DETECTION,
            DeepchecksDataIntegrityCheck.TABULAR_STRING_LENGTH_OUT_OF_BOUNDS,
        ],
    )

    # validation post-processing (e.g. interpret results, take actions) can happen here

    return suite
```

The arguments that the Deepchecks Data Validator methods can take in are the
same as those used for [the Deepchecks standard steps](#the-deepchecks-standard-steps).

Have a look at [the complete list of methods and parameters available in the `DeepchecksDataValidator` API](https://apidocs.zenml.io/latest/integration_code_docs/integrations-deepchecks/#zenml.integrations.deepchecks.data_validators.deepchecks_data_validator.DeepchecksDataValidator) in the API docs.

### Call Deepchecks directly

You can use the Deepchecks library directly in your custom pipeline steps, and
only leverage ZenML's capability of serializing, versioning and storing the
`SuiteResult` objects in its Artifact Store, e.g.:


```python
import pandas as pd
import deepchecks.tabular.checks as tabular_checks

from deepchecks.core.suite import SuiteResult
from deepchecks.tabular import Suite
from deepchecks.tabular import Dataset
from zenml.steps import step

@step
def data_integrity_check(
    dataset: pd.DataFrame,
) -> SuiteResult:
    """Custom data integrity check step with Deepchecks

    Args:
        dataset: a Pandas DataFrame

    Returns:
        Deepchecks test suite execution result
    """

    # validation pre-processing (e.g. dataset preparation) can take place here

    train_dataset = Dataset(
        dataset,
        label='class',
        cat_features=['country', 'state']
    )

    suite = Suite(name="custom")
    check = tabular_checks.OutlierSampleDetection(
        nearest_neighbors_percent=0.01,
        extent_parameter=3,
    )
    check.add_condition_outlier_ratio_less_or_equal(
        max_outliers_ratio=0.007,
        outlier_score_threshold= 0.5,
    )
    suite.add(check)
    check = tabular_checks.StringLengthOutOfBounds(
        num_percentiles=1000,
        min_unique_values=3,
    )
    check.add_condition_number_of_outliers_less_or_equal(
        max_outliers=3,
    )
    results = suite.run(train_dataset=train_dataset)

    # validation post-processing (e.g. interpret results, take actions) can happen here

    return results
```

### The Deepchecks ZenML Visualizer

In the [post-execution workflow](../../starter-guide/pipelines/fetching-pipelines.md),
you can load and render the Deepchecks test suite results generated and returned
by your pipeline steps by means of the ZenML Deepchecks Visualizer, e.g.:

```python
from zenml.integrations.deepchecks.visualizers import DeepchecksVisualizer
from zenml.post_execution import get_pipeline

def visualize_results(pipeline_name: str, step_name: str) -> None:
    pipeline = get_pipeline(pipeline=pipeline_name)
    last_run = pipeline.runs[0]
    step = last_run.get_step(step=step_name)
    DeepchecksVisualizer().visualize(step)

if __name__ == "__main__":
    visualize_results("data_validation_pipeline", "data_integrity_check")
```

The Deepchecks test suite results will be opened as tabs in your browser, or
displayed inline in your Jupyter notebook, depending on where you are running
the code:

![Deepchecks Visualization Example](../../assets/deepchecks/data-integrity-results.png)
