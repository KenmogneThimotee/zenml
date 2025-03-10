#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
from typing import cast

import click
from pipeline import (
    DeploymentTriggerParameters,
    SeldonDeploymentLoaderStepParameters,
    SklearnTrainerParameters,
    TensorflowTrainerParameters,
    continuous_deployment_pipeline,
    deployment_trigger,
    dynamic_importer,
    importer_mnist,
    inference_pipeline,
    normalizer,
    prediction_service_loader,
    predictor,
    sklearn_evaluator,
    sklearn_predict_preprocessor,
    sklearn_trainer,
    tf_evaluator,
    tf_predict_preprocessor,
    tf_trainer,
)
from rich import print

from zenml.integrations.seldon.model_deployers import SeldonModelDeployer
from zenml.integrations.seldon.seldon_client import SeldonResourceRequirements
from zenml.integrations.seldon.services import (
    SeldonDeploymentConfig,
    SeldonDeploymentService,
)
from zenml.integrations.seldon.steps import (
    SeldonDeployerStepParameters,
    seldon_model_deployer_step,
)

DEPLOY = "deploy"
PREDICT = "predict"
DEPLOY_AND_PREDICT = "deploy_and_predict"


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Choice([DEPLOY, PREDICT, DEPLOY_AND_PREDICT]),
    default="deploy_and_predict",
    help="Optionally you can choose to only run the deployment "
    "pipeline to train and deploy a model (`deploy`), or to "
    "only run a prediction against the deployed model "
    "(`predict`). By default both will be run "
    "(`deploy_and_predict`).",
)
@click.option(
    "--model-flavor",
    default="tensorflow",
    type=click.Choice(["tensorflow", "sklearn"]),
    help="Flavor of model being trained",
)
@click.option(
    "--epochs",
    default=5,
    help="Number of epochs for training (tensorflow hyperparam)",
)
@click.option(
    "--lr",
    default=0.003,
    help="Learning rate for training (tensorflow hyperparam, default: 0.003)",
)
@click.option(
    "--solver",
    default="saga",
    type=click.Choice(["newton-cg", "lbfgs", "liblinear", "sag", "saga"]),
    help="Algorithm to use in the optimization problem "
    "(sklearn hyperparam, default: saga)",
)
@click.option(
    "--penalty",
    default="l1",
    type=click.Choice(["l1", "l2", "elasticnet", "none"]),
    help="Regularization (penalty) norm (sklearn hyperparam, default: l1)",
)
@click.option(
    "--penalty-strength",
    default=1.0,
    type=float,
    help="Regularization (penalty) strength (sklearn hyperparam, default: 1.0)",
)
@click.option(
    "--toleration",
    default=0.1,
    type=float,
    help="Tolerance for stopping criteria (sklearn hyperparam, default: 0.1)",
)
@click.option(
    "--min-accuracy",
    default=0.92,
    help="Minimum accuracy required to deploy the model (default: 0.92)",
)
def main(
    config: str,
    model_flavor: str,
    epochs: int,
    lr: float,
    solver: str,
    penalty: str,
    penalty_strength: float,
    toleration: float,
    min_accuracy: float,
):
    """Run the Seldon example continuous deployment or inference pipeline.

    Example usage:

        python run.py --deploy --predict --model-flavor tensorflow \
             --min-accuracy 0.80

    """
    deploy = config == DEPLOY or config == DEPLOY_AND_PREDICT
    predict = config == PREDICT or config == DEPLOY_AND_PREDICT

    model_name = "mnist"
    deployment_pipeline_name = "continuous_deployment_pipeline"
    deployer_step_name = "model_deployer"

    model_deployer = SeldonModelDeployer.get_active_model_deployer()

    if model_flavor == "tensorflow":
        seldon_implementation = "TENSORFLOW_SERVER"
        trainer_params = TensorflowTrainerParameters(epochs=epochs, lr=lr)
        trainer = tf_trainer(trainer_params)
        evaluator = tf_evaluator()
        predict_preprocessor = tf_predict_preprocessor()
    else:
        seldon_implementation = "SKLEARN_SERVER"
        trainer_params = SklearnTrainerParameters(
            solver=solver,
            penalty=penalty,
            C=penalty_strength,
            tol=toleration,
        )
        trainer = sklearn_trainer(trainer_params)
        evaluator = sklearn_evaluator()
        predict_preprocessor = sklearn_predict_preprocessor()

    if deploy:
        # Initialize a continuous deployment pipeline run
        deployment = continuous_deployment_pipeline(
            importer=importer_mnist(),
            normalizer=normalizer(),
            trainer=trainer,
            evaluator=evaluator,
            deployment_trigger=deployment_trigger(
                params=DeploymentTriggerParameters(
                    min_accuracy=min_accuracy,
                )
            ),
            model_deployer=seldon_model_deployer_step(
                params=SeldonDeployerStepParameters(
                    service_config=SeldonDeploymentConfig(
                        model_name=model_name,
                        replicas=1,
                        implementation=seldon_implementation,
                        resources=SeldonResourceRequirements(
                            limits={"cpu": "200m", "memory": "250Mi"}
                        ),
                    ),
                    timeout=120,
                )
            ),
        )

        deployment.run()

    if predict:
        # Initialize an inference pipeline run
        inference = inference_pipeline(
            dynamic_importer=dynamic_importer(),
            predict_preprocessor=predict_preprocessor,
            prediction_service_loader=prediction_service_loader(
                SeldonDeploymentLoaderStepParameters(
                    pipeline_name=deployment_pipeline_name,
                    step_name=deployer_step_name,
                    model_name=model_name,
                )
            ),
            predictor=predictor(),
        )

        inference.run()

    services = model_deployer.find_model_server(
        pipeline_name=deployment_pipeline_name,
        pipeline_step_name=deployer_step_name,
        model_name=model_name,
    )
    if services:
        service = cast(SeldonDeploymentService, services[0])
        if service.is_running:
            print(
                f"The Seldon prediction server is running remotely as a Kubernetes "
                f"service and accepts inference requests at:\n"
                f"    {service.prediction_url}\n"
                f"To stop the service, run "
                f"[italic green]`zenml model-deployer models delete "
                f"{str(service.uuid)}`[/italic green]."
            )
        elif service.is_failed:
            print(
                f"The Seldon prediction server is in a failed state:\n"
                f" Last state: '{service.status.state.value}'\n"
                f" Last error: '{service.status.last_error}'"
            )

    else:
        print(
            "No Seldon prediction server is currently running. The deployment "
            "pipeline must run first to train a model and deploy it. Execute "
            "the same command with the `--deploy` argument to deploy a model."
        )


if __name__ == "__main__":
    main()
