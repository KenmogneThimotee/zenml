#!/usr/bin/env bash

set -Eeo pipefail

setup_stack () {

  zenml model-deployer register mlflow_deployer --flavor=mlflow || \
    msg "${WARNING}Reusing preexisting model deployer ${NOFORMAT}mlflow_deployer"
  zenml experiment-tracker register mlflow_tracker  --flavor=mlflow || \
    msg "${WARNING}Reusing preexisting experiment tracker ${NOFORMAT}mlflow_tracker"
  zenml model-registry register mlflow_registry --flavor=mlflow || \
    msg "${WARNING}Reusing preexisting model registry ${NOFORMAT}mlflow_registry"
  zenml data-validator register evidently_validator --flavor=evidently || \
    msg "${WARNING}Reusing preexisting data validator ${NOFORMAT}evidently_validator"
  zenml stack register quickstart_stack \
      -a default \
      -o default \
      -dv evidently_validator \
      -d mlflow_deployer \
      -r mlflow_registry \
      -e mlflow_tracker || \
    msg "${WARNING}Reusing preexisting stack ${NOFORMAT}quickstart_stack"

  zenml stack set quickstart_stack
}

pre_run () {
  zenml integration install sklearn mlflow evidently
}

pre_run_forced () {
  zenml integration install sklearn mlflow evidently -y
}

post_run () {
  # cleanup the last local ZenML daemon started by the example
  pkill -n -f zenml.services.local.local_daemon_entrypoint
}
