<!-- markdown-link-check-disable -->

# 0.36.0

Our latest release adds hooks to ZenML pipelines to handle custom logic that
occurs on pipeline failure or success. This is a powerful feature that allows
you to easily receive custom alerts, for example, when a pipeline fails or
succeeds. (Check out our video showcasing the feature
[here](https://www.youtube.com/watch?v=KUW2G3EsqF8).)

The release is also packed with bug fixes and documentation updates. Some
smaller improvements include an increase of the `step_configurations` column
size in the database to accommodate really large configurations and the ability
to click through to orchestrator logs for the Sagemaker orchestrator directly
from the ZenML dashboard.

## Breaking Changes

Secrets are now handled internally by ZenML. This changes some behaviors that
you may have become used to with the (now-deprecated) Secrets Manager stack
component. The default behavior for the KServe and Seldon Core Model Deployer if
explicit credentials are not configured through the secret stack component
attribute has changed. Now, the model deployer will attempt to reuse credentials
configured for the Artifact Store in the same stack and may, in some cases, fail
if it cannot use them. In most cases, if credentials are not configured for the
active Artifact Store, the model deployer will assume some form of implicit
in-cloud authentication is configured for the Kubernetes cluster where KServe /
Seldon Core is installed and default to using that.

## What's Changed

* Add CLI utils tests by @strickvl in https://github.com/zenml-io/zenml/pull/1383
* Don't use docker client when building images remotely by @schustmi in https://github.com/zenml-io/zenml/pull/1394
* Fix zenml-quickstart-model typo by @safoinme in https://github.com/zenml-io/zenml/pull/1397
* Ignore starting quotes from Artifact store path by @safoinme in https://github.com/zenml-io/zenml/pull/1388
* CI speed improvements by @stefannica in https://github.com/zenml-io/zenml/pull/1384
* Fix stack recipe link by @strickvl in https://github.com/zenml-io/zenml/pull/1393
* Switch FastAPI response class to orjson so `NaN` values don't break the server by @fa9r in https://github.com/zenml-io/zenml/pull/1395
* Numpy materializer metadata for arrays with strings by @safoinme in https://github.com/zenml-io/zenml/pull/1392
* Fix last remaining runs index by @stefannica in https://github.com/zenml-io/zenml/pull/1399
* Add failure (and success hooks) by @htahir1 in https://github.com/zenml-io/zenml/pull/1361
* Replace `pyspelling` with `typos` by @strickvl in https://github.com/zenml-io/zenml/pull/1400
* Fix the download nltk param for report step by @wjayesh in https://github.com/zenml-io/zenml/pull/1409
* Add `build_timeout` attribute to `GCPImageBuilderConfig` by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/1408
* Bump `ruff` to v0.255 by @strickvl in https://github.com/zenml-io/zenml/pull/1403
* Update title of deployment docs page by @strickvl in https://github.com/zenml-io/zenml/pull/1412
* Changed to debug log by @htahir1 in https://github.com/zenml-io/zenml/pull/1406
* Fix incorrect `--sort_by` help text by @strickvl in https://github.com/zenml-io/zenml/pull/1413
* Document CLI filtering query language by @strickvl in https://github.com/zenml-io/zenml/pull/1414
* Fix GitHub pip download cache key by @stefannica in https://github.com/zenml-io/zenml/pull/1405
* Add orchestrator logs link for Sagemaker by @strickvl in https://github.com/zenml-io/zenml/pull/1375
* Phase out secrets managers from other stack components. by @stefannica in https://github.com/zenml-io/zenml/pull/1401
* Add MLflow UI message to quickstart example and fix autolog spillage by @stefannica in https://github.com/zenml-io/zenml/pull/1421
* Add tests for the model registry by @safoinme in https://github.com/zenml-io/zenml/pull/1415
* Remove Aspell installation by @strickvl in https://github.com/zenml-io/zenml/pull/1419
* Increase `step_configurations` column size to 2^24 by @strickvl in https://github.com/zenml-io/zenml/pull/1422
* Add help text for `enable_service` option in recipe sub-command by @safoinme in https://github.com/zenml-io/zenml/pull/1424


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.35.1...test

# 0.35.1

**Note:** *This release replaces the previous 0.35.0 release that was yanked from
PyPI due to a bug. If you already installed 0.35.0 and are experiencing issues,
we recommend you downgrade to 0.34.0 before installing and upgrading to 0.35.1.*

This release is packed with big features as well as documentation updates and
some bug fixes.

The 0.35.1 release puts models front and center in ZenML with the addition of
the **Model Registry** abstraction and Stack Component. You can now register,
version and manage models as first class citizens in ZenML. This is a major
milestone for ZenML and we are excited to see what you build with it!
The introduction of Model Registries greatly simplifies the journey that the
model takes from training to deployment and extends the ZenML ecosystem to
include model registry tools and libraries. The first Model Registry integration
included in this release is MLFlow, with many more to come in the future.

This release also continues the deprecation of Secrets Managers and the
introduction of Secret Stores. You now have the option of configuring the ZenML
server to use AWS, GCP, Azure or Hashicorp Vault directly as a centralized
secrets store back-end. This is meant to replace all Secrets Manager flavors
which were previously used to store secrets using the same cloud services.

Please be reminded that all Secrets Managers are now deprecated and will be
removed in the near future. We recommend that you migrate all your secrets from
the Secrets Manager stack components to the centralized secrets store by means
of the included `zenml secrets-manager secret migrate` CLI command.

Last but not least, this release includes an updated Evidently integration that
is compatible with the latest and greatest features from Evidently: reports and
test suites. Check out the updated example to get a feel for the new features.

## Breaking Changes

This release introduces a few breaking changes. Please update your code to
reflect the changes below:

* the order of pipelines and runs in the post-execution results has been
reversed. This means that the most recent pipeline and pipeline run can be
accessed using the first index of the respective lists instead of the last
index. This change was made to make the post-execution results more intuitive
and to allow returning multi-page results in the future. This is a code snippet
outlining the changes that you need to make in your post-execution code:

    ```python
    from zenml.post_execution import get_pipelines, get_unlisted_runs

    pipelines = get_pipelines()

    # instead of calling this to get the pipeline last created
    latest_pipeline = pipelines[-1]

    # you now have to call this
    latest_pipeline = pipelines[0]

    # and instead of calling this to get the latest run of a pipeline
    latest_pipeline_run = latest_pipeline.get_runs()[-1]
    # or
    latest_pipeline_run = latest_pipeline.runs[-1]
    
    # you now have to call this
    latest_pipeline_run = latest_pipeline.get_runs()[0]
    # or
    latest_pipeline_run = latest_pipeline.runs[0]

    # the same applies to the unlisted runs; instead of
    last_unlisted_run = get_unlisted_runs()[-1]

    # you now have to call this
    last_unlisted_run = get_unlisted_runs()[0]
    ```

* if you were using the `StepEnvironment` to fetch the name of the active step
in your step implementation, this name no longer reflects the name of the step
function. Instead, it now reflects the name of the step used in the pipeline
DAG, similar to what you would see in the ZenML dashboard when visualizing the
pipeline. This is also implicitly reflected in the output of `zenml model-deployer model`
CLI commands.

## What's Changed
* Upgrade dev dependencies by @strickvl in https://github.com/zenml-io/zenml/pull/1334
* Add warning when attempting server connection without user permissions by @strickvl in https://github.com/zenml-io/zenml/pull/1314
* Keep CLI help text for `zenml pipeline` to a single line by @strickvl in https://github.com/zenml-io/zenml/pull/1338
* Rename page attributes by @schustmi in https://github.com/zenml-io/zenml/pull/1266
* Add missing docs for pipeline build by @schustmi in https://github.com/zenml-io/zenml/pull/1341
* Sagemaker orchestrator docstring and example update by @strickvl in https://github.com/zenml-io/zenml/pull/1350
* Fix `secret create` docs error for secret store by @strickvl in https://github.com/zenml-io/zenml/pull/1355
* Update README for test environment provisioning by @strickvl in https://github.com/zenml-io/zenml/pull/1336
* Disable name prefix matching when updating/deleting entities by @schustmi in https://github.com/zenml-io/zenml/pull/1345
* Add Kubeflow Pipeline UI Port to deprecated config by @safoinme in https://github.com/zenml-io/zenml/pull/1358
* Small clarifications for slack alerter by @htahir1 in https://github.com/zenml-io/zenml/pull/1365
* update Neptune integration for v1.0 compatibility by @AleksanderWWW in https://github.com/zenml-io/zenml/pull/1335
* Integrations conditional requirements by @safoinme in https://github.com/zenml-io/zenml/pull/1255
* Fix fetching versioned pipelines in post execution by @schustmi in https://github.com/zenml-io/zenml/pull/1363
* Load artifact store before loading artifact to register filesystem by @schustmi in https://github.com/zenml-io/zenml/pull/1367
* Remove poetry from CI by @schustmi in https://github.com/zenml-io/zenml/pull/1346
* Fix Sagemaker example readme by @strickvl in https://github.com/zenml-io/zenml/pull/1370
* Update evidently to include reports and tests by @wjayesh in https://github.com/zenml-io/zenml/pull/1283
* Fix neptune linting error on `develop` (and bump ruff) by @strickvl in https://github.com/zenml-io/zenml/pull/1372
* Add pydantic materializer by @htahir1 in https://github.com/zenml-io/zenml/pull/1371
* Registering GIFs added by @htahir1 in https://github.com/zenml-io/zenml/pull/1368
* Refresh CLI cheat sheet by @strickvl in https://github.com/zenml-io/zenml/pull/1347
* Add dependency resolution docs by @strickvl in https://github.com/zenml-io/zenml/pull/1337
* [BUGFIX] Fix error while using an existing SQL server with GCP ZenServer by @wjayesh in https://github.com/zenml-io/zenml/pull/1353
* Update step name assignment with the parameter name by @strickvl in https://github.com/zenml-io/zenml/pull/1310
* Copy huggingface data directory to local before loading in materializers by @TimovNiedek in https://github.com/zenml-io/zenml/pull/1351
* Update huggingface token classification example by @strickvl in https://github.com/zenml-io/zenml/pull/1369
* Use the most specialized materializer based on MRO by @schustmi in https://github.com/zenml-io/zenml/pull/1376
* Update Kserve to support 0.10.0 by @safoinme in https://github.com/zenml-io/zenml/pull/1373
* Add more examples to integration tests by @schustmi in https://github.com/zenml-io/zenml/pull/1245
* Fix order of runs and order of pipelines in post-execution by @stefannica in https://github.com/zenml-io/zenml/pull/1380
* Add Cloud Secrets Store back-ends by @stefannica in https://github.com/zenml-io/zenml/pull/1348
* Model Registry Stack Component + MLFlow integration by @safoinme in https://github.com/zenml-io/zenml/pull/1309
* Fix broken docs URLs and add SDK docs url by @strickvl in https://github.com/zenml-io/zenml/pull/1349
* Fix label studio `dataset delete` command by @strickvl in https://github.com/zenml-io/zenml/pull/1377
* Add missing links to Quickstart by @strickvl in
  https://github.com/zenml-io/zenml/pull/1379
* Fix PyPI readme logo display by @strickvl in https://github.com/zenml-io/zenml/pull/1382
* Fixed broken migration for flavors by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1386
* Add debug mode flag for `zenml info` by @strickvl in https://github.com/zenml-io/zenml/pull/1374
* Update issue creation for bugs by @strickvl in https://github.com/zenml-io/zenml/pull/1387
* Integration sdk docs generated correctly now by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1389

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.34.0...0.35.0

# 0.35.0 (YANKED)

This release is packed with big features as well as documentation updates and
some bug fixes.

The 0.35.0 release puts models front and center in ZenML with the addition of
the **Model Registry** abstraction and Stack Component. You can now register,
version and manage models as first class citizens in ZenML. This is a major
milestone for ZenML and we are excited to see what you build with it!
The introduction of Model Registries greatly simplifies the journey that the
model takes from training to deployment and extends the ZenML ecosystem to
include model registry tools and libraries. The first Model Registry integration
included in this release is MLFlow, with many more to come in the future. 

This release also continues the deprecation of Secrets Managers and the
introduction of Secret Stores. You now have the option of configuring the ZenML
server to use AWS, GCP, Azure or Hashicorp Vault directly as a centralized
secrets store back-end. This is meant to replace all Secrets Manager flavors
which were previously used to store secrets using the same cloud services.

Please be reminded that all Secrets Managers are now deprecated and will be
removed in the near future. We recommend that you migrate all your secrets from
the Secrets Manager stack components to the centralized secrets store by means
of the included `zenml secrets-manager secret migrate` CLI command.

Last but not least, this release includes an updated Evidently integration that
is compatible with the latest and greatest features from Evidently: reports and
test suites. Check out the updated example to get a feel for the new features.

## Breaking Changes

This release introduces a few breaking changes. Please update your code to
reflect the changes below:

* the order of pipelines and runs in the post-execution results has been
reversed. This means that the most recent pipeline and pipeline run can be
accessed using the first index of the respective lists instead of the last
index. This change was made to make the post-execution results more intuitive
and to allow returning multi-page results in the future. This is a code snippet
outlining the changes that you need to make in your post-execution code:

    ```python
    from zenml.post_execution import get_pipelines, get_unlisted_runs

    pipelines = get_pipelines()

    # instead of calling this to get the pipeline last created
    latest_pipeline = pipelines[-1]

    # you now have to call this
    latest_pipeline = pipelines[0]

    # and instead of calling this to get the latest run of a pipeline
    latest_pipeline_run = latest_pipeline.get_runs()[-1]
    # or
    latest_pipeline_run = latest_pipeline.runs[-1]
    
    # you now have to call this
    latest_pipeline_run = latest_pipeline.get_runs()[0]
    # or
    latest_pipeline_run = latest_pipeline.runs[0]

    # the same applies to the unlisted runs; instead of
    last_unlisted_run = get_unlisted_runs()[-1]

    # you now have to call this
    last_unlisted_run = get_unlisted_runs()[0]
    ```

* if you were using the `StepEnvironment` to fetch the name of the active step
in your step implementation, this name no longer reflects the name of the step
function. Instead, it now reflects the name of the step used in the pipeline
DAG, similar to what you would see in the ZenML dashboard when visualizing the
pipeline. This is also implicitly reflected in the output of `zenml model-deployer model`
CLI commands.

## What's Changed
* Upgrade dev dependencies by @strickvl in https://github.com/zenml-io/zenml/pull/1334
* Add warning when attempting server connection without user permissions by @strickvl in https://github.com/zenml-io/zenml/pull/1314
* Keep CLI help text for `zenml pipeline` to a single line by @strickvl in https://github.com/zenml-io/zenml/pull/1338
* Rename page attributes by @schustmi in https://github.com/zenml-io/zenml/pull/1266
* Add missing docs for pipeline build by @schustmi in https://github.com/zenml-io/zenml/pull/1341
* Sagemaker orchestrator docstring and example update by @strickvl in https://github.com/zenml-io/zenml/pull/1350
* Fix `secret create` docs error for secret store by @strickvl in https://github.com/zenml-io/zenml/pull/1355
* Update README for test environment provisioning by @strickvl in https://github.com/zenml-io/zenml/pull/1336
* Disable name prefix matching when updating/deleting entities by @schustmi in https://github.com/zenml-io/zenml/pull/1345
* Add Kubeflow Pipeline UI Port to deprecated config by @safoinme in https://github.com/zenml-io/zenml/pull/1358
* Small clarifications for slack alerter by @htahir1 in https://github.com/zenml-io/zenml/pull/1365
* update Neptune integration for v1.0 compatibility by @AleksanderWWW in https://github.com/zenml-io/zenml/pull/1335
* Integrations conditional requirements by @safoinme in https://github.com/zenml-io/zenml/pull/1255
* Fix fetching versioned pipelines in post execution by @schustmi in https://github.com/zenml-io/zenml/pull/1363
* Load artifact store before loading artifact to register filesystem by @schustmi in https://github.com/zenml-io/zenml/pull/1367
* Remove poetry from CI by @schustmi in https://github.com/zenml-io/zenml/pull/1346
* Fix Sagemaker example readme by @strickvl in https://github.com/zenml-io/zenml/pull/1370
* Update evidently to include reports and tests by @wjayesh in https://github.com/zenml-io/zenml/pull/1283
* Fix neptune linting error on `develop` (and bump ruff) by @strickvl in https://github.com/zenml-io/zenml/pull/1372
* Add pydantic materializer by @htahir1 in https://github.com/zenml-io/zenml/pull/1371
* Registering GIFs added by @htahir1 in https://github.com/zenml-io/zenml/pull/1368
* Refresh CLI cheat sheet by @strickvl in https://github.com/zenml-io/zenml/pull/1347
* Add dependency resolution docs by @strickvl in https://github.com/zenml-io/zenml/pull/1337
* [BUGFIX] Fix error while using an existing SQL server with GCP ZenServer by @wjayesh in https://github.com/zenml-io/zenml/pull/1353
* Update step name assignment with the parameter name by @strickvl in https://github.com/zenml-io/zenml/pull/1310
* Copy huggingface data directory to local before loading in materializers by @TimovNiedek in https://github.com/zenml-io/zenml/pull/1351
* Update huggingface token classification example by @strickvl in https://github.com/zenml-io/zenml/pull/1369
* Use the most specialized materializer based on MRO by @schustmi in https://github.com/zenml-io/zenml/pull/1376
* Update Kserve to support 0.10.0 by @safoinme in https://github.com/zenml-io/zenml/pull/1373
* Add more examples to integration tests by @schustmi in https://github.com/zenml-io/zenml/pull/1245
* Fix order of runs and order of pipelines in post-execution by @stefannica in https://github.com/zenml-io/zenml/pull/1380
* Add Cloud Secrets Store back-ends by @stefannica in https://github.com/zenml-io/zenml/pull/1348
* Model Registry Stack Component + MLFlow integration by @safoinme in https://github.com/zenml-io/zenml/pull/1309
* Fix broken docs URLs and add SDK docs url by @strickvl in https://github.com/zenml-io/zenml/pull/1349
* Fix label studio `dataset delete` command by @strickvl in https://github.com/zenml-io/zenml/pull/1377
* Add missing links to Quickstart by @strickvl in https://github.com/zenml-io/zenml/pull/1379

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.34.0...0.35.0

# 0.34.0

This release comes with major upgrades to the python library as well as the dashboard:
- You can now store you secrets in a centralized way instead of having them
tied to a secrets manager stack component. The secrets manager component is deprecated but will still
work while we continue migrating all secrets manager flavors to be available as a backend to store centralized
secrets. Check out [the docs](https://docs.zenml.io/advanced-guide/practical-mlops/secrets-management)
for more information.
- Pipelines are now versioned: ZenML detects changes to your steps and structure of your pipelines and
automatically creates new pipeline versions for you.
- You can now build the required Docker images for your pipeline without actually running it with
the `zenml pipeline build` command. This build can later be used to run the pipeline using the
`zenml pipeline run` command or by passing it to `pipeline.run()` in python.
- Metadata for runs and artifacts is now displayed in the dashboard: When viewing a pipeline run in the dashboard,
click on a step or artifact to get useful metadata like the endpoint where your model is deployed or
statistics about your training data.


## What's Changed
* Move inbuilt Flavors into the Database by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1187
* Bump `ruff` version to 241 by @strickvl in https://github.com/zenml-io/zenml/pull/1289
* Add docs for run name templates by @schustmi in https://github.com/zenml-io/zenml/pull/1290
* Remove excess help text for `zenml connect` command by @strickvl in https://github.com/zenml-io/zenml/pull/1291
* Increase default service timeout to 60 by @safoinme in https://github.com/zenml-io/zenml/pull/1294
* increase timeout on quickstart example by @safoinme in https://github.com/zenml-io/zenml/pull/1296
* Add warning about MacOS not being supported by @strickvl in https://github.com/zenml-io/zenml/pull/1303
* Always include .zen in docker builds by @schustmi in https://github.com/zenml-io/zenml/pull/1292
* Add warning and docs update for `label_studio` installation issue by @strickvl in https://github.com/zenml-io/zenml/pull/1299
* Loosen version requirements for Great Expectations integration by @strickvl in https://github.com/zenml-io/zenml/pull/1302
* Change zenml init --template to optionally prompt and track email by @stefannica in https://github.com/zenml-io/zenml/pull/1298
* Update docs for Neptune experiment tracker integration by @strickvl in https://github.com/zenml-io/zenml/pull/1307
* Fix the destroy function on the stack recipe CLI by @wjayesh in https://github.com/zenml-io/zenml/pull/1301
* Add missing flavor migrations, make workspace ID optional by @schustmi in https://github.com/zenml-io/zenml/pull/1315
* Bump ruff 246 by @strickvl in https://github.com/zenml-io/zenml/pull/1316
* Remove tag from image name in gcp image builder by @schustmi in https://github.com/zenml-io/zenml/pull/1317
* Fix docs typo by @strickvl in https://github.com/zenml-io/zenml/pull/1318
* Fix step parameter merging by @schustmi in https://github.com/zenml-io/zenml/pull/1320
* Increase timeout for mlflow deployment example by @strickvl in https://github.com/zenml-io/zenml/pull/1308
* Workspace/projects fix for dashboard URL output when running pipeline by @strickvl in https://github.com/zenml-io/zenml/pull/1322
* Component Metadata Tracking Docs by @fa9r in https://github.com/zenml-io/zenml/pull/1319
* Add user environment `zenml info` command to CLI for debugging by @strickvl in https://github.com/zenml-io/zenml/pull/1312
* Added caching to quickstart by @htahir1 in https://github.com/zenml-io/zenml/pull/1321
* Renovation of the zenstore tests by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1275
* Fixes GCP docs typo by @luckri13 in https://github.com/zenml-io/zenml/pull/1327
* Remove deprecated CLI options by @strickvl in https://github.com/zenml-io/zenml/pull/1325
* GCP Image Builder network  by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/1323
* improved flavor docs by @htahir1 in https://github.com/zenml-io/zenml/pull/1324
* Commands to register, build and run pipelines from the CLI by @schustmi in https://github.com/zenml-io/zenml/pull/1293
* Validate kserve model name by @strickvl in https://github.com/zenml-io/zenml/pull/1304
* Fix post-execution run sorting by @schustmi in https://github.com/zenml-io/zenml/pull/1332
* Secrets store with SQL back-end by @stefannica in https://github.com/zenml-io/zenml/pull/1313

## New Contributors
* @luckri13 made their first contribution in https://github.com/zenml-io/zenml/pull/1327

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.33.0...0.34.0

# 0.33.0

This release introduces several big new features:
- Docker images can now be built in GCP using the new 
[Google Cloud Image Builder](https://docs.zenml.io/component-gallery/image-builders/gcloud-build)
integration. Special shoutout to @gabrielmbmb for this amazing contribution!
- Getting started with ZenML has been made even easier. You can now use one of
the new [ZenML Project Templates](https://github.com/zenml-io/zenml-project-templates)
to initialize your ZenML repository with a basic project structure including a
functional pipeline and basic scaffolding for materializers, parameters, and
other classes you might want to extend.
- Orchestrating runs on local Kubernetes has been made easier: The KubeFlow, 
Kubernetes, and Tekton orchestrators have been redesigned to be compatible with 
the [K3D modular stack recipe](https://github.com/zenml-io/mlops-stacks/tree/main/k3d-modular)
that lets you spin up a local K3D Kubernetes cluster with a single line of code!
- The MLflow integration has been updated and can now be used with the new 
MLflow 2.x!
- You can now specify parameters and resources for your Seldon model deployers
thanks to @d-lowl!

Furthermore, the internal `project` concept has been renamed to `workspace` to
avoid confusion with the [zenml-projects](https://github.com/zenml-io/zenml-projects) 
repository. This should only be relevant to you if you have custom applications
that are interacting with the REST API of the ZenML server directly since all 
models sent from/to the server need to contain a `workspace` instead of a 
`project` now.

## What's Changed
* Renaming Project to Workspace by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1254
* Integration tests for post execution functions by @fa9r in https://github.com/zenml-io/zenml/pull/1264
* Introduce `post_execution.BaseView` by @fa9r in https://github.com/zenml-io/zenml/pull/1238
* Make `/cloud` point to enterprise page by @strickvl in https://github.com/zenml-io/zenml/pull/1268
* update mlflow to version greater than 2.0 by @safoinme in https://github.com/zenml-io/zenml/pull/1249
* Store run start time by @schustmi in https://github.com/zenml-io/zenml/pull/1271
* Relax pydantic dependency by @jlopezpena in https://github.com/zenml-io/zenml/pull/1262
* Fix failing filter on stacks by component id by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1276
* Track server version by @schustmi in https://github.com/zenml-io/zenml/pull/1265
* Bump ruff, drop `autoflake`, add `darglint` back by @strickvl in https://github.com/zenml-io/zenml/pull/1279
* Fixed startswith and endswith by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1278
* Fix workspace scoping on `list_workspace_... endpoints` again by @fa9r in https://github.com/zenml-io/zenml/pull/1284
* Custom Metadata Tracking by @fa9r in https://github.com/zenml-io/zenml/pull/1151
* Bug: local ZenML server ignores ip-address CLI argument by @stefannica in https://github.com/zenml-io/zenml/pull/1282
* Configure the zenml-server docker image and helm chart to run as non-privileged user by @stefannica in https://github.com/zenml-io/zenml/pull/1273
* GCP Image Builder by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/1270
* Disentangle K3D code from ZenML by @safoinme in https://github.com/zenml-io/zenml/pull/1185
* Rework params / artifact docs by @strickvl in https://github.com/zenml-io/zenml/pull/1277
* Always add active user to analytics by @stefannica in https://github.com/zenml-io/zenml/pull/1286
* Fix step and pipeline run metadata in LineageGraph by @fa9r in https://github.com/zenml-io/zenml/pull/1288
* add validator to endpoint url to replace hostname with k3d or docker … by @safoinme in https://github.com/zenml-io/zenml/pull/1189
* Add option to use project templates to initialize a repository by @stefannica in https://github.com/zenml-io/zenml/pull/1287
* Add example for Hyperparameter Tuning with ZenML by @nitay93 in https://github.com/zenml-io/zenml/pull/1206
* Add seldon deployment predictor parameters and resource requirements by @d-lowl in https://github.com/zenml-io/zenml/pull/1280

## New Contributors
* @jlopezpena made their first contribution in https://github.com/zenml-io/zenml/pull/1262
* @nitay93 made their first contribution in https://github.com/zenml-io/zenml/pull/1206
* @d-lowl made their first contribution in https://github.com/zenml-io/zenml/pull/1280

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.32.1...0.33.0

# 0.32.1

This release resolves several minor bugs and inconveniences introduced during 
the filtering and pagination overhaul in the last release. Additionally, the 
release includes new integration tests to improve future stability.

## What's Changed
* Update and improve docker and helm deployment docs by @stefannica in https://github.com/zenml-io/zenml/pull/1246
* Fixed broken link returned form pipeline runs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1257
* Fix project scoping on `list_project_...` endpoints by @fa9r in https://github.com/zenml-io/zenml/pull/1256
* Orchestrator tests by @schustmi in https://github.com/zenml-io/zenml/pull/1258
* Add integration tests for lineage graph creation by @fa9r in https://github.com/zenml-io/zenml/pull/1253
* Always instantiate a zen_store before startup. by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1261
* Fix post execution run fetching by @schustmi in https://github.com/zenml-io/zenml/pull/1263
* Implemented the option to choose between ascending and descending on list calls by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1260
* Fix logger warning message by @strickvl in https://github.com/zenml-io/zenml/pull/1267

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.32.0...0.32.1

# 0.32.0

Release 0.32.0 introduces two big new features:
* A new stack component, the "image builder", with a corresponding new Kaniko
integration.
* Logic for filtering and pagination of list requests.

## Image Builder Abstraction and Kaniko Integration
ZenML stacks can now contain an image builder as additional optional stack 
component. The image builder defines how the Docker images are built that are
required by many of the other stack components such as Airflow or Kubeflow.
Previously, all image building was handled implicitly by ZenML using local
Docker, which has now been refactored into the "local" image builder flavor.
As an alternative, you can now install the new "kaniko" integration to build
your images in Kubernetes using Kaniko.

## Filtering and Pagination
All list commands in ZenML are now capable of advanced filtering such as
`zenml stack list --created="gt:22-12-04 17:00:00" --name contains:def`.

Additionally, list commands now return pages of results, which significantly
improves performance for power ZenML users that have already created many runs
or other entities.

## What's Changed
* UserResponseModel contains roles, block recursion properly on more Models, reduce amount of Runs on a PipelineResponseModel by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1180
* Bump ruff version by @strickvl in https://github.com/zenml-io/zenml/pull/1232
* Zenfile becomes project by @strickvl in https://github.com/zenml-io/zenml/pull/1235
* Fix class resolution in notebooks under Python>=3.10 by @fa9r in https://github.com/zenml-io/zenml/pull/1234
* Fix Sagemaker README images & pipeline addition by @strickvl in https://github.com/zenml-io/zenml/pull/1239
* Step/Pipeline configuration tests by @schustmi in https://github.com/zenml-io/zenml/pull/1233
* Removed gRPC from diagrams by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1242
* Fix MLflow tracking example bug for Macs by @strickvl in https://github.com/zenml-io/zenml/pull/1237
* Fix copy function to copyfile in registered filesystem by @safoinme in https://github.com/zenml-io/zenml/pull/1243
* Image builder abstraction by @schustmi in https://github.com/zenml-io/zenml/pull/1198
* Add support for modular recipes to the recipe CLI by @wjayesh in https://github.com/zenml-io/zenml/pull/1247
* Add docs on upgrading and troubleshooting zenml server by @wjayesh in https://github.com/zenml-io/zenml/pull/1244
* Improve Seldon and Kserve Docs by @wjayesh in https://github.com/zenml-io/zenml/pull/1236
* Add Pagination to all List commands by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1113

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.31.1...0.32.0

# 0.31.1

This release includes several bug fixes and new additions under the hood such as 
testing for various internal utility functions. This should help keep ZenML more 
stable over time. Additionally, we added the ability to customize default 
materializers for custom artifact stores, and the ability to track system info 
and the Python version of pipeline runs (both where pipelines are initially 
executed as well as wherever they eventually run). We added better support for 
pipeline scheduling (particularly from within the CLI) and tracking of the 
source code of steps. The release also includes the addition of information 
about whether the pipeline is running on a stack created by the active user, and
the ability to specify Kubernetes container resource requests and limits. 
Finally, we addressed issues with caching such that caching is enabled for steps
that have explicit enable_cache=True specified (even when pipelines have it 
turned off).


## What's Changed
* Test for `enum_utils` by @strickvl in https://github.com/zenml-io/zenml/pull/1209
* Add missing space in Azure docs by @strickvl in https://github.com/zenml-io/zenml/pull/1218
* Test for `dashboard_utils` by @strickvl in https://github.com/zenml-io/zenml/pull/1202
* Cloud version gets love by @htahir1 in https://github.com/zenml-io/zenml/pull/1219
* ZenFiles to ZenML Projects by @htahir1 in https://github.com/zenml-io/zenml/pull/1220
* Track System Info and Python Version of Pipeline Runs by @fa9r in https://github.com/zenml-io/zenml/pull/1215
* Tests for `pydantic_utils` by @strickvl in https://github.com/zenml-io/zenml/pull/1207
* Customizing Default Materializers for Custom Artifact Stores by @safoinme in https://github.com/zenml-io/zenml/pull/1224
* Test `typed_model` utilities by @strickvl in https://github.com/zenml-io/zenml/pull/1208
* Enable Airflow<2.4 by @schustmi in https://github.com/zenml-io/zenml/pull/1222
* Fix `alembic_start` migration if tables exist by @fa9r in https://github.com/zenml-io/zenml/pull/1214
* Tests for `network_utils` by @strickvl in https://github.com/zenml-io/zenml/pull/1201
* Tests for `io_utils` and removal of duplicate code by @strickvl in https://github.com/zenml-io/zenml/pull/1199
* Use `ruff` to replace our linting suite by @strickvl in https://github.com/zenml-io/zenml/pull/1211
* Test `materializer` utilities by @safoinme in https://github.com/zenml-io/zenml/pull/1221
* Add information whether pipeline is running on a stack created by the active user by @schustmi in https://github.com/zenml-io/zenml/pull/1229
* Test `daemon` util functions by @strickvl in https://github.com/zenml-io/zenml/pull/1210
* Test `filesync_model` utils by @strickvl in https://github.com/zenml-io/zenml/pull/1230
* Track Source Code of Steps by @fa9r in https://github.com/zenml-io/zenml/pull/1216
* Track Pipeline Run Schedules by @fa9r in https://github.com/zenml-io/zenml/pull/1227
* Tests for analytics by @bcdurak in https://github.com/zenml-io/zenml/pull/1228
* Allow specifying Kubernetes container resource requests and limits by @schustmi in https://github.com/zenml-io/zenml/pull/1223
* Enable cache for all steps that have explicit `enable_cache=True` by @fa9r in https://github.com/zenml-io/zenml/pull/1217
* Make shared stacks visible again by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1225


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.31.0...0.31.1


# 0.31.0

The highlights of this release are:

* our Materializers have been redesigned to be more flexible and easier to use
* we have added a new integration test framework
* the SageMaker orchestrator has been added to our list of supported orchestrators
* pipeline runs and artifacts can now be deleted from the ZenML database via the CLI
or the Client API
* some integrations have been updated to a more recent version: Kubeflow, Seldon
Core and Tekton

This release also includes a few bug fixes and other minor improvements to
existing features.

## What's Changed
* Fix installation instructions in readme and docs by @schustmi in https://github.com/zenml-io/zenml/pull/1167
* Fix broken TOC for scheduling docs by @strickvl in https://github.com/zenml-io/zenml/pull/1169
* Ensure model string fields have a max length by @strickvl in https://github.com/zenml-io/zenml/pull/1136
* Integration test framework by @stefannica in https://github.com/zenml-io/zenml/pull/1099
* Check if all ZenML server dependencies are installed for local zenml deployment using `zenml up` by @dnth in https://github.com/zenml-io/zenml/pull/1144
* Persist the server ID in the database by @stefannica in https://github.com/zenml-io/zenml/pull/1173
* Tiny docs improvements by @strickvl in https://github.com/zenml-io/zenml/pull/1179
* Changing some interactions with analytics fields by @bcdurak in https://github.com/zenml-io/zenml/pull/1174
* Fix `PyTorchDataLoaderMaterializer` for older torch versions by @fa9r in https://github.com/zenml-io/zenml/pull/1178
* Redesign Materializers by @fa9r in https://github.com/zenml-io/zenml/pull/1154
* Fixing the error messages when fetching entities by @bcdurak in https://github.com/zenml-io/zenml/pull/1171
* Moved the active_user property onto the client, implemented get_myself as zenstore method by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1161
* Bugfix/bump evidently version by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1183
* Alembic migration to update size of flavor config schema by @fa9r in https://github.com/zenml-io/zenml/pull/1181
* Deleting pipeline runs and artifacts by @fa9r in https://github.com/zenml-io/zenml/pull/1164
* Signer email checked before setting in google cloud scheduler by @htahir1 in https://github.com/zenml-io/zenml/pull/1184
* Fix zenml helm chart to not leak analytics events by @stefannica in https://github.com/zenml-io/zenml/pull/1190
* Tests for `dict_utils` by @strickvl in https://github.com/zenml-io/zenml/pull/1196
* Adding exception tracking to `zeml init` by @bcdurak in https://github.com/zenml-io/zenml/pull/1192
* Prevent crashes during Airflow server forking on MacOS by @schustmi in https://github.com/zenml-io/zenml/pull/1186
* add alpha as server deployment type by @wjayesh in https://github.com/zenml-io/zenml/pull/1197
* Bugfix for custom flavor registration by @bcdurak in https://github.com/zenml-io/zenml/pull/1195
* Tests for `uuid_utils` by @strickvl in https://github.com/zenml-io/zenml/pull/1200
* Sagemaker orchestrator integration by @strickvl in https://github.com/zenml-io/zenml/pull/1177
* Fix Pandas Materializer Index by @safoinme in https://github.com/zenml-io/zenml/pull/1193
* Add support for deploying custom stack recipes using the ZenML CLI by @wjayesh in https://github.com/zenml-io/zenml/pull/1188
* Add cloud CI environments by @stefannica in https://github.com/zenml-io/zenml/pull/1176
* Fix project scoping for artifact list through ZenServer by @fa9r in https://github.com/zenml-io/zenml/pull/1203


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.30.0...0.31.0

# 0.30.0

In this release, ZenML finally adds Mac M1 support, Python 3.10 support and much
greater flexibility and configurability under the hood by deprecating some 
large dependencies like `ml-pipelines-sdk`.

## Scheduling

Based on some community feedback around scheduling, this release comes with
improved docs concerning scheduling in general. Additionally, the Vertex AI
orchestrator now also supports scheduling.

## Slimmer Dependencies

By removing dependencies on some of the packages that ZenML was built on, this 
version of ZenML is slimmer, faster and more configurable than ever. This also
finally makes ZenML run natively on Macs with M1 processors without the need for
Rosetta. This also finally enables ZenML to run on Python 3.10.

## Breaking Changes

* The removal of `ml-pipelines-sdk` and `tfx` leads to some larger changes in 
the database that is tracking your pipeline runs and artifacts. **Note**: There
is an automatic migration to upgrade this automatically, However, please note
that downgrading back down to 0.23.0 is not supported.
* The CLI commands to export and import pipeline runs have been deprecated. 
Namely: `zenml pipeline runs export` and `zenml pipeline runs import`
These commands were meant for migrating from `zenml<0.20.0` to 
`0.20.0<=zenml<0.30.0`. 
* The `azure-ml` integration dependency on `azureml-core` has been upgraded 
from `1.42` to `1.48`


## What's Changed
* Remove stack extra from installation, enable re-running the quickstart by @schustmi in https://github.com/zenml-io/zenml/pull/1133
* Secrets manager support to experiment trackers docs  by @safoinme in https://github.com/zenml-io/zenml/pull/1137
* Updating the README files of our examples by @bcdurak in https://github.com/zenml-io/zenml/pull/1128
* Prevent running with local ZenStore and remote code execution by @schustmi in https://github.com/zenml-io/zenml/pull/1134
* Remove `ml-pipelines-sdk` dependency by @schustmi in https://github.com/zenml-io/zenml/pull/1103
* Fix Huggingface dataset materializer by @safoinme in https://github.com/zenml-io/zenml/pull/1142
* Disallow alembic downgrades for 0.30.0 release by @fa9r in https://github.com/zenml-io/zenml/pull/1140
* Fix Client flavor-related methods by @schustmi in https://github.com/zenml-io/zenml/pull/1153
* Replace User Password with Token in docker images by @safoinme in https://github.com/zenml-io/zenml/pull/1147
* Remove zenml pipeline runs export / import CLI commands by @fa9r in https://github.com/zenml-io/zenml/pull/1150
* Context manager to track events by @bcdurak in https://github.com/zenml-io/zenml/pull/1149
* Made explicit `is not None` calls to allow for empty pwd again by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1159
* Add Neptune exp tracker into flavors table by @dnth in https://github.com/zenml-io/zenml/pull/1156
* Fix step operators by @schustmi in https://github.com/zenml-io/zenml/pull/1155
* Display correct name when updating a stack component by @schustmi in https://github.com/zenml-io/zenml/pull/1160
* Update mysql database creation by @schustmi in https://github.com/zenml-io/zenml/pull/1152
* Adding component conditions to experiment tracker examples and adding to the environmental variable docs by @bcdurak in https://github.com/zenml-io/zenml/pull/1162
* Increase dependency range for protobuf by @schustmi in https://github.com/zenml-io/zenml/pull/1163
* Scheduling documentation by @strickvl in https://github.com/zenml-io/zenml/pull/1158
* Adding scheduling for Vertex Pipelines by @htahir1 in https://github.com/zenml-io/zenml/pull/1148
* Fix alembic migration for sqlite<3.25 by @fa9r in https://github.com/zenml-io/zenml/pull/1165
* Fix pandas Series materializer by @jordandelbar in https://github.com/zenml-io/zenml/pull/1146

## New Contributors
* @jordandelbar made their first contribution in https://github.com/zenml-io/zenml/pull/1146

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.23.0...0.30.0

# 0.23.0

This release comes with a brand-new Neptune integration to track your ML experiments
as well as lots of performance improvements!

## Neptune integration

The new [Neptune integration](https://github.com/zenml-io/zenml/tree/main/examples/neptune_tracking)
includes a Neptune experiment tracker component that allows you to track your machine learning experiments
using Neptune.

## Performance Optimization

The 0.20.0 release introduced our new server but brought with it a few performance and scalability issues.
Since then, we've made many improvements to it, and this release is the final and biggest boost in performance. We reduced the amount of server calls needed for almost all CLI commands and greatly improved the speed of the dashboard as well.

## PyArrow dependency removal

We've removed PyArrow as a dependency of the `zenml` python package.
As a consequence of that, our NumPy and Pandas materializer no
longer read and write their artifacts using PyArrow but instead use
native formats instead. If you still want to use PyArrow to serialize
your NumPy arrays and Pandas dataframes, you'll need to install it manually
like this: `pip install pyarrow`

In future releases we'll get rid of other unnecessary dependencies to
further slim down the `zenml` package.

## Breaking Changes

The following changes introduces with this release mey require some manual
intervention to update your current installations:

- If your code calls some methods of our `Client` class, it might need to be
updated to the new model classes introduced by the performance optimization changes
explained above
- The CLI command to remove an attribute from a stack component now takes no more dashes
in front of the attribute names:
`zenml stack-component remove-attribute <COMPONENT_NAME> <ATTRIBUTE_NAME>`
- If you're using a custom stack component and have overridden the `cleanup_step_run` method,
you'll need to update the method signature to include a `step_failed` parameter.

## What's Changed
* Docs regarding roles and permissions by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1081
* Add global config dir to `zenml status` by @schustmi in https://github.com/zenml-io/zenml/pull/1084
* Remove  source pins and ignore source pins during step spec comparisons by @schustmi in https://github.com/zenml-io/zenml/pull/1083
* Docs/links for roles permissions by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1091
* Bugfix/eng 1485 fix api docs build by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1089
* fix bento builder step parameters to match bentoml by @safoinme in https://github.com/zenml-io/zenml/pull/1096
* Add bentoctl to BentoML docs and example by @safoinme in https://github.com/zenml-io/zenml/pull/1094
* Fix BaseParameters sample code in docs by @jcarlosgarcia in https://github.com/zenml-io/zenml/pull/1098
* zenml <stack-component> logs defaults to active stack without name_or_id by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1101
* Fixed evidently docs by @htahir1 in https://github.com/zenml-io/zenml/pull/1111
* Update sagemaker default instance type by @schustmi in https://github.com/zenml-io/zenml/pull/1112
* The ultimate optimization for performance by @bcdurak in https://github.com/zenml-io/zenml/pull/1077
* Update stack exporting and importing by @schustmi in https://github.com/zenml-io/zenml/pull/1114
* Fix readme by @schustmi in https://github.com/zenml-io/zenml/pull/1116
* Remove Pyarrow dependency by @safoinme in https://github.com/zenml-io/zenml/pull/1109
* Bugfix for listing the runs filtered by a name by @bcdurak in https://github.com/zenml-io/zenml/pull/1118
* Neptune.ai integration by @AleksanderWWW in https://github.com/zenml-io/zenml/pull/1082
* Add YouTube video explaining Stack Components Settings vs Config by @dnth in https://github.com/zenml-io/zenml/pull/1120
* Add failed Status to component when step fails by @safoinme in https://github.com/zenml-io/zenml/pull/1115
* Add architecture diagrams to docs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1119
* Remove local orchestrator restriction from step operator docs by @schustmi in https://github.com/zenml-io/zenml/pull/1122
* Validate Stack Before Provision by @safoinme in https://github.com/zenml-io/zenml/pull/1110
* Bugfix/fix endpoints for dashboard development by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1125
* Skip kubeflow UI daemon provisioning if a hostname is configured by @schustmi in https://github.com/zenml-io/zenml/pull/1126
* Update Neptune Example by @safoinme in https://github.com/zenml-io/zenml/pull/1124
* Add debugging guide to docs by @dnth in https://github.com/zenml-io/zenml/pull/1097
* Fix stack component attribute removal CLI command by @schustmi in https://github.com/zenml-io/zenml/pull/1127
* Improving error messages when fetching entities by @bcdurak in https://github.com/zenml-io/zenml/pull/1117
* Introduce username and password to kubeflow for more native multi-tenant support by @htahir1 in https://github.com/zenml-io/zenml/pull/1123
* Add support for Label Studio OCR config generation by @shivalikasingh95 in https://github.com/zenml-io/zenml/pull/1062
* Misc doc updates by @schustmi in https://github.com/zenml-io/zenml/pull/1131
* Fix Neptune run cleanup by @safoinme in https://github.com/zenml-io/zenml/pull/1130

## New Contributors
* @jcarlosgarcia made their first contribution in https://github.com/zenml-io/zenml/pull/1098
* @AleksanderWWW made their first contribution in https://github.com/zenml-io/zenml/pull/1082
* @shivalikasingh95 made their first contribution in https://github.com/zenml-io/zenml/pull/1062

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.22.0...0.23.0

# 0.22.0

The 0.22.0 release comes with a new BentoML integration as well as a reworked
Airflow orchestrator. Additionally, it greatly improves the server performance
as well as other small fixes and updates to our docs!

## BentoML integration

The new [BentoML integration](https://github.com/zenml-io/zenml/tree/main/examples/bentoml_deployment)
includes a BentoML model deployer component that allows you to deploy
your models from any of the major machine learning frameworks on your local machine.
## Airflow orchestrator v2

The previous Airflow orchestrator was limited to running locally and had many
additional unpleasant constraints that made it hard to work with. This 
release includes a completely rewritten, new version of the Airflow orchestrator
that now relies on Docker images to run your pipelines and works both locally
and with remote Airflow deployments.

## Notable bugfixes

- Further improvements to the synchronization that transfers pipeline run information from
the MLMD database to the ZenML Server.
- The ZenML Label Studio integration can now be used with non-local (i.e.
deployed) instances. For more information see [the Label Studiodocs](https://docs.zenml.io/component-gallery/annotators/label-studio).
- The Spark example is fixed and now works again end-to-end.

## Breaking Changes

The following changes introduces with this release mey require some manual
intervention to update your current installations:

* the Airflow orchestrator now requires a newer version of Airflow
(run `zenml integration install airflow` to upgrade) and Docker installed
to work.

## What's Changed
* Fix bug when running non-local annotator instance. by @sheikhomar in https://github.com/zenml-io/zenml/pull/1045
* Introduce Permissions, Link Permissions to Roles, Restrict Access to endpoints based on Permission by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1007
* Fix copy-pasted log message for annotator by @strickvl in https://github.com/zenml-io/zenml/pull/1049
* Add warning message for client server version mismatch by @schustmi in https://github.com/zenml-io/zenml/pull/1047
* Fix path to ingress values in ZenServer recipes by @wjayesh in https://github.com/zenml-io/zenml/pull/1053
* Prevent deletion/update of default entities by @stefannica in https://github.com/zenml-io/zenml/pull/1046
* Fix Publish API docs workflow by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1054
* Fix multiple alembic heads warning by @fa9r in https://github.com/zenml-io/zenml/pull/1051
* Fix Null Step Configuration/Parameters Error by @fa9r in https://github.com/zenml-io/zenml/pull/1050
* Fix role permission migration by @schustmi in https://github.com/zenml-io/zenml/pull/1056
* Made role assignment/revokation possible through zen_server by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1059
* Bugfix/make role assignment work with enum by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1063
* Manually set scoped for each endpoint by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1064
* Add run args to local docker orchestrator settings by @schustmi in https://github.com/zenml-io/zenml/pull/1060
* Docker ZenML deployment improvements and docs by @stefannica in https://github.com/zenml-io/zenml/pull/1061
* Bugfix Mlflow service cleanup configuration by @safoinme in https://github.com/zenml-io/zenml/pull/1067
* Rename DB Tables and Fix Foreign Keys by @fa9r in https://github.com/zenml-io/zenml/pull/1058
* Paginate secrets in `AWSSecretsManager` by @chiragjn in https://github.com/zenml-io/zenml/pull/1057
* Add explicit dashboard docs by @strickvl in https://github.com/zenml-io/zenml/pull/1052
* Added GA and Gitlab to envs by @htahir1 in https://github.com/zenml-io/zenml/pull/1068
* Add Inference Server Predictor to KServe and Seldon Docs by @safoinme in https://github.com/zenml-io/zenml/pull/1048
* Rename project table to workspace by @fa9r in https://github.com/zenml-io/zenml/pull/1073
* Airflow orchestrator v2 by @schustmi in https://github.com/zenml-io/zenml/pull/1042
* Add get_or_create_run() ZenStore method by @fa9r in https://github.com/zenml-io/zenml/pull/1070
* Fix the flaky fileio tests by @schustmi in https://github.com/zenml-io/zenml/pull/1072
* BentoML Deployer Integration by @safoinme in https://github.com/zenml-io/zenml/pull/1044
* Sync Speedup by @fa9r in https://github.com/zenml-io/zenml/pull/1055
* Fixed broken links in docs and examples. by @dnth in https://github.com/zenml-io/zenml/pull/1076
* Make additional stack component config options available as a setting by @schustmi in https://github.com/zenml-io/zenml/pull/1069
* Rename `step_run_artifact` table to `step_run_input_artifact` by @fa9r in https://github.com/zenml-io/zenml/pull/1075
* Update Spark Example to ZenML post 0.20.0 by @safoinme in https://github.com/zenml-io/zenml/pull/1071
* Always set caching to false for all Kubeflow based orchestrators by @schustmi in https://github.com/zenml-io/zenml/pull/1079
* Feature/eng 1402 consolidate stack sharing by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1036

## New Contributors
* @sheikhomar made their first contribution in https://github.com/zenml-io/zenml/pull/1045
* @chiragjn made their first contribution in https://github.com/zenml-io/zenml/pull/1057

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.21.1...0.22.0

# 0.21.1

This is an ad-hoc release to fix some bugs introduced the 0.21.0 release that
made the local ZenML dashboard unusable.

## What's Changed
* Include latest (not oldest) three runs in HydratedPipelineModel by @schustmi in https://github.com/zenml-io/zenml/pull/1039
* Update docs to use `pip install [server]` by @strickvl in https://github.com/zenml-io/zenml/pull/1037
* Docs fix for Deepchecks by @strickvl in https://github.com/zenml-io/zenml/pull/1040
* Fix the pipeline run sync on sqlite and the --blocking zenml server deployment by @stefannica in https://github.com/zenml-io/zenml/pull/1041

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.21.0...0.21.1

# 0.21.0

This release primarily fixes a number of bugs that were introduced as part of
the 0.20.0 ZenServer release. These significantly improve the stability when
using ZenML with the ZenML Server.

Notable fixes include:

- Improved the synchronization that transfers pipeline run information from
the MLMD database to the ZenML Server. This helps fix a number of issues with
missing steps in the post-execution workflow, model deployment steps and other
issues.
- The Label Studio example is fixed and now works again end-to-end.
- The ZenML Label Studio integration can now be used with non-local (i.e.
deployed) instances. For more information see [the Label Studiodocs](https://docs.zenml.io/component-gallery/annotators/label-studio).

New features and other improvements:

- ZenML now uses [alembic](https://alembic.sqlalchemy.org/en/latest/) for
automated database migrations. The migrations happen automatically after every
ZenML update.
- New `zenml pipeline runs export / import / migrate` CLI commands are now
available to export, import and migrate pipeline runs from older, pre-0.20.0
versions of ZenML. The ZenML server now also automatically picks up older
pipeline runs that have been logged in the metadata store by ZenML prior to
0.20.0.
- An MLMD gRPC service can now be deployed with the ZenML Helm chart to act
as a proxy between clients, orchestrators and the MySQL database. This
significantly reduces the time it takes to run pipelines locally.
- You can now specify affinity and tolerations and node selectors to all
Kubernetes based orchestrators with the new Kubernetes Pod settings feature.


## Breaking Changes

The following changes introduces with this release mey require some manual
intervention to update your current installations:

* the zenml server helm chart `values.yaml` file has been restructured to make
  it easier to configure and to clearly distinguish between the zenml server
  component and the newly introduced gRPC service component. Please update your
  `values.yaml` copies accordingly.
* the Azure integration dependency versions have been updated. Please run
  `zenml integration install azure` to update your current installation, if
  you're using Azure.


## What's Changed
* Implement automatic alembic migration by @AlexejPenner in https://github.com/zenml-io/zenml/pull/990
* Fix GCP Artifact Store listdir empty path by @safoinme in https://github.com/zenml-io/zenml/pull/998
* Add flavors mini-video to docs by @strickvl in https://github.com/zenml-io/zenml/pull/999
* Remove the Client() warning when used inside a step by @stefannica in https://github.com/zenml-io/zenml/pull/1000
* Fix broken links caused by updated  by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1002
* Fix `FileNotFoundError` with remote path in HuggingFace Dataset materializer by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/995
* Add `zenml pipeline runs export / import / migrate` CLI commands by @fa9r in https://github.com/zenml-io/zenml/pull/977
* Log message when activating a stack as part of registration by @schustmi in https://github.com/zenml-io/zenml/pull/1005
* Minor fixes in Migration to 0.20.0 documentation by @alvarobartt in https://github.com/zenml-io/zenml/pull/1009
* Doc updates by @htahir1 in https://github.com/zenml-io/zenml/pull/1006
* Fixing broken links in docs by @dnth in https://github.com/zenml-io/zenml/pull/1018
* Label Studio example fix by @strickvl in https://github.com/zenml-io/zenml/pull/1021
* Docs for using CUDA-enabled docker images by @strickvl in https://github.com/zenml-io/zenml/pull/1010
* Add social media heading on docs page by @dnth in https://github.com/zenml-io/zenml/pull/1020
* Add executing custom command for getting requirements by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/1012
* Delay user instruction in dockerfile generation by @schustmi in https://github.com/zenml-io/zenml/pull/1004
* Update link checker configs for faster, more accurate checks by @dnth in https://github.com/zenml-io/zenml/pull/1022
* Add `pip install zenml[server]` to relevant examples by @dnth in https://github.com/zenml-io/zenml/pull/1027
* Add Tolerations and NodeAffinity to Kubernetes executor by @wefner in https://github.com/zenml-io/zenml/pull/994
* Support pydantic subclasses in BaseParameter attributes by @schustmi in https://github.com/zenml-io/zenml/pull/1023
* Unify run names across orchestrators by @schustmi in https://github.com/zenml-io/zenml/pull/1025
* Add gRPC metadata service to the ZenML helm chart by @stefannica in https://github.com/zenml-io/zenml/pull/1026
* Make the MLMD pipeline run information transfer synchronous by @stefannica in https://github.com/zenml-io/zenml/pull/1032
* Add console spinner back by @strickvl in https://github.com/zenml-io/zenml/pull/1034
* Fix Azure CLI auth problem by @wjayesh in https://github.com/zenml-io/zenml/pull/1035
* Allow non-local Label Studio instances for annotation by @strickvl in https://github.com/zenml-io/zenml/pull/1033
* Before deleting the global zen_server files, spin it down by @AlexejPenner in https://github.com/zenml-io/zenml/pull/1029
* Adding zenserver integration to stack recipe CLI  by @wjayesh in https://github.com/zenml-io/zenml/pull/1017
* Add support for Azure ZenServer by @wjayesh in https://github.com/zenml-io/zenml/pull/1024
* Kubernetes Pod settings by @schustmi in https://github.com/zenml-io/zenml/pull/1008

## New Contributors
* @alvarobartt made their first contribution in https://github.com/zenml-io/zenml/pull/1009
* @wefner made their first contribution in https://github.com/zenml-io/zenml/pull/994

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.20.5...0.21.0

# 0.20.5

ZenML 0.20.5 fixes another series of minor bugs, significantly improves the performance of the CLI, and adds an option to specify APT packages in Docker images.

## What's Changed
* Fix accessing local zen store and artifact store in containers by @stefannica in https://github.com/zenml-io/zenml/pull/976
* K3d local registry pod spec updated by @wjayesh in https://github.com/zenml-io/zenml/pull/972
* Update readme page by @dnth in https://github.com/zenml-io/zenml/pull/985
* Remove beam dependency by @schustmi in https://github.com/zenml-io/zenml/pull/986
* Fix error message when registering secret without secrets manager by @schustmi in https://github.com/zenml-io/zenml/pull/981
* Update cheat sheet up to `zenml==0.20.4` by @dnth in https://github.com/zenml-io/zenml/pull/987
* Example fixes (part 2) by @strickvl in https://github.com/zenml-io/zenml/pull/971
* Allow duplicate step classes inside a pipeline by @schustmi in https://github.com/zenml-io/zenml/pull/989
* Include deployment in azureml docker build by @schustmi in https://github.com/zenml-io/zenml/pull/984
* Automatically open browser upon `zenml up` command by @dnth in https://github.com/zenml-io/zenml/pull/978
* Add a `just_mine` flag for `zenml stack list` by @strickvl in https://github.com/zenml-io/zenml/pull/979
* Add option to specify apt packages by @schustmi in https://github.com/zenml-io/zenml/pull/982
* Replace old flavor references, fix the windows local ZenML server and other fixes by @stefannica in https://github.com/zenml-io/zenml/pull/988
* Improve docker and k8s detection by @schustmi in https://github.com/zenml-io/zenml/pull/991
* Update GH actions example by @schustmi in https://github.com/zenml-io/zenml/pull/993
* Update `MissingStepParameterError` exception message by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/996
* Separated code docs into `core` and `integration` docs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/983
* Add docs/mkdocstrings_helper.py to format script sources by @fa9r in https://github.com/zenml-io/zenml/pull/997
* Further CLI optimization by @bcdurak in https://github.com/zenml-io/zenml/pull/992

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.20.4...0.20.5


# 0.20.4

This release fixes another series of minor bugs that were introduced in 0.20.0.

## What's Changed
* Detect failed executions by @schustmi in https://github.com/zenml-io/zenml/pull/964
* Only build docker images for custom deployments by @schustmi in https://github.com/zenml-io/zenml/pull/960
* M1 Mac Installation Tutorial by @fa9r in https://github.com/zenml-io/zenml/pull/966
* Update ZenBytes links in docs by @fa9r in https://github.com/zenml-io/zenml/pull/968
* Fix the API docs builder by @stefannica in https://github.com/zenml-io/zenml/pull/967
* Fix `gpu_limit` condition in `VertexOrchestrator` by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/963
* Add simple node affinity configurations by @schustmi in https://github.com/zenml-io/zenml/pull/973
* First iteration of the CLI optimization by @bcdurak in https://github.com/zenml-io/zenml/pull/962

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.20.3...0.20.4

# 0.20.3

This release fixes another series of minor bugs that were introduced in 0.20.0.

## What's Changed
* Fixed GitHub/Colab JSON formatting error on quickstart. by @fa9r in https://github.com/zenml-io/zenml/pull/947
* Update YAML config template by @htahir1 in https://github.com/zenml-io/zenml/pull/952
* correct code from merge and fix import by @wjayesh in https://github.com/zenml-io/zenml/pull/950
* Check for active component using id instead of name by @schustmi in https://github.com/zenml-io/zenml/pull/956
* Tekton fix by @htahir1 in https://github.com/zenml-io/zenml/pull/955
* Improve zenml up/down UX and other fixes by @stefannica in https://github.com/zenml-io/zenml/pull/957
* Update kubeflow docs for multi-tenant deployments by @htahir1 in https://github.com/zenml-io/zenml/pull/958
* Update kubeflow.md by @abohmeed in https://github.com/zenml-io/zenml/pull/959
* Add additional stack validation for step operators by @schustmi in https://github.com/zenml-io/zenml/pull/954
* Fix pipeline run dashboard URL for unlisted runs by @fa9r in https://github.com/zenml-io/zenml/pull/951
* Support subclasses of registered types in recursive materialization by @fa9r in https://github.com/zenml-io/zenml/pull/953

## New Contributors
* @abohmeed made their first contribution in https://github.com/zenml-io/zenml/pull/959

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.20.2...0.20.3

# 0.20.2

After a successful release of the new ZenML server and dashboard paradigm, we set to ironing out some bugs that slipped through.

## What's Changed
* Capitalize all docs page titles. by @fa9r in https://github.com/zenml-io/zenml/pull/937
* Increase field sizes for docstrings and step parameters. by @fa9r in https://github.com/zenml-io/zenml/pull/940
* Fixing the bug in the registration of custom flavors by @bcdurak in https://github.com/zenml-io/zenml/pull/938
* Implemented `docstring` Attribute of StepModel by @fa9r in https://github.com/zenml-io/zenml/pull/936
* Fix shared stack emoji by @strickvl in https://github.com/zenml-io/zenml/pull/941
* Fix shared stacks not being allowed to be set as active. by @fa9r in https://github.com/zenml-io/zenml/pull/943
* Typo fix by @strickvl in https://github.com/zenml-io/zenml/pull/944
* Update Kubernetes Orchestrator Example by @fa9r in https://github.com/zenml-io/zenml/pull/942
* Add code and instructions to run quickstart on Colab. by @fa9r in https://github.com/zenml-io/zenml/pull/939
* Fixing the interaction in getting stacks/components by @bcdurak in https://github.com/zenml-io/zenml/pull/945
* Fix Kubeflow run name by @safoinme in https://github.com/zenml-io/zenml/pull/946
* `VertexOrchestrator` apply node selector constraint if `gpu_limit > 0` by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/935

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.20.1...0.20.2

# 0.20.0 / 0.20.1

The ZenML 0.20.0 release brings a number of big changes to its architecture and
a lot of cool new features, some of which are not backwards compatible with
previous versions.

These changes are only covered briefly in the release notes. For a detailed
view on what happened and how you can get the most out of the 0.20.0 release,
please head over to [our "ZenML 0.20.0: Our Biggest Release Yet" blog post](https://blog.zenml.io/zenml-revamped).

## Warning: Breaking Changes

Updating to ZenML 0.20.0 needs to be followed by a migration of your existing
ZenML Stacks and you may also need to make changes to your current ZenML
pipeline code. Please read [the migration guide](https://docs.zenml.io/guidelines/migration-zero-twenty) carefully and follow the
instructions to ensure a smooth transition. The guide walks you through these
changes and offers instructions on how to migrate your existing ZenML stacks and 
pipelines to the new version with minimal effort and disruption to your existing
workloads.

If you have updated to ZenML 0.20.0 by mistake or are experiencing issues with
the new version, you can always go back to the previous version by using
`pip install zenml==0.13.2` instead of `pip install zenml` when installing
ZenML manually or in your scripts.

## Overview of Changes

* [ZenML takes over the Metadata Store](https://docs.zenml.io/guidelines/migration-zero-twenty#zenml-takes-over-the-metadata-store-role)
role. All information about your ZenML Stacks, pipelines, and artifacts is now
tracked by ZenML itself directly. If you are currently using remote Metadata
Stores (e.g. deployed in cloud) in your stacks, you will probably need to
replace them with [ZenML cloud deployments](https://docs.zenml.io/guidelines/migration-zero-twenty/getting-started/deploying-zenml/deploying-zenml.md).
* the [new ZenML Dashboard](https://docs.zenml.io/guidelines/migration-zero-twenty#the-zenml-dashboard-is-now-available) is now
available with all ZenML deployments.
* [ZenML Profiles have been removed](https://docs.zenml.io/guidelines/migration-zero-twenty#removal-of-profiles-and-the-local-yaml-database)
in favor of ZenML Projects. You need to
[manually migrate your existing ZenML Profiles](https://docs.zenml.io/guidelines/migration-zero-twenty#how-to-migrate-your-profiles)
after the update.
* the [configuration of Stack Components is now decoupled from their implementation](https://docs.zenml.io/guidelines/migration-zero-twenty#decoupling-stack-component-configuration-from-implementation).
If you extended ZenML with custom stack component implementations, you may need
to update the way they are registered in ZenML.
* the updated ZenML server provides a new and improved collaborative experience.
When connected to a ZenML server, you can now [share your ZenML Stacks and Stack Components](https://docs.zenml.io/guidelines/migration-zero-twenty#shared-zenml-stacks-and-stack-components) with other users. If you were
previously using the ZenML Profiles or the ZenML server to share your ZenML
Stacks, you should switch to the new ZenML server and Dashboard and update your
existing workflows to reflect the new features.

## What's Changed
* Fix error in checking Great Expectations results when exit_on_error=True by @TimovNiedek in https://github.com/zenml-io/zenml/pull/889
* feat(user-dockerfile): Add user argument to DockerConfiguration by @cjidboon94 in https://github.com/zenml-io/zenml/pull/892
* Minor doc updates for backporting by @htahir1 in https://github.com/zenml-io/zenml/pull/894
* Removed feature request and replaced with hellonext board by @htahir1 in https://github.com/zenml-io/zenml/pull/897
* Unit tests for (some) integrations by @strickvl in https://github.com/zenml-io/zenml/pull/880
* Fixed integration installation command by @edshee in https://github.com/zenml-io/zenml/pull/900
* Pipeline configuration and intermediate representation by @schustmi in https://github.com/zenml-io/zenml/pull/898
* [Bugfix] Fix bug in auto-import of stack after recipe deploy by @wjayesh in https://github.com/zenml-io/zenml/pull/901
* Update TOC on CONTRIBUTING.md by @strickvl in https://github.com/zenml-io/zenml/pull/907
* ZenServer by @fa9r in https://github.com/zenml-io/zenml/pull/879
* Update `kserve` README by @strickvl in https://github.com/zenml-io/zenml/pull/912
* Confirmation prompts were not working by @htahir1 in https://github.com/zenml-io/zenml/pull/917
* Stacks can be registered in `Click<8.0.0` now by @AlexejPenner in https://github.com/zenml-io/zenml/pull/920
* Made Pipeline and Stack optional on the HydratedPipelineRunModel by @AlexejPenner in https://github.com/zenml-io/zenml/pull/919
* Renamed all references from ZenServer to ZenML Server in logs and comments by @htahir1 in https://github.com/zenml-io/zenml/pull/915
* Prettify pipeline runs list CLI output. by @fa9r in https://github.com/zenml-io/zenml/pull/921
* Warn when registering non-local component with local ZenServer by @strickvl in https://github.com/zenml-io/zenml/pull/904
* Fix duplicate results in pipeline run lists and unlisted flag. by @fa9r in https://github.com/zenml-io/zenml/pull/922
* Fix error log by @htahir1 in https://github.com/zenml-io/zenml/pull/916
* Update cli docs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/913
* Fix Pipeline Run Status by @fa9r in https://github.com/zenml-io/zenml/pull/923
* Change the CLI emoji for whether a stack is shared or not. by @fa9r in https://github.com/zenml-io/zenml/pull/926
* Fix running pipelines from different locations. by @fa9r in https://github.com/zenml-io/zenml/pull/925
* Fix zenml stack-component describe CLI command. by @fa9r in https://github.com/zenml-io/zenml/pull/929
* Update custom deployment to use ArtifactModel  by @safoinme in https://github.com/zenml-io/zenml/pull/928
* Fix the CI unit test and integration test failures by @stefannica in https://github.com/zenml-io/zenml/pull/924
* Add gcp zenserver recipe by @wjayesh in https://github.com/zenml-io/zenml/pull/930
* Extend Post Execution Class Properties by @fa9r in https://github.com/zenml-io/zenml/pull/931
* Fixes for examples by @strickvl in https://github.com/zenml-io/zenml/pull/918
* Update cheat sheet by @dnth in https://github.com/zenml-io/zenml/pull/932
* Fix the docstring attribute of pipeline models. by @fa9r in https://github.com/zenml-io/zenml/pull/933
* New docs post ZenML Server by @htahir1 in https://github.com/zenml-io/zenml/pull/927

## New Contributors
* @TimovNiedek made their first contribution in https://github.com/zenml-io/zenml/pull/889
* @cjidboon94 made their first contribution in https://github.com/zenml-io/zenml/pull/892
* @edshee made their first contribution in https://github.com/zenml-io/zenml/pull/900

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.13.2...0.20.0

# 0.13.2

ZenML 0.13.2 comes with a new local Docker orchestrator and many other improvements and fixes:
* You can now run your pipelines locally in isolated Docker containers per step
* @gabrielmbmb updated our MLFlow experiment tracker to work with Databricks deployments 🎉
* Documentation updates for cloud deployments and multi-tenancy Kubeflow support

## What's Changed
* Update GitHub Actions by @fa9r in https://github.com/zenml-io/zenml/pull/864
* Raise zenml exception when cyclic graph is detected by @schustmi in https://github.com/zenml-io/zenml/pull/866
* Add source to segment identify call by @htahir1 in https://github.com/zenml-io/zenml/pull/868
* Use default local paths/URIs for the local artifact and metadata stores by @stefannica in https://github.com/zenml-io/zenml/pull/873
* Implement local docker orchestrator by @schustmi in https://github.com/zenml-io/zenml/pull/862
* Update cheat sheet with latest CLI commands from 0.13.0 by @dnth in https://github.com/zenml-io/zenml/pull/867
* Add a note about importing proper DockerConfiguration module by @jsuchome in https://github.com/zenml-io/zenml/pull/877
* Bugfix/misc by @schustmi in https://github.com/zenml-io/zenml/pull/878
* Fixed bug in tfx by @htahir1 in https://github.com/zenml-io/zenml/pull/883
* Mlflow Databricks connection by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/882
* Refactor cloud guide to stack deployment guide by @wjayesh in https://github.com/zenml-io/zenml/pull/861
* Add cookie consent by @strickvl in https://github.com/zenml-io/zenml/pull/871
* Stack recipe CLI improvements by @wjayesh in https://github.com/zenml-io/zenml/pull/872
* Kubeflow workaround added by @htahir1 in https://github.com/zenml-io/zenml/pull/886


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.13.1...0.13.2

# 0.13.1

ZenML 0.13.1 is here and it comes with several quality of life improvements:

* You can now specify the exact order in which your pipelines steps should be
executed, e.g., via `step_b.after(step_a)`
* TensorBoard was moved to a separate integration so you can use it with Pytorch
and other modeling frameworks
* You can now configure the Evidently integration to ignore specific columns in 
your datasets. 

This release also contains a lot of documentation on how to deploy
custom code (like preprocessing and postprocessing code) with our KServe and
Seldon integrations.

## What's Changed
* Fix flag info on recipes in docs by @wjayesh in https://github.com/zenml-io/zenml/pull/854
* Fix some materializer issues by @schustmi in https://github.com/zenml-io/zenml/pull/852
* Add ignore columns for evidently drift detection by @SangamSwadiK in https://github.com/zenml-io/zenml/pull/851
* TensorBoard Integration by @fa9r in https://github.com/zenml-io/zenml/pull/850
* Add option to specify task dependencies by @schustmi in https://github.com/zenml-io/zenml/pull/858
* Custom code readme and docs by @safoinme in https://github.com/zenml-io/zenml/pull/853

## New Contributors
* @SangamSwadiK made their first contribution in https://github.com/zenml-io/zenml/pull/851

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.13.0...0.13.1


# 0.13.0

ZenML version 0.13.0 is chock-full with exciting features. 

[Custom Code Deployment](https://github.com/zenml-io/zenml/tree/main/examples/custom_code_deployment) is the
continuation of the Model Deployment story that we have been working on over the last few releases. Now
it is possible to deploy custom code along with your models using Kserve or Seldon.

With [Spark](https://github.com/zenml-io/zenml/tree/main/examples/spark_distributed_programming) this 
release also brings distributed processing into the ZenML toolkit.

Spinning up and configuring infrastructure is a difficult part of the MLOps journey 
and can easily become a barrier to entry. Using our [mlops-stacks](https://github.com/zenml-io/mlops-stacks)
repository, it is now possible to spin up perfectly configured infrastructure with
the corresponding ZenML stack using the ZenML CLI.

As always, we've also included various bug fixes and lots of improvements to the documentation and our examples.

## Breaking Changes

This release introduces a breaking change to the CLI by adjusting the access to
the stack component specific resources for `secret-managers` and 
`model-deployers` to be more explicitly linked to the component. Here is how:

```bash
# `zenml secret register ...` becomes 
zenml secrets-manager secret register ...

# `zenml served_models list` becomes 
zenml model-deployer models list
```

## What's Changed
* Link checker by @dnth in https://github.com/zenml-io/zenml/pull/818
* Update Readme with latest info from docs page by @dnth in https://github.com/zenml-io/zenml/pull/810
* Typo on Readme by @dnth in https://github.com/zenml-io/zenml/pull/821
* Update kserve installation to 0.9 on kserve deployment example by @safoinme in https://github.com/zenml-io/zenml/pull/823
* Allow setting caching via the `config.yaml` by @strickvl in https://github.com/zenml-io/zenml/pull/827
* Handle file-io with context manager by @aliabbasjaffri in https://github.com/zenml-io/zenml/pull/825
* Add automated link check github actions by @dnth in https://github.com/zenml-io/zenml/pull/828
* Fix the SQL zenstore to work with MySQL by @stefannica in https://github.com/zenml-io/zenml/pull/829
* Improve label studio error messages if secrets are missing or of wrong schema by @schustmi in https://github.com/zenml-io/zenml/pull/832
* Add secret scoping to the Azure Key Vault by @stefannica in https://github.com/zenml-io/zenml/pull/830
* Unify CLI concepts (removing `secret`, `feature` and `served-models`) by @strickvl in https://github.com/zenml-io/zenml/pull/833
* Put link checker as part of CI by @dnth in https://github.com/zenml-io/zenml/pull/838
* Add missing requirement for step operators by @schustmi in https://github.com/zenml-io/zenml/pull/834
* Fix broken links from link checker results by @dnth in https://github.com/zenml-io/zenml/pull/835
* Fix served models logs formatting error by @safoinme in https://github.com/zenml-io/zenml/pull/836
* New Docker build configuration by @schustmi in https://github.com/zenml-io/zenml/pull/811
* Secrets references on stack component attributes by @schustmi in https://github.com/zenml-io/zenml/pull/817
* Misc bugfixes by @schustmi in https://github.com/zenml-io/zenml/pull/842
* Pillow Image materializer by @strickvl in https://github.com/zenml-io/zenml/pull/820
* Add Tekton orchestrator by @schustmi in https://github.com/zenml-io/zenml/pull/844
* Put Slack call to action at the top of README page. by @dnth in https://github.com/zenml-io/zenml/pull/846
* Change Quickstart to Use Tabular Data by @fa9r in https://github.com/zenml-io/zenml/pull/843
* Add sleep before docker builds in release GH action by @schustmi in https://github.com/zenml-io/zenml/pull/849
* Implement Recursive Built-In Container Materializer by @fa9r in https://github.com/zenml-io/zenml/pull/812
* Custom deployment with KServe and Seldon Core by @safoinme in https://github.com/zenml-io/zenml/pull/841
* Spark Integration by @bcdurak in https://github.com/zenml-io/zenml/pull/837
* Add zenml stack recipe CLI commands by @wjayesh in https://github.com/zenml-io/zenml/pull/807

## New Contributors
* @aliabbasjaffri made their first contribution in https://github.com/zenml-io/zenml/pull/825

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.12.0...0.13.0


# 0.12.0

The 0.12.0 release comes with the third implementation of the ZenML Model Deployer abstraction: 
The [KServe](https://github.com/zenml-io/zenml/tree/main/examples/kserve_deployment) 
integration allows you to deploy any PyTorch, TensorFlow or SKLearn from within your ZenML pipelines!

We also added functionality to specify hardware resources on a step level to control the amount of memory, CPUs and GPUs that
each ZenML step has access to. This is currently limited to the Kubeflow and Vertex orchestrator but will be expanded in upcoming releases.

Additionally, we've added support for scoped secrets in our AWS, GCP and Vault Secrets Managers. These updated Secrets Managers allow
you to configure a scope which determines if secrets are shared with other ZenML Secrets Managers using the same backend.

As always, we've also included various bug fixes and lots of improvements to the documentation and our examples.

## What's Changed
* Fix Links on the examples by @safoinme in https://github.com/zenml-io/zenml/pull/782
* Fix broken links in source code by @schustmi in https://github.com/zenml-io/zenml/pull/784
* Invalidating artifact/metadata store if there is a change in one of them by @bcdurak in https://github.com/zenml-io/zenml/pull/719
* Fixed broken link in README by @htahir1 in https://github.com/zenml-io/zenml/pull/785
* Embed Cheat Sheet in a separate docs page by @fa9r in https://github.com/zenml-io/zenml/pull/790
* Add data validation documentation by @stefannica in https://github.com/zenml-io/zenml/pull/789
* Add local path for mlflow experiment tracker by @schustmi in https://github.com/zenml-io/zenml/pull/786
* Improve Docker build logs. by @fa9r in https://github.com/zenml-io/zenml/pull/793
* Allow standard library types in steps  by @stefannica in https://github.com/zenml-io/zenml/pull/799
* Added small description by @AlexejPenner in https://github.com/zenml-io/zenml/pull/801
* Replace the restriction to use Repository inside step with a warning by @stefannica in https://github.com/zenml-io/zenml/pull/792
* Adjust quickstart to data validators by @fa9r in https://github.com/zenml-io/zenml/pull/797
* Add utility function to deprecate pydantic attributes by @schustmi in https://github.com/zenml-io/zenml/pull/778
* Fix the mismatch KFP version between Kubeflow and GCP integration by @safoinme in https://github.com/zenml-io/zenml/pull/796
* Made mlflow more verbose by @htahir1 in https://github.com/zenml-io/zenml/pull/802
* Fix links by @dnth in https://github.com/zenml-io/zenml/pull/798
* KServe model deployer integration by @stefannica in https://github.com/zenml-io/zenml/pull/655
* retrieve pipeline requirement within running step by @safoinme in https://github.com/zenml-io/zenml/pull/805
* Fix `--decouple_stores` error message by @strickvl in https://github.com/zenml-io/zenml/pull/814
* Support subscripted generic step output types by @fa9r in https://github.com/zenml-io/zenml/pull/806
* Allow empty kubeconfig when using local kubeflow orchestrator by @schustmi in https://github.com/zenml-io/zenml/pull/809
* fix the secret register command in kserve docs page by @safoinme in https://github.com/zenml-io/zenml/pull/815
* Annotation example (+ stack component update) by @strickvl in https://github.com/zenml-io/zenml/pull/813
* Per-step resource configuration by @schustmi in https://github.com/zenml-io/zenml/pull/794
* Scoped secrets by @stefannica in https://github.com/zenml-io/zenml/pull/803
* Adjust examples and docs to new pipeline and step fetching syntax by @fa9r in https://github.com/zenml-io/zenml/pull/795


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.11.0...0.12.0


# 0.11.0

Our 0.11.0 release contains our new annotation workflow and stack component. We've been blogging about this for a few weeks, and even started maintaining our own repository of open-source annotation tools. With ZenML 0.11.0 you can bring data labeling into your MLOps pipelines and workflows as a first-class citizen. We've started our first iteration of this functionality by integrating with [Label Studio](https://labelstud.io/), a leader in the open-source annotation tool space.

This release also includes a ton of updates to our documentation. (Seriously, go check them out! We added tens of thousands of words since the last release.) We continued the work on our data validation story from the previous release: [Deepchecks](https://deepchecks.com/) is the newest data validator we support, and we updated our Evidently and Whylogs integrations to include all the latest and greatest from those tools.

Beyond this, as usual we included a number of smaller bugfixes and documentation changes to cumulatively improve experience of using ZenML as a user. For a detailed look at what's changed, give [our full release notes](https://github.com/zenml-io/zenml/releases/tag/0.11.0) a glance.

## Breaking Changes

The 0.11.0 release remodels the Evidently and whylogs integrations as Data Validator stack components, in an effort to converge all data profiling and validation libraries around the same abstraction. As a consequence, you now need to configure and add a Data Validator stack component to your stack if you wish to use Evidently or whylogs in your pipelines:

* for Evidently:

    ```shell
    zenml data-validator register evidently -f evidently
    zenml stack update -dv evidently
    ```

* for whylogs:

    ```shell
    zenml data-validator register whylogs -f whylogs
    zenml stack update -dv whylogs
    ```

In this release, we have also upgraded the Evidently and whylogs libraries to their latest and greatest versions (whylogs 1.0.6 and evidently 0.1.52). These versions introduce non-backwards compatible changes that are also reflected in the ZenML integrations:

* Evidently profiles are now materialized using their original `evidently.model_profile.Profile ` data type and the builtin `EvidentlyProfileStep` step now also returns a `Profile` instance instead of the previous dictionary representation. This may impact your existing pipelines as you may have to update your steps to take in `Profile` artifact instances instead of dictionaries.

* the whylogs `whylogs.DatasetProfile` data type was replaced by `whylogs.core.DatasetProfileView` in the builtin whylogs materializer and steps. This may impact your existing pipelines as you may have to update your steps to return and take in `whylogs.core.DatasetProfileView` artifact instances instead of `whylogs.DatasetProfile` objects.

* the whylogs library has gone through a major transformation that completely removed the session concept. As a result, the `enable_whylogs` step decorator was replaced by an `enable_whylabs` step decorator. You only need to use the step decorator if you wish to log your profiles to the Whylabs platform.

Pleaser refer to the examples provided for Evidently and whylogs to learn more about how to use the new integration versions:

* [Evidently](https://github.com/zenml-io/zenml/tree/main/examples/evidently_drift_detection)
* [whylogs/Whylabs](https://github.com/zenml-io/zenml/tree/main/examples/whylogs_data_profiling)

## What's Changed
* Changed PR template to reflect integrations flow by @htahir1 in https://github.com/zenml-io/zenml/pull/732
* Fix broken Feast integration by @strickvl in https://github.com/zenml-io/zenml/pull/737
* Describe args run.py application actually supports by @jsuchome in https://github.com/zenml-io/zenml/pull/740
* Update kubernetes_orchestration example by @fa9r in https://github.com/zenml-io/zenml/pull/743
* Fix some example links by @schustmi in https://github.com/zenml-io/zenml/pull/744
* Fix broken links for docs and examples by @safoinme in https://github.com/zenml-io/zenml/pull/747
* Update CONTRIBUTING.md by @strickvl in https://github.com/zenml-io/zenml/pull/748
* Fix references to types when registering secrets managers by @strickvl in https://github.com/zenml-io/zenml/pull/738
* Make examples conform to best practices guidance by @AlexejPenner in https://github.com/zenml-io/zenml/pull/734
* API Docs with Cookies and Milk by @AlexejPenner in https://github.com/zenml-io/zenml/pull/758
* Use correct region when trying to fetch ECR repositories by @schustmi in https://github.com/zenml-io/zenml/pull/761
* Encode azure secrets manager secret names by @schustmi in https://github.com/zenml-io/zenml/pull/760
* Add nested mlflow option to enable_mlflow decorator by @Val3nt-ML in https://github.com/zenml-io/zenml/pull/742
* Combine all MLMD contexts by @schustmi in https://github.com/zenml-io/zenml/pull/759
* Prevent extra attributes when initializing StackComponents by @schustmi in https://github.com/zenml-io/zenml/pull/763
* New Docker images by @schustmi in https://github.com/zenml-io/zenml/pull/757
* Fix facets magic display in Google Colab by @fa9r in https://github.com/zenml-io/zenml/pull/765
* Allow fetching secrets from within a step by @schustmi in https://github.com/zenml-io/zenml/pull/766
* Add notebook to great expectation example by @stefannica in https://github.com/zenml-io/zenml/pull/768
* Module resolving and path fixes by @schustmi in https://github.com/zenml-io/zenml/pull/735
* Fix step operator entrypoint by @schustmi in https://github.com/zenml-io/zenml/pull/771
* Docs Revamp by @fa9r in https://github.com/zenml-io/zenml/pull/769
* Allow fetching pipeline/step by name, class or instance by @AlexejPenner in https://github.com/zenml-io/zenml/pull/733
* Data Validator abstraction and Deepchecks integration by @htahir1 in https://github.com/zenml-io/zenml/pull/553
* rolling back seldon deployment example by @safoinme in https://github.com/zenml-io/zenml/pull/774
* Added changes from 1062 and 1061 into the updated docs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/775
* Refresh Examples on `zenml examples pull` by @fa9r in https://github.com/zenml-io/zenml/pull/776
* Annotation stack component and Label Studio integration by @strickvl in https://github.com/zenml-io/zenml/pull/764
* Add optional machine specs to vertex orchestrator by @felixthebeard in https://github.com/zenml-io/zenml/pull/762

## New Contributors
* @jsuchome made their first contribution in https://github.com/zenml-io/zenml/pull/740
* @Val3nt-ML made their first contribution in https://github.com/zenml-io/zenml/pull/742
* @felixthebeard made their first contribution in https://github.com/zenml-io/zenml/pull/762

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.10.0...0.11.0

# 0.10.0

The 0.10.0 release continues our streak of extending ZenML with support for new
orchestrators, this time by adding
[the Kubernetes Native Orchestrator](https://github.com/zenml-io/zenml/tree/main/examples/kubernetes_orchestration).
This orchestrator is a lightweight alternative to other distributed orchestrators
like Airflow or Kubeflow that gives our users the ability to run pipelines in any
Kubernetes cluster without having to install and manage additional tools or
components. 

This release features another integration that we are really excited about: the
popular data profiling and validation library [Great Expectations](https://greatexpectations.io/)
is our first Data Validator, a new category of stack components that we are in
the process of standardizing, that will make data quality a central feature of
ZenML. [The ZenML Great Expectations integration](https://github.com/zenml-io/zenml/tree/main/examples/great_expectations_data_validation)
eliminates the complexity associated with configuring the store backends for
Great Expectations by reusing our Artifact Store concept for that purpose and
gives ZenML users immediate access to Great Expectations in both local and cloud
settings.

Last but not least, the release also includes a new secrets manager implementation,
courtesy of our contributor @karimhabush, that integrates ZenML with the
[Hashicorp Vault Server](https://www.vaultproject.io) as well as a few other bug
fixes and improvements.

## What's Changed
* Fix broken link by @strickvl in https://github.com/zenml-io/zenml/pull/707
* Add stack component copy command by @schustmi in https://github.com/zenml-io/zenml/pull/705
* Remove `force` flag from secrets managers' implementation by @strickvl in https://github.com/zenml-io/zenml/pull/708
* Fixed wrong example README by @AlexejPenner in https://github.com/zenml-io/zenml/pull/712
* Fix dead links in integrations docs. by @fa9r in https://github.com/zenml-io/zenml/pull/710
* Fixing link to guide by @chethanuk-plutoflume in https://github.com/zenml-io/zenml/pull/716
* Adding azure-keyvault-secrets to azure integration dependencies by @safoinme in https://github.com/zenml-io/zenml/pull/717
* Fix MLflow repeated deployment error by @fa9r in https://github.com/zenml-io/zenml/pull/715
* Replace alerter standard steps by Slack-specific steps to fix config issue. by @fa9r in https://github.com/zenml-io/zenml/pull/714
* Fix broken links on README by @dnth in https://github.com/zenml-io/zenml/pull/722
* Invalidate cache by @strickvl in https://github.com/zenml-io/zenml/pull/724
* Skip Cleaning Trace on tests by @safoinme in https://github.com/zenml-io/zenml/pull/725
* Kubernetes orchestrator by @fa9r in https://github.com/zenml-io/zenml/pull/688
* Vault Secrets Manager integration - KV Secrets Engine by @karimhabush in https://github.com/zenml-io/zenml/pull/689
* Add missing help text for CLI commands  by @safoinme in https://github.com/zenml-io/zenml/pull/723
* Misc bugfixes by @schustmi in https://github.com/zenml-io/zenml/pull/713
* Great Expectations integration for data validation by @strickvl in https://github.com/zenml-io/zenml/pull/555
* Fix GCP artifact store by @schustmi in https://github.com/zenml-io/zenml/pull/730

## New Contributors
* @chethanuk-plutoflume made their first contribution in https://github.com/zenml-io/zenml/pull/716
* @dnth made their first contribution in https://github.com/zenml-io/zenml/pull/722
* @karimhabush made their first contribution in https://github.com/zenml-io/zenml/pull/689

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.9.0...0.10.0

# 0.9.0

It's been a couple of weeks, so it's time for a new release! 0.9.0 brings two whole new orchestrators, one of which was contributed by a community member just one day after we unveiled new documentation for orchestrator extensibility! The release also includes a new secrets manager, a Slack integration and a bunch of other smaller changes across the codebase. (Our new orchestrators are exciting enough that they'll get their own blog posts to showcase their strengths in due course.)

Beyond this, as usual we included a number of smaller bugfixes and documentation changes to cumulatively improve experience of using ZenML as a user.

## What's Changed
* Pass secret to release linting workflow by @schustmi in https://github.com/zenml-io/zenml/pull/642
* Fix typo in example by @anencore94 in https://github.com/zenml-io/zenml/pull/644
* Added `SecretExistsError` in `register_secret()` method by @hectorLop in https://github.com/zenml-io/zenml/pull/648
* Fix broken GCP Secrets example CLI command by @strickvl in https://github.com/zenml-io/zenml/pull/649
* Upgrade to `ml-pipelines-sdk` v1.8.0 by @strickvl in https://github.com/zenml-io/zenml/pull/651
* Fix example list CLI command name by @schustmi in https://github.com/zenml-io/zenml/pull/647
* Fix README by @strickvl in https://github.com/zenml-io/zenml/pull/657
* Fix broken links in docs by @safoinme in https://github.com/zenml-io/zenml/pull/652
* Add `VertexOrchestrator` implementation by @gabrielmbmb in https://github.com/zenml-io/zenml/pull/640
* Fix index page links and Heading links. by @safoinme in https://github.com/zenml-io/zenml/pull/661
* Add docstring checks to `pre-commit` script by @strickvl in https://github.com/zenml-io/zenml/pull/481
* Pin MLflow to <1.26.0 to prevent issues when matplotlib is not installed by @fa9r in https://github.com/zenml-io/zenml/pull/666
* Making `utils` more consistent by @strickvl in https://github.com/zenml-io/zenml/pull/658
* Fix linting failures on `develop` by @strickvl in https://github.com/zenml-io/zenml/pull/669
* Add docstrings for `config` module by @strickvl in https://github.com/zenml-io/zenml/pull/668
* Miscellaneous bugfixes by @schustmi in https://github.com/zenml-io/zenml/pull/660
* Make ZenServer dependencies optional by @schustmi in https://github.com/zenml-io/zenml/pull/665
* Implement Azure Secrets Manager integration by @strickvl in https://github.com/zenml-io/zenml/pull/654
* Replace `codespell` with `pyspelling` by @strickvl in https://github.com/zenml-io/zenml/pull/663
* Add Community Event to README by @htahir1 in https://github.com/zenml-io/zenml/pull/674
* Fix failing integration tests by @strickvl in https://github.com/zenml-io/zenml/pull/677
* Add `io` and `model_deployers` docstring checks by @strickvl in https://github.com/zenml-io/zenml/pull/675
* Update `zenml stack down` to use --force flag by @schustmi in https://github.com/zenml-io/zenml/pull/673
* Fix class resolving on windows by @schustmi in https://github.com/zenml-io/zenml/pull/678
* Added `pipelines` docstring checks by @strickvl in https://github.com/zenml-io/zenml/pull/676
* Docstring checks for `cli` module by @strickvl in https://github.com/zenml-io/zenml/pull/680
* Docstring fixes for `entrypoints` and `experiment_trackers` modules by @strickvl in https://github.com/zenml-io/zenml/pull/672
* Clearer Contributing.md by @htahir1 in https://github.com/zenml-io/zenml/pull/681
* How to access secrets within step added to docs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/653
* FIX: Log a warning instead of raising an `AssertionError` by @ketangangal in https://github.com/zenml-io/zenml/pull/628
* Reviewer Reminder by @htahir1 in https://github.com/zenml-io/zenml/pull/683
* Fix some docs phrasings and headers by @strickvl in https://github.com/zenml-io/zenml/pull/670
* Implement `SlackAlerter.ask()` by @fa9r in https://github.com/zenml-io/zenml/pull/662
* Extending Alerters Docs by @fa9r in https://github.com/zenml-io/zenml/pull/690
* Sane defaults for MySQL by @htahir1 in https://github.com/zenml-io/zenml/pull/691
* pd.Series materializer by @Reed-Schimmel in https://github.com/zenml-io/zenml/pull/684
* Add docstrings for `materializers` and `metadata_stores` by @strickvl in https://github.com/zenml-io/zenml/pull/694
* Docstrings for the `integrations` module(s) by @strickvl in https://github.com/zenml-io/zenml/pull/692
* Add remaining docstrings by @strickvl in https://github.com/zenml-io/zenml/pull/696
* Allow enabling mlflow/wandb/whylogs with the class-based api by @schustmi in https://github.com/zenml-io/zenml/pull/697
* GitHub Actions orchestrator by @schustmi in https://github.com/zenml-io/zenml/pull/685
* Created MySQL docs, Vertex AI docs, and step.entrypoint() by @AlexejPenner in https://github.com/zenml-io/zenml/pull/698
* Update ignored words by @strickvl in https://github.com/zenml-io/zenml/pull/701
* Stack Component registering made easier by @AlexejPenner in https://github.com/zenml-io/zenml/pull/695
* Cleaning up the docs after the revamp by @bcdurak in https://github.com/zenml-io/zenml/pull/699
* Add model deployer to CLI docs by @safoinme in https://github.com/zenml-io/zenml/pull/702
* Merge Cloud Integrations and create a Vertex AI Example by @AlexejPenner in https://github.com/zenml-io/zenml/pull/693
* GitHub actions orchestrator example by @schustmi in https://github.com/zenml-io/zenml/pull/703

## New Contributors
* @anencore94 made their first contribution in https://github.com/zenml-io/zenml/pull/644
* @hectorLop made their first contribution in https://github.com/zenml-io/zenml/pull/648
* @gabrielmbmb made their first contribution in https://github.com/zenml-io/zenml/pull/640
* @ketangangal made their first contribution in https://github.com/zenml-io/zenml/pull/628
* @Reed-Schimmel made their first contribution in https://github.com/zenml-io/zenml/pull/684

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.8.1...0.9.0

# 0.8.1

ZenML 0.8.1 is here and it comes with support for Python 3.9 🎉. It also includes major updates to our 
documentation, fixes some broken links in our examples and improves the `zenml go` command which helps 
you get started with ZenML.

## What's Changed
* Hotfix/fix failing release by @AlexejPenner in https://github.com/zenml-io/zenml/pull/611
* Remove autocomplete + alerter from documentation by @strickvl in https://github.com/zenml-io/zenml/pull/612
* Support Python 3.9 by @htahir1 in https://github.com/zenml-io/zenml/pull/605
* Revert README by @htahir1 in https://github.com/zenml-io/zenml/pull/624
* Don't build cuda image on release by @schustmi in https://github.com/zenml-io/zenml/pull/623
* Update quickstart for `zenml go` by @fa9r in https://github.com/zenml-io/zenml/pull/625
* Improve kubeflow manual setup logs by @schustmi in https://github.com/zenml-io/zenml/pull/622
* Added missing space to error message by @AlexejPenner in https://github.com/zenml-io/zenml/pull/614
* Added --set flag to register stack command by @AlexejPenner in https://github.com/zenml-io/zenml/pull/613
* Fixes for multiple examples by @schustmi in https://github.com/zenml-io/zenml/pull/626
* Bring back the `served_model` format to the keras materializer by @stefannica in https://github.com/zenml-io/zenml/pull/629
* Fix broken example links by @schustmi in https://github.com/zenml-io/zenml/pull/630
* FAQ edits by @strickvl in https://github.com/zenml-io/zenml/pull/634
* Fix version parsing by @schustmi in https://github.com/zenml-io/zenml/pull/633
* Completed Best Practices Page by @AlexejPenner in https://github.com/zenml-io/zenml/pull/635
* Comments on Issues should no longer trigger gh actions by @AlexejPenner in https://github.com/zenml-io/zenml/pull/636
* Revise `CONTRIBUTING.md` by @strickvl in https://github.com/zenml-io/zenml/pull/615
* Alerter Component for Slack Integration by @fa9r in https://github.com/zenml-io/zenml/pull/586
* Update `zenml go` to open quickstart/notebooks. by @fa9r in https://github.com/zenml-io/zenml/pull/631
* Update examples by @schustmi in https://github.com/zenml-io/zenml/pull/638
* More detailed instructions on creating an integration by @AlexejPenner in https://github.com/zenml-io/zenml/pull/639
* Added publish api docs to release workflow by @AlexejPenner in https://github.com/zenml-io/zenml/pull/641
* Added *.md to ignore paths by @AlexejPenner in https://github.com/zenml-io/zenml/pull/637
* Update README and Docs with new messaging and fix broken links by @htahir1 in https://github.com/zenml-io/zenml/pull/632

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.8.0...0.8.1

# 0.8.0

## 🧘‍♀️ Extensibility is our middle name

* The ability to register custom stack component flavors (and renaming types to
  flavor (Registering custom stack component flavors by @bcdurak in
  https://github.com/zenml-io/zenml/pull/541)
* The ability to easily extend orchestrators
* Documentation for stacks, stack components and flavors by @bcdurak in
  https://github.com/zenml-io/zenml/pull/607
* Allow configuration of s3fs by @schustmi in
  https://github.com/zenml-io/zenml/pull/532
* Ability to use SSL to connect to MySQL clients (That allows for connecting to
  Cloud based MYSQL deployments)
* New MySQL metadata stores by @bcdurak in
  https://github.com/zenml-io/zenml/pull/580!
* Docs and messaging change
* Make Orchestrators more extensible and simplify the interface by @AlexejPenner
  in https://github.com/zenml-io/zenml/pull/581
* S3 Compatible Artifact Store and materializers file handling by @safoinme in
  https://github.com/zenml-io/zenml/pull/598

## Manage your stacks

* Update stack and stack components via the CLI by @strickvl in
  https://github.com/zenml-io/zenml/pull/497
* Add `stack delete` confirmation prompt by @strickvl in
  https://github.com/zenml-io/zenml/pull/548
* Add `zenml stack export` and `zenml stack import` commands by @fa9r in
  https://github.com/zenml-io/zenml/pull/560

## Collaboration

* User management by @schustmi in https://github.com/zenml-io/zenml/pull/500

## CLI improvements

* CLI speed improvement by @bcdurak in
  https://github.com/zenml-io/zenml/pull/567
* Ensure `rich` CLI displays full text and wraps table text by @strickvl in
  https://github.com/zenml-io/zenml/pull/577
* Add CLI command to remove stack component attribute by @strickvl in
  https://github.com/zenml-io/zenml/pull/590
* Beautify CLI by grouping commands list into tags by @safoinme in
  https://github.com/zenml-io/zenml/pull/546

## New integrations:

* Add PyTorch example by @htahir1 in https://github.com/zenml-io/zenml/pull/559
* Added GCP as secret manager by @AlexejPenner in
  https://github.com/zenml-io/zenml/pull/556

## Documentation / ZenBytes etc

* ZenBytes update (and ZenML Projects)
* Beautification of Examples by @AlexejPenner in
  https://github.com/zenml-io/zenml/pull/491
* Document global configuration and repository by @stefannica in
  https://github.com/zenml-io/zenml/pull/579
* ZenML Collaboration docs by @stefannica in
  https://github.com/zenml-io/zenml/pull/597

## ➕ Other Updates, Additions and Fixes

* Experiment tracker stack components by @htahir1 in
  https://github.com/zenml-io/zenml/pull/530
* Secret Manager improvements and Seldon Core secret passing by @stefannica in
  https://github.com/zenml-io/zenml/pull/529
* Pipeline run tracking by @schustmi in
  https://github.com/zenml-io/zenml/pull/601
* Stream model deployer logs through CLI by @stefannica in
  https://github.com/zenml-io/zenml/pull/557
* Fix various usability bugs by @stefannica in
  https://github.com/zenml-io/zenml/pull/561
* Replace `-f` and `--force` with `-y` and `--yes` by @strickvl in
  https://github.com/zenml-io/zenml/pull/566
* Make it easier to submit issues by @htahir1 in
  https://github.com/zenml-io/zenml/pull/571
* Sync the repository and local store with the disk configuration files and
  other fixes by @stefannica in https://github.com/zenml-io/zenml/pull/588
* Add ability to give in-line pip requirements for pipeline by @strickvl in
  https://github.com/zenml-io/zenml/pull/583
* Fix evidently visualizer on Colab by @fa9r in
  https://github.com/zenml-io/zenml/pull/592

## 🙌 Community Contributions

* @Ankur3107 made their first contribution in
  https://github.com/zenml-io/zenml/pull/467
* @MateusGheorghe made their first contribution in
  https://github.com/zenml-io/zenml/pull/523
* Added support for scipy sparse matrices by @avramdj in
  https://github.com/zenml-io/zenml/pull/534

# 0.7.3

## 📊 Experiment Tracking Components

[PR #530](https://github.com/zenml-io/zenml/pull/530) adds a new stack component to ZenMLs ever-growing list:  `experiment_trackers` allows users to configure your experiment tracking tools with ZenML. Examples of experiment tracking tools are [Weights&Biases](https://wandb.ai), [mlflow](https://mlflow.org), [Neptune](https://neptune.ai), amongst others.

Existing users might be confused, as ZenML has had MLflow and wandb support for a while now without such a component. However, this component allows uses more control over the configuration of MLflow and wandb with the new `MLFlowExperimentTracker` and 
 `WandbExperimentTracker` components. This allows these tools to work in more scenarios than the currently limiting local use-cases.

## 🔎 XGBoost and LightGBM support

[XGBoost](https://xgboost.readthedocs.io/en/stable/) and [LightGBM](https://lightgbm.readthedocs.io/) are one of the most widely used boosting algorithm libraries out there. This release adds materializers for native objects for each library.

Check out [both examples here](https://github.com/zenml-io/zenml/tree/main/examples) and PR's [#544](https://github.com/zenml-io/zenml/pull/544) and [#538](https://github.com/zenml-io/zenml/pull/538) for more details.

## 📂 Parameterized S3FS support to enable non-AWS S3 storage (minio, ceph)

A big complaint of the [S3 Artifact Store](https://github.com/zenml-io/zenml/blob/main/src/zenml/integrations/s3/artifact_stores/s3_artifact_store.py) integration was that it was hard to parameterize it in a way that it supports non-AWS S3 storage like [minio](https://min.io/) and [ceph](https://docs.ceph.com/en/latest/radosgw/s3/). The latest release 
 made this super simple! When you want to register an S3ArtifactStore from the CLI, you can now pass in  `client_kwargs`, `config_kwargs` or `s3_additional_kwargs` as a JSON string. For example:

```shell
zenml artifact-store register my_s3_store --type=s3 --path=s3://my_bucket \
    --client_kwargs='{"endpoint_url": "http://my-s3-endpoint"}'
```

See PR [#532](https://github.com/zenml-io/zenml/pull/532) for more details.

## 🧱 New CLI commands to update stack components

We added functionality to allow users to update stacks that already exist. This shows the basic workflow:

```shell
zenml orchestrator register local_orchestrator2 -t local
zenml stack update default -o local_orchestrator2
zenml stack describe default
zenml container-registry register local_registry --type=default --uri=localhost:5000
zenml container-registry update local --uri='somethingelse.com'
zenml container-registry rename local local2
zenml container-registry describe local2
zenml stack rename default new_default
zenml stack update new_default -c local2
zenml stack describe new_default
zenml stack remove-component -c
```
More details are in the [CLI docs](https://apidocs.zenml.io/0.7.3/cli/). 
Users can add new stack components to a pre-existing stack, or they can modify 
already-present stack components. They can also rename their stack and individual stack components.

## 🐛 Seldon Core authentication through ZenML secrets

The Seldon Core Model Deployer stack component was updated in this release to allow the configuration of ZenML secrets with credentials that authenticate Seldon to access the Artifact Store. The Seldon Core integration provides 3 different secret schemas for the 3 flavors of Artifact Store: AWS, GCP, and Azure, but custom secrets can be used as well. For more information on how to use this feature please refer to our [Seldon Core deployment example](https://github.com/zenml-io/zenml/tree/main/examples/seldon_deployment).

Lastly, we had numerous other changes such as ensuring the PyTorch materializer works across all artifact stores 
and the Kubeflow Metadata Store can be easily queried locally.

## Detailed Changelog
* Fix caching & `mypy` errors by @strickvl in https://github.com/zenml-io/zenml/pull/524
* Switch unit test from local_daemon to multiprocessing by @jwwwb in https://github.com/zenml-io/zenml/pull/508
* Change Pytorch materializer to support remote storage by @safoinme in https://github.com/zenml-io/zenml/pull/525
* Remove TODO from Feature Store `init` docstring by @strickvl in https://github.com/zenml-io/zenml/pull/527
* Fixed typo predicter -> predictor by @MateusGheorghe in https://github.com/zenml-io/zenml/pull/523
* Fix mypy errors by @strickvl in https://github.com/zenml-io/zenml/pull/528
* Replaced old local_* logic by @htahir1 in https://github.com/zenml-io/zenml/pull/531
* capitalize aws username in ECR docs by @wjayesh in https://github.com/zenml-io/zenml/pull/533
* Build docker base images quicker after release by @schustmi in https://github.com/zenml-io/zenml/pull/537
* Allow configuration of s3fs by @schustmi in https://github.com/zenml-io/zenml/pull/532
* Update contributing and fix ci badge to main by @htahir1 in https://github.com/zenml-io/zenml/pull/536
* Added XGboost integration by @htahir1 in https://github.com/zenml-io/zenml/pull/538
* Added fa9r to .github/teams.yml. by @fa9r in https://github.com/zenml-io/zenml/pull/539
* Secret Manager improvements and Seldon Core secret passing by @stefannica in https://github.com/zenml-io/zenml/pull/529
* User management by @schustmi in https://github.com/zenml-io/zenml/pull/500
* Update stack and stack components via the CLI by @strickvl in https://github.com/zenml-io/zenml/pull/497
* Added lightgbm integration by @htahir1 in https://github.com/zenml-io/zenml/pull/544
* Fix the Kubeflow metadata store and other stack management improvements by @stefannica in https://github.com/zenml-io/zenml/pull/542
* Experiment tracker stack components by @htahir1 in https://github.com/zenml-io/zenml/pull/530

## New Contributors
* @MateusGheorghe made their first contribution in https://github.com/zenml-io/zenml/pull/523
* @fa9r made their first contribution in https://github.com/zenml-io/zenml/pull/539

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.7.2...0.7.3
**Blog Post**: https://blog.zenml.io/zero-seven-two-three-release/

# 0.7.2

0.7.2 is a minor release which quickly patches some bugs found in the last
release to do with Seldon and Mlflow deployment.

This release also features initial versions of two amazing new integrations:
[HuggingFace](https://huggingface.co/) and [Weights&Biases](https://wandb.ai/site)!

- HuggingFace models are now supported to be passed through ZenML pipelines!
- You can now track your pipeline runs with Weights&Biases with the new
`enable_wandb` decorator!

Continuous model deployment with MLflow has been improved with ZenML 0.7.2. A new
MLflow Model Deployer Stack component is now available and needs to be part of
your stack to be able to deploy models:

```bash
zenml integration install mlflow
zenml model-deployer register mlflow --type=mlflow
zenml stack register local_with_mlflow -m default -a default -o default -d mlflow
zenml stack set local_with_mlflow
```

The MLflow Model Deployer is yet another addition to the list of Model Deployers
available in ZenML. You can read more on deploying models to production with MLflow
in our [Continuous Training and Deployment documentation section](https://docs.zenml.io/advanced-guide/practical/deploying-models) and 
our [MLflow deployment example](https://github.com/zenml-io/zenml/tree/main/examples/mlflow_deployment).

## What's Changed
* Fix the seldon deployment example by @htahir1 in https://github.com/zenml-io/zenml/pull/511
* Create base deployer and refactor MLflow deployer implementation by @wjayesh in https://github.com/zenml-io/zenml/pull/489
* Add nlp example by @Ankur3107 in https://github.com/zenml-io/zenml/pull/467
* Fix typos by @strickvl in https://github.com/zenml-io/zenml/pull/515
* Bugfix/hypothesis given does not work with fixture by @jwwwb in https://github.com/zenml-io/zenml/pull/513
* Bug: fix long Kubernetes labels in Seldon deployments by @stefannica in https://github.com/zenml-io/zenml/pull/514
* Change prediction_uri to prediction_url in MLflow deployer by @stefannica in https://github.com/zenml-io/zenml/pull/516
* Simplify HuggingFace Integration by @AlexejPenner in https://github.com/zenml-io/zenml/pull/517
* Weights & Biases Basic Integration by @htahir1 in https://github.com/zenml-io/zenml/pull/518

## New Contributors
* @Ankur3107 made their first contribution in https://github.com/zenml-io/zenml/pull/467

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.7.1...0.7.2

# 0.7.1

The release introduces the [Seldon Core](https://github.com/SeldonIO/seldon-core) ZenML integration, featuring the
*Seldon Core Model Deployer* and a *Seldon Core standard model deployer step*.
The [*Model Deployer*](https://docs.zenml.io/component-gallery/model-deployers/model-deployers)
is a new type of stack component that enables you to develop continuous
model deployment pipelines that train models and continuously deploy them to an
external model serving tool, service or platform. You can read more on deploying models
to production with Seldon Core in our
[Continuous Training and Deployment documentation section](https://docs.zenml.io/component-gallery/model-deployers/model-deployers) and our [Seldon Core deployment example](https://github.com/zenml-io/zenml/tree/main/examples/seldon_deployment).

We also see two new integrations with [Feast](https://feast.dev) as ZenML's first feature store integration. Feature stores allow data teams to serve data via an offline store and an online low-latency store where data is kept in sync between the two. It also offers a centralized registry where features (and feature schemas) are stored for use within a team or wider organization. ZenML now supports connecting to a Redis-backed Feast feature store as a stack component integration. Check out the [full example](https://github.com/zenml-io/zenml/tree/release/0.7.1/examples/feature_store) to see it in action! 

0.7.1 also brings  an addition to ZenML training library integrations with [NeuralProphet](https://neuralprophet.com/html/index.html). Check out the new [example](https://github.com/zenml-io/zenml/tree/main/examples) for more details, and the [docs](https://docs.zenml.io) for more further detail on all new features!

## What's Changed
* Add linting of examples to `pre-commit` by @strickvl in https://github.com/zenml-io/zenml/pull/490
* Remove dev-specific entries in `.gitignore` by @strickvl in https://github.com/zenml-io/zenml/pull/488
* Produce periodic mocked data for Segment/Mixpanel by @AlexejPenner in https://github.com/zenml-io/zenml/pull/487
* Abstractions for artifact stores by @bcdurak in https://github.com/zenml-io/zenml/pull/474
* enable and disable cache from runtime config by @AlexejPenner in https://github.com/zenml-io/zenml/pull/492
* Basic Seldon Core Deployment Service by @stefannica in https://github.com/zenml-io/zenml/pull/495
* Parallelize our test suite and make errors more readable by @alex-zenml in https://github.com/zenml-io/zenml/pull/378
* Provision local zenml service by @jwwwb in https://github.com/zenml-io/zenml/pull/496
* bugfix/optional-secrets-manager by @safoinme in https://github.com/zenml-io/zenml/pull/493
* Quick fix for copying folders by @bcdurak in https://github.com/zenml-io/zenml/pull/501
* Pin exact ml-pipelines-sdk version by @schustmi in https://github.com/zenml-io/zenml/pull/506
* Seldon Core model deployer stack component and standard step by @stefannica in https://github.com/zenml-io/zenml/pull/499
* Fix datetime test / bug by @strickvl in https://github.com/zenml-io/zenml/pull/507
* Added NeuralProphet integration by @htahir1 in https://github.com/zenml-io/zenml/pull/504
* Feature Store (Feast with Redis) by @strickvl in https://github.com/zenml-io/zenml/pull/498


# 0.7.0

With ZenML 0.7.0, a lot has been revamped under the hood about how things are stored. Importantly what this means is that ZenML now has system-wide profiles that let you register stacks to share across several of your projects! If you still want to manage your stacks for each project folder individually, profiles still let you do that as well.

Most projects of any complexity will require passwords or tokens to access data and infrastructure, and for this purpose ZenML 0.7.0 introduces [the Secrets Manager](https://docs.zenml.io/component-gallery/secrets-managers/secrets-managers) stack component to seamlessly pass around these values to your steps. Our AWS integration also allows you to use AWS Secrets Manager as a backend to handle all your secret persistence needs.

Finally, in addition to the new AzureML and Sagemaker Step Operators that version 0.6.3 brought, this release also adds the ability to [run individual steps on GCP's Vertex AI](https://docs.zenml.io/component-gallery/step-operators/gcloud-vertexai).

Beyond this, some smaller bugfixes and documentation changes combine to make ZenML 0.7.0 a more pleasant user experience.

## What's Changed
* Added quick mention of how to use dockerignore by @AlexejPenner in https://github.com/zenml-io/zenml/pull/468
* Made rich traceback optional with ENV variable by @htahir1 in https://github.com/zenml-io/zenml/pull/472
* Separate stack persistence from repo implementation by @jwwwb in https://github.com/zenml-io/zenml/pull/462
* Adding safoine username to github team by @safoinme in https://github.com/zenml-io/zenml/pull/475
* Fix `zenml stack describe` bug by @strickvl in https://github.com/zenml-io/zenml/pull/476
* ZenProfiles and centralized ZenML repositories by @stefannica in https://github.com/zenml-io/zenml/pull/471
* Add `examples` folder to linting script by @strickvl in https://github.com/zenml-io/zenml/pull/482
* Vertex AI integration and numerous other changes by @htahir1 in https://github.com/zenml-io/zenml/pull/477
* Fix profile handing in the Azure ML step operator by @stefannica in https://github.com/zenml-io/zenml/pull/483
* Copy the entire stack configuration into containers by @stefannica in https://github.com/zenml-io/zenml/pull/480
* Improve some things with the Profiles CLI output by @stefannica in https://github.com/zenml-io/zenml/pull/484
* Secrets manager stack component and interface by @AlexejPenner in https://github.com/zenml-io/zenml/pull/470
* Update schedule.py (#485) by @avramdj in https://github.com/zenml-io/zenml/pull/485 

## New Contributors
* @avramdj in https://github.com/zenml-io/zenml/pull/485 

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.6.3...0.7.0rc


# 0.6.3

With ZenML 0.6.3, you can now run your ZenML steps on Sagemaker and AzureML! It's normal to have certain steps that require specific hardware on which to run model training, for example, and this latest release gives you the power to switch out hardware for individual steps to support this.

We added a new Tensorboard visualization that you can make use of when using our Kubeflow Pipelines integration. We handle the background processes needed to spin up this interactive web interface that you can use to visualize your model's performance over time.

Behind the scenes we gave our integration testing suite a massive upgrade, fixed a number of smaller bugs and made documentation updates. For a detailed look at what's changed, give [our full release notes](https://github.com/zenml-io/zenml/releases/tag/0.6.3) a glance.

## What's Changed
* Fix typo by @wjayesh in https://github.com/zenml-io/zenml/pull/432
* Remove tabulate dependency (replaced by rich) by @jwwwb in https://github.com/zenml-io/zenml/pull/436
* Fix potential issue with local integration tests by @schustmi in https://github.com/zenml-io/zenml/pull/428
* Remove support for python 3.6 by @schustmi in https://github.com/zenml-io/zenml/pull/437
* Create clean test repos in separate folders by @michael-zenml in https://github.com/zenml-io/zenml/pull/430
* Copy explicit materializers before modifying, log correct class by @schustmi in https://github.com/zenml-io/zenml/pull/434
* Fix typo in mysql password parameter by @pafpixel in https://github.com/zenml-io/zenml/pull/438
* Pytest-fixture for separate virtual environments for each integration test by @AlexejPenner in https://github.com/zenml-io/zenml/pull/405
* Bugfix/fix failing tests due to comments step by @AlexejPenner in https://github.com/zenml-io/zenml/pull/444
* Added --use-virtualenvs option to allow choosing envs to run by @AlexejPenner in https://github.com/zenml-io/zenml/pull/445
* Log whether a step was cached by @strickvl in https://github.com/zenml-io/zenml/pull/435
* Added basic integration tests for remaining examples by @strickvl in https://github.com/zenml-io/zenml/pull/439
* Improve error message when provisioning local kubeflow resources with a non-local container registry. by @schustmi in https://github.com/zenml-io/zenml/pull/442
* Enable generic step inputs and outputs by @schustmi in https://github.com/zenml-io/zenml/pull/440
* Removed old reference to a step that no longer exists by @AlexejPenner in https://github.com/zenml-io/zenml/pull/452
* Correctly use custom kubernetes context if specified by @schustmi in https://github.com/zenml-io/zenml/pull/451
* Fix CLI stack component describe/list commands by @schustmi in https://github.com/zenml-io/zenml/pull/450
* Ignore type of any tfx proto file by @schustmi in https://github.com/zenml-io/zenml/pull/453
* Another boyscout pr on the gh actions by @AlexejPenner in https://github.com/zenml-io/zenml/pull/455
* Upgrade TFX to 1.6.1 by @jwwwb in https://github.com/zenml-io/zenml/pull/441
* Added ZenML Projects to README by @htahir1 in https://github.com/zenml-io/zenml/pull/457
* Upgrade `rich` from 11.0 to 12.0 by @strickvl in https://github.com/zenml-io/zenml/pull/458
* Add Kubeflow tensorboard viz and fix tensorflow file IO for cloud back-ends by @stefannica in https://github.com/zenml-io/zenml/pull/447
* Implementing the `explain` subcommand by @bcdurak in https://github.com/zenml-io/zenml/pull/460
* Implement AzureML and Sagemaker step operators by @schustmi in https://github.com/zenml-io/zenml/pull/456

## New Contributors
* @pafpixel made their first contribution in https://github.com/zenml-io/zenml/pull/438

# 0.6.2

ZenML 0.6.2 brings you the ability to serve models using MLflow deployments as well as an updated CLI interface! For a real continuous deployment cycle, we know that ZenML pipelines should be able to handle everything — from pre-processing to training to serving to monitoring and then potentially re-training and re-serving. The interfaces we created in this release are the foundation on which all of this will build.

We also improved how you interact with ZenML through the CLI. Everything looks so much smarter and readable now with the popular `rich` library integrated into our dependencies.

Smaller changes that you'll notice include updates to our cloud integrations and bug fixes for Windows users. For a detailed look at what's changed, see below.

## What's Changed

* Updated notebook for quickstart by @htahir1 in https://github.com/zenml-io/zenml/pull/398
* Update tensorflow base image by @schustmi in https://github.com/zenml-io/zenml/pull/396
* Add cloud specific deployment guide + refactoring by @wjayesh in https://github.com/zenml-io/zenml/pull/400
* add cloud sub page to toc.md by @wjayesh in https://github.com/zenml-io/zenml/pull/401
* fix tab indent by @wjayesh in https://github.com/zenml-io/zenml/pull/402
* Bugfix for workflows failing due to modules not being found by @bcdurak in https://github.com/zenml-io/zenml/pull/390
* Improve github workflows by @schustmi in https://github.com/zenml-io/zenml/pull/406
* Add plausible script to docs.zenml.io pages by @alex-zenml in https://github.com/zenml-io/zenml/pull/414
* Add orchestrator and ECR docs by @wjayesh in https://github.com/zenml-io/zenml/pull/413
* Richify the CLI by @alex-zenml in https://github.com/zenml-io/zenml/pull/392
* Allow specification of required integrations for a pipeline by @schustmi in https://github.com/zenml-io/zenml/pull/408
* Update quickstart in docs to conform to examples by @htahir1 in https://github.com/zenml-io/zenml/pull/410
* Updated PR template with some more details by @htahir1 in https://github.com/zenml-io/zenml/pull/411
* Bugfix on the CLI to work without a git installation by @bcdurak in https://github.com/zenml-io/zenml/pull/412
* Added Ayush's Handle by @ayush714 in https://github.com/zenml-io/zenml/pull/417
* Adding an info message on Windows if there is no application associated to .sh files by @bcdurak in https://github.com/zenml-io/zenml/pull/419
* Catch `matplotlib` crash when running IPython in terminal by @strickvl in https://github.com/zenml-io/zenml/pull/416
* Automatically activate integrations when unable to find stack component by @schustmi in https://github.com/zenml-io/zenml/pull/420
* Fix some code inspections by @halvgaard in https://github.com/zenml-io/zenml/pull/422
* Prepare integration tests on kubeflow by @schustmi in https://github.com/zenml-io/zenml/pull/423
* Add concepts back into glossary by @strickvl in https://github.com/zenml-io/zenml/pull/425
* Make guide easier to follow by @wjayesh in https://github.com/zenml-io/zenml/pull/427
* Fix httplib to 0.19 and pyparsing to 2.4 by @jwwwb in https://github.com/zenml-io/zenml/pull/426
* Wrap context serialization in try blocks by @jwwwb in https://github.com/zenml-io/zenml/pull/397
* Track stack configuration when registering and running a pipeline by @schustmi in https://github.com/zenml-io/zenml/pull/429
* MLflow deployment integration by @stefannica in https://github.com/zenml-io/zenml/pull/415

# 0.6.1

ZenML 0.6.1 is out and it's all about the cloud ☁️! We have improved AWS integration and a brand-new [Azure](https://github.com/zenml-io/zenml/tree/0.6.1/src/zenml/integrations/azure) integration! Run your pipelines on AWS and Azure now and let us know how it went on our [Slack](https://zenml.io/slack-invite).

Smaller changes that you'll notice include much-awaited updates and fixes, including the first iterations of scheduling pipelines and tracking more reproducibility-relevant data in the metadata store.

For a detailed look at what's changed, see below.

## What's changed

* Add MVP for scheduling by @htahir1 in https://github.com/zenml-io/zenml/pull/354
* Add S3 artifact store and filesystem by @schustmi in https://github.com/zenml-io/zenml/pull/359
* Update 0.6.0 release notes by @alex-zenml in https://github.com/zenml-io/zenml/pull/362
* Fix cuda-dev base container image by @stefannica in https://github.com/zenml-io/zenml/pull/361
* Mark ZenML as typed package by @schustmi in https://github.com/zenml-io/zenml/pull/360
* Improve error message if ZenML repo is missing inside kubeflow container entrypoint by @schustmi in https://github.com/zenml-io/zenml/pull/363
* Spell whylogs and WhyLabs correctly in our docs by @stefannica in https://github.com/zenml-io/zenml/pull/369
* Feature/add readme for mkdocs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/372
* Cleaning up the assets pushed by gitbook automatically by @bcdurak in https://github.com/zenml-io/zenml/pull/371
* Turn codecov off for patch updates by @htahir1 in https://github.com/zenml-io/zenml/pull/376
* Minor changes and fixes by @schustmi in https://github.com/zenml-io/zenml/pull/365
* Only include python files when building local docs by @schustmi in https://github.com/zenml-io/zenml/pull/377
* Prevent access to repo during step execution by @schustmi in https://github.com/zenml-io/zenml/pull/370
* Removed duplicated Section within docs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/379
* Fixing the materializer registry to spot sub-classes of defined types by @bcdurak in https://github.com/zenml-io/zenml/pull/368
* Computing hash of step and materializer works in notebooks by @htahir1 in https://github.com/zenml-io/zenml/pull/375
* Sort requirements to improve docker build caching by @schustmi in https://github.com/zenml-io/zenml/pull/383
* Make sure the s3 artifact store is registered when the integration is activated by @schustmi in https://github.com/zenml-io/zenml/pull/382
* Make MLflow integration work with kubeflow and scheduled pipelines by @stefannica in https://github.com/zenml-io/zenml/pull/374
* Reset _has_been_called to False ahead of pipeline.connect by @AlexejPenner in https://github.com/zenml-io/zenml/pull/385
* Fix local airflow example by @schustmi in https://github.com/zenml-io/zenml/pull/366
* Improve and extend base materializer error messages by @schustmi in https://github.com/zenml-io/zenml/pull/380
* Windows CI issue by @schustmi in https://github.com/zenml-io/zenml/pull/389
* Add the ability to attach custom properties to the Metadata Store by @bcdurak in https://github.com/zenml-io/zenml/pull/355
* Handle case when return values do not match output by @AlexejPenner in https://github.com/zenml-io/zenml/pull/386
* Quickstart code in docs fixed by @AlexejPenner in https://github.com/zenml-io/zenml/pull/387
* Fix mlflow tracking example by @stefannica in https://github.com/zenml-io/zenml/pull/393
* Implement azure artifact store and fileio plugin by @schustmi in https://github.com/zenml-io/zenml/pull/388
* Create todo issues with separate issue type by @schustmi in https://github.com/zenml-io/zenml/pull/394
* Log that steps are cached while running pipeline by @alex-zenml in https://github.com/zenml-io/zenml/pull/381
* Schedule added to context for all orchestrators by @AlexejPenner in https://github.com/zenml-io/zenml/pull/391

# 0.6.0

ZenML 0.6.0 is out now. We've made some big changes under the hood, but our biggest public-facing addition is our new integration to support all your data logging needs: [`whylogs`](https://github.com/whylabs/whylogs). Our core architecture was [thoroughly reworked](https://github.com/zenml-io/zenml/pull/305) and is now in a much better place to support our ongoing development needs.


Smaller changes that you'll notice include extensive documentation additions, updates and fixes. For a detailed look at what's changed, see below.

## 📊 Whylogs logging

[Whylogs](https://github.com/whylabs/whylogs) is an open source library that analyzes your data and creates statistical summaries called whylogs profiles. Whylogs profiles can be visualized locally or uploaded to the WhyLabs platform where more comprehensive analysis can be carried out.

ZenML integrates seamlessly with Whylogs and [WhyLabs](https://whylabs.ai/). This example shows how easy it is to enhance steps in an existing ML pipeline with Whylogs profiling features. Changes to the user code are minimal while ZenML takes care of all aspects related to Whylogs session initialization, profile serialization, versioning and persistence and even uploading generated profiles to [Whylabs](https://whylabs.ai/).

![Example of the visualizations you can make from Whylogs profiles](https://blog.zenml.io/assets/posts/release_0_6_0/whylogs-visualizer.png)

With our `WhylogsVisualizer`, as described in [the associated example notes](https://github.com/zenml-io/zenml/tree/0.6.0/examples/whylogs), you can visualize Whylogs profiles generated as part of a pipeline.

## ⛩ New Core Architecture

We implemented [some fundamental changes](https://github.com/zenml-io/zenml/pull/305) to the core architecture to solve some of the issues we previously had and provide a more extensible design to support quicker implementations of different stack components and integrations. The main change was to refactor the `Repository`, `Stack` and `StackComponent` architectures. These changes had a pretty wide impact so involved changes in many files throughout the codebase, especially in the CLI which makes calls to all these pieces.

We've already seen how it helps us move faster in building integrations and we hope it helps making contributions as pain-free as possible!

## 🗒 Documentation and Example Updates

As the codebase and functionality of ZenML grows, we always want to make sure our documentation is clear, up-to-date and easy to use. We made a number of changes in this release that will improve your experience in this regard:

- added a number of new explainers on key ZenML concepts and how to use them in your code, notably on [how to create a custom materializer](https://docs.zenml.io/v/0.6.0/guides/index/custom-materializer) and [how to fetch historic pipeline runs](https://docs.zenml.io/v/0.6.0/guides/index/historic-runs) using the `StepContext`
- fixed a number of typos and broken links
- [added versioning](https://github.com/zenml-io/zenml/pull/336) to our API documentation so you can choose to view the reference appropriate to the version that you're using. We now use `mkdocs` for this so you'll notice a slight visual refresh as well.
- added new examples highlighting specific use cases and integrations:
	- how to create a custom materializer ([example](https://github.com/zenml-io/zenml/tree/0.6.0/examples/custom_materializer))
	- how to fetch historical pipeline runs ([example](https://github.com/zenml-io/zenml/tree/0.6.0/examples/fetch_historical_runs))
	- how to use standard interfaces for common ML patterns ([example](https://github.com/zenml-io/zenml/tree/0.6.0/examples/standard_interfaces))
	- `whylogs` logging ([example](https://github.com/zenml-io/zenml/tree/0.6.0/examples/whylogs))

## ➕ Other updates, additions and fixes

As with most releases, we made a number of small but significant fixes and additions. The most import of these were that you can now [access the metadata store](https://github.com/zenml-io/zenml/pull/338) via the step context. This enables a number of new possible workflows and pipeline patterns and we're really excited to have this in the release.

We [added in](https://github.com/zenml-io/zenml/pull/315) a markdown parser for the `zenml example info …` command, so now when you want to use our CLI to learn more about specific examples you will see beautifully parsed text and not markdown markup.

We improved a few of our error messages, too, like for when the return type of a step function [doesn’t match the expected type](https://github.com/zenml-io/zenml/pull/322), or if [step is called twice](https://github.com/zenml-io/zenml/pull/353). We hope this makes ZenML just that little bit easier to use.

# 0.5.7

ZenML 0.5.7 is here  :100:  and it brings not one, but :fire:TWO:fire: brand new integrations :rocket:! ZenML now support [MLFlow](https://www.mlflow.org/docs/latest/tracking.html) for tracking pipelines as experiments and [Evidently](https://github.com/evidentlyai/evidently) for detecting drift in your ML pipelines in production!

## New Features
* Introducing the [MLFlow Tracking](https://www.mlflow.org/docs/latest/tracking.html) Integration, a first step towards 
our complete MLFlow Integration as described in the [#115 poll](https://github.com/zenml-io/zenml/discussions/115). 
Full example found [here](https://github.com/zenml-io/zenml/tree/0.5.7/examples/mlflow).
* Introducing the [Evidently](https://github.com/evidentlyai/evidently) integration. Use the standard 
[Evidently drift detection step](https://github.com/zenml-io/zenml/blob/0.5.7/src/zenml/integrations/evidently/steps/evidently_profile.py) 
to calculate drift automatically in your pipeline. Full example found [here](https://github.com/zenml-io/zenml/tree/0.5.7/examples/drift_detection).

## Bugfixes
* Prevent KFP install timeouts during `stack up` by @stefannica in https://github.com/zenml-io/zenml/pull/299
* Prevent naming parameters same name as inputs/outputs to prevent kwargs-errors by @bcdurak in https://github.com/zenml-io/zenml/pull/300


## What's Changed
* Force pull overwrites local examples without user confirmation by @AlexejPenner in https://github.com/zenml-io/zenml/pull/278
* Updated README with latest features by @htahir1 in https://github.com/zenml-io/zenml/pull/280
* Integration test the examples within ci pipeline by @AlexejPenner in https://github.com/zenml-io/zenml/pull/282
* Add exception for missing system requirements by @kamalesh0406 in https://github.com/zenml-io/zenml/pull/281
* Examples are automatically pulled if not present before any example command is run by @AlexejPenner in https://github.com/zenml-io/zenml/pull/279
* Add pipeline error for passing the same step object twice by @kamalesh0406 in https://github.com/zenml-io/zenml/pull/283
* Create pytest fixture to use a temporary zenml repo in tests by @htahir1 in https://github.com/zenml-io/zenml/pull/287
* Additional example run implementations for standard interfaces, functional and class based api by @AlexejPenner in https://github.com/zenml-io/zenml/pull/286
* Make pull_request.yaml actually use os.runner instead of ubuntu by @htahir1 in https://github.com/zenml-io/zenml/pull/288
* In pytest return to previous workdir before tearing down tmp_dir fixture by @AlexejPenner in https://github.com/zenml-io/zenml/pull/289
* Don't raise an exception during integration installation if system requirement is not installed by @schustmi in https://github.com/zenml-io/zenml/pull/291
* Update starting page for the API docs by @alex-zenml in https://github.com/zenml-io/zenml/pull/294
* Add `stack up` failure prompts by @alex-zenml in https://github.com/zenml-io/zenml/pull/290
* Spelling fixes by @alex-zenml in https://github.com/zenml-io/zenml/pull/295
* Remove instructions to git init from docs by @bcdurak in https://github.com/zenml-io/zenml/pull/293
* Fix the `stack up` and `orchestrator up` failure prompts by @stefannica in https://github.com/zenml-io/zenml/pull/297
* Prevent KFP install timeouts during `stack up` by @stefannica in https://github.com/zenml-io/zenml/pull/299
* Add stefannica to list of internal github users by @stefannica in https://github.com/zenml-io/zenml/pull/303
* Improve KFP UI daemon error messages by @schustmi in https://github.com/zenml-io/zenml/pull/292
* Replaced old diagrams with new ones in the docs by @AlexejPenner in https://github.com/zenml-io/zenml/pull/306
* Fix broken links & text formatting in docs by @alex-zenml in https://github.com/zenml-io/zenml/pull/302
* Run KFP container as local user/group if local by @stefannica in https://github.com/zenml-io/zenml/pull/304
* Add james to github team by @jwwwb in https://github.com/zenml-io/zenml/pull/308
* Implement integration of mlflow tracking by @AlexejPenner in https://github.com/zenml-io/zenml/pull/301
* Bugfix integration tests on windows by @jwwwb in https://github.com/zenml-io/zenml/pull/296
* Prevent naming parameters same name as inputs/outputs to prevent kwargs-errors by @bcdurak in https://github.com/zenml-io/zenml/pull/300
* Add tests for `fileio` by @alex-zenml in https://github.com/zenml-io/zenml/pull/298
* Evidently integration (standard steps and example) by @alex-zenml in https://github.com/zenml-io/zenml/pull/307
* Implemented evidently integration by @stefannica in https://github.com/zenml-io/zenml/pull/310
* Make mlflow example faster by @AlexejPenner in https://github.com/zenml-io/zenml/pull/312

## New Contributors
* @kamalesh0406 made their first contribution in https://github.com/zenml-io/zenml/pull/281
* @stefannica made their first contribution in https://github.com/zenml-io/zenml/pull/297
* @jwwwb made their first contribution in https://github.com/zenml-io/zenml/pull/308


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.5.6...0.5.7
# 0.5.6

        )                    *      (     
     ( /(                  (  `     )\ )  
     )\())    (            )\))(   (()/(  
    ((_)\    ))\    (     ((_)()\   /(_)) 
     _((_)  /((_)   )\ )  (_()((_) (_))   
    |_  /  (_))    _(_/(  |  \/  | | |    
     / /   / -_)  | ' \)) | |\/| | | |__  
    /___|  \___|  |_||_|  |_|  |_| |____| 

This release fixes some known bugs from previous releases and especially 0.5.5. Therefore, upgrading to 0.5.6 is a **breaking change**. You must do the following in order to proceed with this version:

```
cd zenml_enabled_repo
rm -rf .zen/
```

And then start again with ZenML init:

```
pip install --upgrade zenml
zenml init
```

## New Features
* Added `zenml example run [EXAMPLE_RUN_NAME]` feature: The ability to run an example with one command. In order to run this, do `zenml example pull` first and see all examples available by running `zenml example list`.
* Added ability to specify a `.dockerignore` file before running pipelines on Kubeflow.
* Kubeflow Orchestrator is now leaner and faster. 
* Added the `describe` command group to the CLI for groups `stack`, `orchestrator`, `artifact-store`, and `metadata-store`. E.g. `zenml stack describe`

## Bug fixes and minor improvements
* Adding `StepContext` to a branch now invalidates caching by default. Disable explicitly with `enable_cache=True`.
* Docs updated to reflect minor changes in CLI commands.
* CLI `list` commands now mentions active component. Try `zenml stack list` to check this out.
* `zenml version` now has cooler art.

## What's Changed
* Delete blog reference from release notes by @alex-zenml in https://github.com/zenml-io/zenml/pull/228
* Docs updates by @alex-zenml in https://github.com/zenml-io/zenml/pull/229
* Update kubeflow guide by @schustmi in https://github.com/zenml-io/zenml/pull/230
* Updated quickstart to reflect newest zenml version by @alexej-zenml in https://github.com/zenml-io/zenml/pull/231
* Add KFP GCP example readme by @schustmi in https://github.com/zenml-io/zenml/pull/233
* Baris/update docs with class api by @bcdurak in https://github.com/zenml-io/zenml/pull/232
* fixing a small typo [ci skip] by @bcdurak in https://github.com/zenml-io/zenml/pull/236
* Hamza/docs last min updates by @htahir1 in https://github.com/zenml-io/zenml/pull/234
* fix broken links by @alex-zenml in https://github.com/zenml-io/zenml/pull/237
* added one more page for standardized artifacts [ci skip] by @bcdurak in https://github.com/zenml-io/zenml/pull/238
* Unified use of cli_utils.print_table for all table format cli printouts by @AlexejPenner in https://github.com/zenml-io/zenml/pull/240
* Remove unused tfx kubeflow code by @schustmi in https://github.com/zenml-io/zenml/pull/239
* Relaxed typing requirements for cli_utils.print_table by @AlexejPenner in https://github.com/zenml-io/zenml/pull/241
* Pass input artifact types to kubeflow container entrypoint by @schustmi in https://github.com/zenml-io/zenml/pull/242
* Catch duplicate run name error and throw custom exception by @schustmi in https://github.com/zenml-io/zenml/pull/243
* Improved logs by @htahir1 in https://github.com/zenml-io/zenml/pull/244
* CLI active component highlighting by @alex-zenml in https://github.com/zenml-io/zenml/pull/245
* Baris/eng 244 clean up by @bcdurak in https://github.com/zenml-io/zenml/pull/246
* CLI describe command by @alex-zenml in https://github.com/zenml-io/zenml/pull/248
* Alexej/eng 35 run examples from cli by @AlexejPenner in https://github.com/zenml-io/zenml/pull/253
* CLI argument and option flag consistency improvements by @alex-zenml in https://github.com/zenml-io/zenml/pull/250
* Invalidate caching when a step requires a step context by @schustmi in https://github.com/zenml-io/zenml/pull/252
* Implement better error messages for custom step output artifact types by @schustmi in https://github.com/zenml-io/zenml/pull/254
* Small improvements by @schustmi in https://github.com/zenml-io/zenml/pull/251
* Kubeflow dockerignore by @schustmi in https://github.com/zenml-io/zenml/pull/249
* Rename container registry folder to be consistent with the other stack components by @schustmi in https://github.com/zenml-io/zenml/pull/257
* Update todo script by @schustmi in https://github.com/zenml-io/zenml/pull/256
* Update docs following CLI change by @alex-zenml in https://github.com/zenml-io/zenml/pull/255
* Bump mypy version by @schustmi in https://github.com/zenml-io/zenml/pull/258
* Kubeflow Windows daemon alternative by @schustmi in https://github.com/zenml-io/zenml/pull/259
* Run pre commit in local environment by @schustmi in https://github.com/zenml-io/zenml/pull/260
* Hamza/eng 269 move beam out by @htahir1 in https://github.com/zenml-io/zenml/pull/262
* Update docs by @alex-zenml in https://github.com/zenml-io/zenml/pull/261
* Hamza/update readme with contribitions by @htahir1 in https://github.com/zenml-io/zenml/pull/271
* Hamza/eng 256 backoff analytics by @htahir1 in https://github.com/zenml-io/zenml/pull/270
* Add spellcheck by @alex-zenml in https://github.com/zenml-io/zenml/pull/264
* Using the pipeline run name to explicitly access when explaining the … by @AlexejPenner in https://github.com/zenml-io/zenml/pull/263
* Import user main module in kubeflow entrypoint to make sure all components are registered by @schustmi in https://github.com/zenml-io/zenml/pull/273
* Fix cli version command by @schustmi in https://github.com/zenml-io/zenml/pull/272
* User is informed of version mismatch and example pull defaults to cod… by @AlexejPenner in https://github.com/zenml-io/zenml/pull/274
* Hamza/eng 274 telemetry by @htahir1 in https://github.com/zenml-io/zenml/pull/275
* Update docs with right commands and events by @htahir1 in https://github.com/zenml-io/zenml/pull/276
* Fixed type annotation for some python versions by @AlexejPenner in https://github.com/zenml-io/zenml/pull/277

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.5.5...0.5.6

# 0.5.5

ZenML 0.5.5 is jam-packed with new features to take your ML pipelines to the next level. Our three biggest new features: Kubeflow Pipelines, CLI support for our integrations and Standard Interfaces. That’s right, Standard Interfaces are back!

## What's Changed
* Implement base component tests by @schustmi in https://github.com/zenml-io/zenml/pull/211
* Add chapter names by @alex-zenml in https://github.com/zenml-io/zenml/pull/212
* Fix docstring error by @alex-zenml in https://github.com/zenml-io/zenml/pull/213
* Hamza/add caching example by @htahir1 in https://github.com/zenml-io/zenml/pull/214
* Update readme by @alex-zenml in https://github.com/zenml-io/zenml/pull/216
* Hamza/add small utils by @htahir1 in https://github.com/zenml-io/zenml/pull/219
* Update docs by @alex-zenml in https://github.com/zenml-io/zenml/pull/220
* Docs fixes by @alex-zenml in https://github.com/zenml-io/zenml/pull/222
* Baris/eng 182 standard interfaces by @bcdurak in https://github.com/zenml-io/zenml/pull/209
* Fix naming error by @alex-zenml in https://github.com/zenml-io/zenml/pull/221
* Remove framework design by @alex-zenml in https://github.com/zenml-io/zenml/pull/224
* Alexej/eng 234 zenml integration install by @alexej-zenml in https://github.com/zenml-io/zenml/pull/223
* Fix deployment section order by @alex-zenml in https://github.com/zenml-io/zenml/pull/225
* the readme of the example by @bcdurak in https://github.com/zenml-io/zenml/pull/227
* Kubeflow integration by @schustmi in https://github.com/zenml-io/zenml/pull/226

## New Contributors
* @alexej-zenml made their first contribution in https://github.com/zenml-io/zenml/pull/223

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.5.4...0.5.5

# 0.5.4

0.5.4 adds a [lineage tracking](https://github.com/zenml-io/zenml/tree/main/examples/lineage) integration to visualize lineage of pipeline runs! It also includes numerous bug fixes and optimizations.

## What's Changed
* Fix typos by @alex-zenml in https://github.com/zenml-io/zenml/pull/192
* Fix Apache Beam bug by @alex-zenml in https://github.com/zenml-io/zenml/pull/194
* Fix apache beam logging bug by @alex-zenml in https://github.com/zenml-io/zenml/pull/195
* Add step context by @schustmi in https://github.com/zenml-io/zenml/pull/196
* Init docstrings by @alex-zenml in https://github.com/zenml-io/zenml/pull/197
* Hamza/small fixes by @htahir1 in https://github.com/zenml-io/zenml/pull/199
* Fix writing to metadata store with airflow orchestrator by @schustmi in https://github.com/zenml-io/zenml/pull/198
* Use pipeline parameter name as step name in post execution by @schustmi in https://github.com/zenml-io/zenml/pull/200
* Add error message when step name is not in metadata store by @schustmi in https://github.com/zenml-io/zenml/pull/201
* Add option to set repo location using an environment variable by @schustmi in https://github.com/zenml-io/zenml/pull/202
* Run cloudbuild after pypi publish by @schustmi in https://github.com/zenml-io/zenml/pull/203
* Refactor component generation by @schustmi in https://github.com/zenml-io/zenml/pull/204
* Removed unnecessary panel dependency by @htahir1 in https://github.com/zenml-io/zenml/pull/206
* Updated README to successively install requirements by @AlexejPenner in https://github.com/zenml-io/zenml/pull/205
* Store active stack in local config by @schustmi in https://github.com/zenml-io/zenml/pull/208
* Hamza/eng 125 lineage tracking vis by @htahir1 in https://github.com/zenml-io/zenml/pull/207

## New Contributors
* @AlexejPenner made their first contribution in https://github.com/zenml-io/zenml/pull/205

**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.5.3...0.5.4

# 0.5.3

Version 0.5.3 adds [statistics visualizations](https://github.com/zenml-io/zenml/blob/main/examples/visualizers/statistics/README.md), greatly improved speed for CLI commands as well as lots of small improvements to the pipeline and step interface. 

## What's Changed
* Make tests run in a random order by @alex-zenml in https://github.com/zenml-io/zenml/pull/160
* Connect steps using *args by @schustmi in https://github.com/zenml-io/zenml/pull/162
* Move location of repobeats image by @alex-zenml in https://github.com/zenml-io/zenml/pull/163
* Hamza/add sam by @htahir1 in https://github.com/zenml-io/zenml/pull/165
* Pipeline initialization with *args by @schustmi in https://github.com/zenml-io/zenml/pull/164
* Improve detection of third party modules during class resolving by @schustmi in https://github.com/zenml-io/zenml/pull/167
* Merge path_utils into fileio & refactor what was left by @alex-zenml in https://github.com/zenml-io/zenml/pull/168
* Update docker files by @schustmi in https://github.com/zenml-io/zenml/pull/169
* Hamza/deploy api reference by @htahir1 in https://github.com/zenml-io/zenml/pull/171
* API Reference by @schustmi in https://github.com/zenml-io/zenml/pull/172
* Add color back into our github actions by @alex-zenml in https://github.com/zenml-io/zenml/pull/176
* Refactor tests not raising by @alex-zenml in https://github.com/zenml-io/zenml/pull/177
* Improve step and pipeline interface by @schustmi in https://github.com/zenml-io/zenml/pull/175
* Alex/eng 27 windows bug again by @htahir1 in https://github.com/zenml-io/zenml/pull/178
* Automated todo tracking by @schustmi in https://github.com/zenml-io/zenml/pull/173
* Fix mypy issues related to windows by @schustmi in https://github.com/zenml-io/zenml/pull/179
* Include Github URL to TODO comment in issue by @schustmi in https://github.com/zenml-io/zenml/pull/181
* Create Visualizers logic by @htahir1 in https://github.com/zenml-io/zenml/pull/182
* Add README for visualizers examples by @alex-zenml in https://github.com/zenml-io/zenml/pull/184
* Allow None as default value for BaseStep configs by @schustmi in https://github.com/zenml-io/zenml/pull/185
* Baris/eng 37 standard import check by @bcdurak in https://github.com/zenml-io/zenml/pull/183
* Replace duplicated code by call to source_utils.resolve_class by @schustmi in https://github.com/zenml-io/zenml/pull/186
* Remove unused base enum cases by @schustmi in https://github.com/zenml-io/zenml/pull/187
* Testing mocks for CLI `examples` command by @alex-zenml in https://github.com/zenml-io/zenml/pull/180
* Set the correct module for steps created using our decorator by @schustmi in https://github.com/zenml-io/zenml/pull/188
* Fix some cli commands by @schustmi in https://github.com/zenml-io/zenml/pull/189
* Tag jira issues for which the todo was deleted by @schustmi in https://github.com/zenml-io/zenml/pull/190
* Remove deadlinks by @alex-zenml in https://github.com/zenml-io/zenml/pull/191


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.5.2...0.5.3

# 0.5.2

0.5.2 brings an improved post-execution workflow and lots of minor changes and upgrades for the developer experience when 
creating pipelines. It also improves the Airflow orchestrator logic to accommodate for more real world scenarios. 

## What's Changed
* Fix autocomplete for step and pipeline decorated functions by @schustmi in https://github.com/zenml-io/zenml/pull/144
* Add reference docs for CLI example functionality by @alex-zenml in https://github.com/zenml-io/zenml/pull/145
* Fix mypy integration by @schustmi in https://github.com/zenml-io/zenml/pull/147
* Improve Post-Execution Workflow by @schustmi in https://github.com/zenml-io/zenml/pull/146
* Fix CLI examples bug by @alex-zenml in https://github.com/zenml-io/zenml/pull/148
* Update quickstart example notebook by @alex-zenml in https://github.com/zenml-io/zenml/pull/150
* Add documentation images by @alex-zenml in https://github.com/zenml-io/zenml/pull/151
* Add prettierignore to gitignore by @alex-zenml in https://github.com/zenml-io/zenml/pull/154
* Airflow orchestrator improvements by @schustmi in https://github.com/zenml-io/zenml/pull/153
* Google colab added by @htahir1 in https://github.com/zenml-io/zenml/pull/155
* Tests for `core` and `cli` modules by @alex-zenml in https://github.com/zenml-io/zenml/pull/149
* Add Paperspace environment check by @alex-zenml in https://github.com/zenml-io/zenml/pull/156
* Step caching by @schustmi in https://github.com/zenml-io/zenml/pull/157
* Add documentation for pipeline step parameter and run name configuration by @schustmi in https://github.com/zenml-io/zenml/pull/158
* Automatically disable caching if the step function code has changed by @schustmi in https://github.com/zenml-io/zenml/pull/159


**Full Changelog**: https://github.com/zenml-io/zenml/compare/0.5.1...0.5.2

# 0.5.1
0.5.1 builds on top of Slack of the 0.5.0 release with quick bug updates.


## Overview

* Pipeline can now be run via a YAML file. #132
* CLI now let's you pull directly from GitHub examples folder. :fire: Amazing @alex-zenml with #141!
* ZenML now has full [mypy](http://mypy-lang.org/) compliance. :tada: Thanks @schustmi for #140!
* Numerous bugs and performance improvements. #136, @bcdurak great job with #142
* Added new docs with a low level API guide. #143

[Our roadmap](https://zenml.hellonext.co/roadmap) goes into further detail on the timeline. Vote on the [next features now](https://github.com/zenml-io/zenml/discussions).

We encourage every user (old or new) to start afresh with this release. Please go over our latest [docs](https://docs.zenml.io) and [examples](examples) to get a hang of the new system.


# 0.5.0
This long-awaited ZenML release marks a seminal moment in the project's history. We present to you a complete 
revamp of the internals of ZenML, with a fresh new design and API. While these changes are significant, and have been months 
in the making, the original vision of ZenML has not wavered. We hope that the ZenML community finds the new 
design choices easier to grasp and use, and we welcome feedback on the [issues board](https://github.com/zenml-io/zenml/issues).

## Warning
0.5.0 is a complete API change from the previous versions of ZenML, and is a *breaking* upgrade. Fundamental 
concepts have been changed, and therefore backwards compatibility is not maintained. Please use only this version 
with fresh projects.

With such significant changes, we expect this release to also be breaking. Please report any bugs in the issue board, and 
they should be addressed in upcoming releases.

## Overview

* Introducing a new functional API for creating pipelines and steps. This is now the default mechanism for building ZenML pipelines. [read more](https://docs.zenml.io/starter-guide/pipelines/pipelines)
* Steps now use Materializers to handle artifact serialization/deserialization between steps. This is a powerful change, and will be expanded upon in the future. [read more](https://docs.zenml.io/pipelines/materializers)
* Introducing the new `Stack` paradigm: Easily transition from one MLOps stack to the next with a few CLI commands [read more](https://docs.zenml.io/starter-guide/stacks/stacks)
* Introducing a new `Artifact`, `Typing`, and `Annotation` system, with `pydantic` (and `dataclasses`) support [read more](https://docs.zenml.io/getting-started/core-concepts)
* Deprecating the `pipelines_dir`: Now individual pipelines will be stored in their metadata stores, making the metadata store a single source of truth. [read more](https://docs.zenml.io/getting-started/core-concepts)
* Deprecating the YAML config file: ZenML no longer natively compiles to an intermediate YAML-based representation. Instead, it compiles and deploys directly into the selected orchestrator's 
representation. While we do plan to support running pipelines directly through YAML in the future, it will no longer be
the default route through which pipelines are run. [read more about orchestrators here](https://docs.zenml.io/component-gallery/orchestrators/orchestrators)

## Technical Improvements
* A completely new system design, please refer to the [docs](https://docs.zenml.io/getting-started/core-concepts).
* Better type hints and docstrings.
* Auto-completion support.
* Numerous performance improvements and bug fixes, including a smaller dependency footprint.

## What to expect in the next weeks and the new ZenML
Currently, this release is bare bones. We are missing some basic features which used to be part of ZenML 0.3.8 (the previous release):

* Standard interfaces for `TrainingPipeline`.
* Individual step interfaces like `PreprocessorStep`, `TrainerStep`, `DeployerStep` etc. need to be rewritten from within the new paradigm. They should
be included in the non-RC version of this release.
* A proper production setup with an orchestrator like Airflow.
* A post-execution workflow to analyze and inspect pipeline runs.
* The concept of `Backends` will evolve into a simple mechanism of transitioning individual steps into different runners.
* Support for `KubernetesOrchestrator`, `KubeflowOrchestrator`, `GCPOrchestrator` and `AWSOrchestrator` are also planned.
* Dependency management including Docker support is planned.

[Our roadmap](https://zenml.hellonext.co/roadmap) goes into further detail on the timeline.

We encourage every user (old or new) to start afresh with this release. Please go over our latest [docs](https://docs.zenml.io) 
and [examples](examples) to get a hang of the new system.

Onwards and upwards to 1.0.0!

# 0.5.0rc2
This long-awaited ZenML release marks a seminal moment in the project's history. We present to you a complete 
revamp of the internals of ZenML, with a fresh new design and API. While these changes are significant, and have been months 
in the making, the original vision of ZenML has not wavered. We hope that the ZenML community finds the new 
design choices easier to grasp and use, and we welcome feedback on the [issues board](https://github.com/zenml-io/zenml/issues).

## Warning
0.5.0rc0 is a complete API change from the previous versions of ZenML, and is a *breaking* upgrade. Fundamental 
concepts have been changed, and therefore backwards compatibility is not maintained. Please use only this version 
with fresh projects.

With such significant changes, we expect this release to also be breaking. Please report any bugs in the issue board, and 
they should be addressed in upcoming releases.

## Overview

* Introducing a new functional API for creating pipelines and steps. This is now the default mechanism for building ZenML pipelines. [read more](https://docs.zenml.io/starter-guide/pipelines/pipelines)
* Introducing the new `Stack` paradigm: Easily transition from one MLOps stack to the next with a few CLI commands [read more](https://docs.zenml.io/starter-guide/stacks/stacks)
* Introducing a new `Artifact`, `Typing`, and `Annotation` system, with `pydantic` (and `dataclasses`) support [read more](https://docs.zenml.io/getting-started/core-concepts)
* Deprecating the `pipelines_dir`: Now individual pipelines will be stored in their metadata stores, making the metadata store a single source of truth. [read more](https://docs.zenml.io/starter-guide/stacks/stacks)
* Deprecating the YAML config file: ZenML no longer natively compiles to an intermediate YAML-based representation. Instead, it compiles and deploys directly into the selected orchestrator's 
representation. While we do plan to support running pipelines directly through YAML in the future, it will no longer be
the default route through which pipelines are run. [read more about orchestrators here](https://docs.zenml.io/core/stacks)

## Technical Improvements
* A completely new system design, please refer to the [docs](https://docs.zenml.io/component-gallery/orchestrators/orchestrators).
* Better type hints and docstrings.
* Auto-completion support.
* Numerous performance improvements and bug fixes, including a smaller dependency footprint.

## What to expect in the next weeks and the new ZenML
Currently, this release is bare bones. We are missing some basic features which used to be part of ZenML 0.3.8 (the previous release):

* Standard interfaces for `TrainingPipeline`.
* Individual step interfaces like `PreprocessorStep`, `TrainerStep`, `DeployerStep` etc. need to be rewritten from within the new paradigm. They should
be included in the non-RC version of this release.
* A proper production setup with an orchestrator like Airflow.
* A post-execution workflow to analyze and inspect pipeline runs.
* The concept of `Backends` will evolve into a simple mechanism of transitioning individual steps into different runners.
* Support for `KubernetesOrchestrator`, `KubeflowOrchestrator`, `GCPOrchestrator` and `AWSOrchestrator` are also planned.
* Dependency management including Docker support is planned.

[Our roadmap](https://zenml.hellonext.co/roadmap) goes into further detail on the timeline.

We encourage every user (old or new) to start afresh with this release. Please go over our latest [docs](https://docs.zenml.io) 
and [examples](examples) to get a hang of the new system.

Onwards and upwards to 1.0.0!

# 0.3.7.1
This release fixes some known bugs from previous releases and especially 0.3.7. Same procedure as always, please delete existing pipelines, metadata, and artifact stores.

```
cd zenml_enabled_repo
rm -rf pipelines/
rm -rf .zenml/
```

And then another ZenML init:

```
pip install --upgrade zenml
cd zenml_enabled_repo
zenml init
```

## New Features
* Introduced new `zenml example` CLI sub-group: Easily pull examples via zenml to check it out.

```bash
zenml example pull # pulls all examples in `zenml_examples` directory
zenml example pull EXAMPLE_NAME  # pulls specific example
zenml example info EXAMPLE_NAME  # gives quick info regarding example
```  
Thanks Michael Xu for the suggestion!

* Updated examples with new `zenml examples` paradigm for examples.

## Bug Fixes + Refactor

* ZenML now works on Windows -> Thank you @Franky007Bond for the heads up.
* Updated numerous bugs in examples directory. Also updated README's.
* Fixed remote orchestration logic -> Now remote orchestration works.
* Changed datasource `to_config` to include reference to backend, metadata, and artifact store.


# 0.3.7
0.3.7 is a much-needed, long-awaited, big refactor of the Datasources paradigm of ZenML. There are also bug fixes, improvements, and more!

For those upgrading from an older version of ZenML, we ask to please delete their old `pipelines` dir and `.zenml` folders and start afresh with a `zenml init`.

If only working locally, this is as simple as:

```
cd zenml_enabled_repo
rm -rf pipelines/
rm -rf .zenml/
```

And then another ZenML init:

```
pip install --upgrade zenml
cd zenml_enabled_repo
zenml init
```

## New Features
* The inner-workings of the `BaseDatasource` have been modified along with the concrete implementations. Now, there is no relation between a `DataStep` and a `Datasource`: A `Datasource` holds all the logic to version and track itself via the new `commit` paradigm.

* Introduced a new interface for datasources, the `process` method which is responsible for ingesting data and writing to TFRecords to be consumed by later steps.

* Datasource versions (snapshots) can be accessed directly via the `commits` paradigm: Every commit is a new version of data.

* Added `JSONDatasource` and `TFRecordsDatasource`.

## Bug Fixes + Refactor
A big thanks to our new contributor @aak7912 for the help in this release with issue #71 and PR #75.

* Added an example for [regression](https://github.com/zenml-io/zenml/tree/main/examples/regression).
* `compare_training_runs()` now takes an optional `datasource` parameter to filter by datasource.
* `Trainer` interface refined to focus on `run_fn` rather than other helper functions.
* New docs released with a streamlined vision and coherent storyline: https://docs.zenml.io
* Got rid of unnecessary Torch dependency with base ZenML version.


# 0.3.6
0.3.6 is a more inwards-facing release as part of a bigger effort to create a more flexible ZenML. As a first step, ZenML now supports arbitrary splits for all components natively, freeing us from the `train/eval` split paradigm. Here is an overview of changes:

## New Features
* The inner-workings of the `BaseTrainerStep`, `BaseEvaluatorStep` and the `BasePreprocessorStep` have been modified along with their respective components to work with the new split_mapping. Now, users can define arbitrary splits (not just train/eval). E.g. Doing a `train/eval/test` split is possible.

* Within the instance of a `TrainerStep`, the user has access to `input_patterns` and `output_patterns` which provide the required uris with respect to their splits for the input and output(test_results) examples.

* The built-in trainers are modified to work with the new changes.

## Bug Fixes + Refactor
A big thanks to our new super supporter @zyfzjsc988 for most of the feedback that led to bug fixes and enhancements for this release: 

* #63: Now one can specify which ports ZenML opens its add-on applications.
* #64 Now there is a way to list integrations with the following code:
```
from zenml.utils.requirements_utils import list_integrations.
list_integrations()
```
* Fixed #61: `view_anomalies()` breaking in the quickstart.
* Analytics is now `opt-in` by default, to get rid of the unnecessary prompt at `zenml init`. Users can still freely `opt-out` by using the CLI:

```
zenml config analytics opt-out
```

Again, the telemetry data is fully anonymized and just used to improve the product. Read more [here](https://docs.zenml.io/misc/usage-analytics)

# 0.3.5

## New Features
* Added a new interface into the trainer step called [`test_fn`]() which is utilized to produce model predictions and save them as test results

* Implemented a new evaluator step called [`AgnosticEvaluator`]() which is designed to work regardless of the model type as long as you run the `test_fn` in your trainer step

* The first two changes allow torch trainer steps to be followed by an agnostic evaluator step, see the example [here]().

* Proposed a new naming scheme, which is now integrated into the built-in steps, in order to make it easier to handle feature/label names

* Implemented a new adapted version of 2 TFX components, namely the [`Trainer`]() and the [`Evaluator`]() to allow the aforementioned changes to take place

* Modified the [`TorchFeedForwardTrainer`]() to showcase how to use TensorBoard in conjunction with PyTorch


## Bug Fixes + Refactor
* Refactored how ZenML treats relative imports for custom steps. Now:
```python

```

* Updated the [Scikit Example](https://github.com/zenml-io/zenml/tree/main/examples/scikit), [PyTorch Lightning Example](https://github.com/zenml-io/zenml/tree/main/examples/pytorch_lightning), [GAN Example](https://github.com/zenml-io/zenml/tree/main/examples/gan) accordingly. Now they should work according to their README's.

Big shout out to @SarahKing92 in issue #34 for raising the above issues!


# 0.3.4
This release is a big design change and refactor. It involves a significant change in the Configuration file structure, meaning this is a **breaking upgrade**. 
For those upgrading from an older version of ZenML, we ask to please delete their old `pipelines` dir and `.zenml` folders and start afresh with a `zenml init`.

If only working locally, this is as simple as:

```
cd zenml_enabled_repo
rm -rf pipelines/
rm -rf .zenml/
```

And then another ZenML init:

```
pip install --upgrade zenml
cd zenml_enabled_repo
zenml init
```

## New Features
* Introduced another higher-level pipeline: The [NLPPipeline](https://github.com/zenml-io/zenml/blob/main/zenml/pipelines/nlp_pipeline.py). This is a generic 
  NLP pipeline for a text-datasource based training task. Full example of how to use the NLPPipeline can be found [here](https://github.com/zenml-io/zenml/tree/main/examples/nlp)
* Introduced a [BaseTokenizerStep](https://github.com/zenml-io/zenml/blob/main/zenml/steps/tokenizer/base_tokenizer.py) as a simple mechanism to define how to train and encode using any generic 
tokenizer (again for NLP-based tasks).

## Bug Fixes + Refactor
* Significant change to imports: Now imports are way simpler and user-friendly. E.g. Instead of:
```python
from zenml.core.pipelines.training_pipeline import TrainingPipeline
```

A user can simple do:

```python
from zenml.pipelines import TrainingPipeline
```

The caveat is of course that this might involve a re-write of older ZenML code imports.

Note: Future releases are also expected to be breaking. Until announced, please expect that upgrading ZenML versions may cause older-ZenML 
generated pipelines to behave unexpectedly. 
