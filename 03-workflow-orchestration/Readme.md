## Motivation 
Imagin every week more data is added. Run the jub on the weekly manner, train new model (maybe as mentioned in mlflow lesson, do a little bit of hyperparameter tunning and select the best model and register that.) compute the performance of the new model and compare it with the model which is currently in production. if its performance is better, mlflow will promote the new model to production and archive the model which was in production before. We want to automate  this process on a weekly manner with workflow management tool.

## Overview
workflow orchestration should not only run a pipeline on a schedule, but it should also handles errors gracefully. ( lot of work is spent on handling errors, something called negative engineering and prefect reduces negative engineering by automatic retrying, providing observibility, conditional failure)

prefect 2.0 (orion):
- Dag free
- like pyhton coding
- (If you add type hints to yout flow or task, and they do not coarsed, you'll see an error.)

## Steps 
1. code wise
- Have modular codes.
- Decorate your pipeline with `@flow`
- Decorate your components with `@task`. (it is not necessary for all the steps or functions to be decorated with task). The task will be monitored by prefect and its logges will be shown in the dashboard. you can configure your task like `@task(retries=3)` or  use caching.
- you can set the task runner as well. ConcurrentTaskRunner or SequentialTaskRunner: `@flow(task_runner=SequentialTaskRunner())`

To run the ui (server), in the terminal `prefect orion start`.
(There was no server running up when flow was running.  when ui is up, prefect update its state to the API and you can see in the dashboard.)



2. **Deployment** (The idea of workflow managment is to set up a flow in a scheduled time.)
To do so:
- set up a prefect orion server (you just need to setup your instance firewall rules and run prefect orion start --host 0.0.0.0, also you need to set one env). alternatively you can use their managed service (prefect cloud)
- On a VM or locally (where ever you want to run the flow, your  agent),  configure the Prefect API url. You can now as before run the flow and see the results in the server.
- **Storage**: place to store your flow. when the flow is executed it pulls the flow from that storage and then execute that. So define a storage, you can use S3, localfile system, ...
- Write prefect deploymentspec, what is the _flow_, what is the _schedule_, tags.
- create deployment by running `prefect deployment create <python script>`. (This is one way, another way  will be explained later.) 

-> so we scheuled the flow.

- now we should define where to run it? **agents** and **work queues**. create a work queue from the server for your deployments (you  can mention deployment name or tags or runner spec). it will gives a workqueue id and by `prefect work-queue preview/inspect <id>` you can see  all the schedule runs (queue). now attach a work agent to the queue `prefect agent start <deployment id>` in where ever you want to run the flow.

-> The agent will check the queue from server, pull the flow instruction from storage (wherever it is) and run it. (if you wanted to run it from docker, the agent is responsible for spinning up a docker container.)


-> so the prefect does not provide the compute resources.

You  can have multiple work queues, for examples some task should be run on gpu (so there would be a work queue 1, and gpu agents will pull runs from  that and another queue for cpu tasks and cpu agents will read from that.)



## Summary
These  are the  concepts:
- flow and  task (in a DAG like format), you can specify the runner for the flow (concurrent, sequential)
- storage
- scheduling (interval, corn)
- Infrustructre block (whether local process, docker, kubernetese is used to run  the flow.)
- Deployment
- orchestrate (agents  and queue)


A _deployment_ is a server-side concept that encapsulates a flow, allowing it to be scheduled and triggered via API.

For creating deployment:
1.  CLI command: Run the `prefect deployment build `  with deployment options to create a deployment.yaml deployment definition file, then run `prefect deployment apply` to create a deployment on the API using the settings in deployment.yaml.
2. Define a Deployment Python object, specifying the deployment options as properties of the object, then building and applying the object using methods of Deployment.

for creating deployment, you should mention  _flow_, _schedule_, _storage_ (the flow will be uploaded to storage) , _infra_


The server create some work queues based on schedules and agents listen to that and pull runs.

### usefull commands:
`prefect config view`
running the code locally, working directory was /private/var/folders/14/78kcjhx901j_7fpqftm57rym0000gn/T/tmp1_xmznexprefect

# Alternatives:
- corn: simple solution, can  run  jobs on a specified time. can not handle dependencies netween  tasks or orchestration though. It has some expression  to write the schedules.
- general software schedulers: Slurm (not sure how it is different than data science workflow orchestrarion tools)
- data science spicific ones: Airflow, Kubeflow, Metaflow, Prefect,  ...
