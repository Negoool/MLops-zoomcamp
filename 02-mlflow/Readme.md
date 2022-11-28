# Experiment tracking:
## WHY:
 1. Imagine in a meeting, you have reported some metrics for a project to your team. After sometime, you want to train your model again. Only you noticed that you are not able to reproduce the metrics you reported. what has changed? was it another set of parameters? has any of your teammates changed the code? well **reporducibility** matters a lot. I guess anyone in an iterative project (which happens in ML) without any experiment tracking way has faced with reproducibility issue.

 2. If you are in  a team, it is nice to have a **centralized** place for runs and others can  see the results of runs. It boosts **collaboration**

 3. It is nice to be able to **compare runs** together, expecially in hyperparameter search, where you can see the effect of each parameter. 

 Naive way: 
    Spreadsheet. and its obviouse problems are  ...

Better way:
    Mlflow. Experiment tracking
    

### what should be tracked for an experiment (minimum)?
    - version of the code (code commit)
    - data 
    - hyperparameter
    - enviroment
    - metrics
    - model

you can use mlflow to log parameters, metrics, artifacts, models, tags and mlflow automatically will save commit id, source script and some more. 
A little bit of mlflow concepts, _experiment_ is an experminet for example hyper-parameter-taxi-newyork and you can have different _runs_ (e.g.  trying different HP) under one experiment.
the default expermein has the id of 0 and as you creat more experiments, their id gets incremeted.


 # Model managements:
 ## WHY?
The model is named as "classifier_final" which is obviously never a final one. The next model is named as "really_final", which of course, it never is. It is nice to have versions.
well! naming folders can work to some extend, model_v1, model_v2. But what is difference between model_v1 and model_v2? (folder naming does not have any model lineage.)

Better way:
    Mlflow. Model registery


When you are happy with the models, you can register them. You can put them in different stages. (stage, production or archive) and move from one stage to another. As you register more model, the version automaticallly gets incremented (versioning). For each registered model the run id is there, which shows you all the information saved during expriment tracking (lineage). 

You can register models through UI or using the mlflow python APIs. For example as in the homework, you can run a hyperparameter tunning, get the n top model (based on your performance metric) and register them through mlflow client. Later you can compare these models more, for example based on run time, change its stage to production.


# Mlflow configuration
- Backend store: For saving metric, parameters and metadata fo runs.
    - local filesystem
    -  SQLAlchemy compatible database (eg SQLit)
- Artifact store
    - local filesystem
    - remote (eg S3)
- You can using no tracking server, a local tracking server, or a remote one.

which to choose? depends on the scenario. For example 
- If you are competing in a kaggle competition and you just want to track experminets, Backend store: local filesystem, Artifact store: local filesystem and no tracking server would be enough.
- If you are a team of data scientists and sw, Backend store: postgres, Artifact store: google cloud server, tracking server: a gcp.



# Homework
Before running the code, set up the mlflow server `mlflow server --backend-store-uri sqlite:///bk.db --default-artifact-root ./artifacts`

- `preprocess.py` data
- `train.py` with autologging, In a general setting you have to manually call mlflow.log... . But for some of the libraries, like sklearn, mlflow supports autologging. 
- `hpo.py` Hyperparameter tunning using hyperopt and traking multiple runs using mlflow.
- `register_model.py`  search runs in an experiment that fit the specified criteria and sort them. here get the top 5 models based on validation metric and register the best one.



Mlflow has multiple python APIs, https://www.mlflow.org/docs/latest/python_api/index.html.
**mlflow** is the high level one for starting and managing MLflow runs.
here is an example:

```import mlflow

with mlflow.start_run() as run:
    mlflow.log_param("p", 0)

run_id = run.info.run_id
print("run_id: {}; lifecycle_stage: {}".format(run_id,
    mlflow.get_run(run_id).info.lifecycle_stage))
```

You can have multiple runs in a script, starting and ending. Even you can have nested runs (not sure where it is useful, I guess it gives some kind of hirerarchy).
```import mlflow

_Create nested runs_
experiment_id = mlflow.create_experiment("experiment1")
with mlflow.start_run(
    run_name="PARENT_RUN",
    experiment_id=experiment_id,
    tags={"version": "v1", "priority": "P1"},
    description="parent",
) as parent_run:
    mlflow.log_param("parent", "yes")
    with mlflow.start_run(
        run_name="CHILD_RUN",
        experiment_id=experiment_id,
        description="child",
        nested=True,
    ) as child_run:
        mlflow.log_param("child", "yes")

print("parent run:")

print("run_id: {}".format(parent_run.info.run_id))
_Search all child runs with a parent id_
query = "tags.mlflow.parentRunId = '{}'".format(parent_run.info.run_id)
results = mlflow.search_runs(experiment_ids=[experiment_id], filter_string=query)
print("child runs:")
```

**mlflowclient**
Is a low level API and Client of an MLflow Tracking Server that creates and manages experiments and runs, and of an MLflow Registry Server that creates and manages registered models and model versions.

## Notes

cool to search through runs in python script, makes it automatic.

runs can get clutter, It can be beneficial to add tags for runs, later you can filter the results based on that.

It can be beneficial to add text descrioption to your registered model, through ui or programatically.

one bad thing about mlflow, it can not track uncommited changes. so remember to commit before running experiments. otherwise the commit id does not match the code you used for running  experiments. Also out of the box, it does not track data (there are some workaround for that).

Mlflow has some pther components, like project which I do not know what it does at this time.

Tool is not the answer. **Needs** for a spacific project matters most. So first identify those needs in a project and then looks whether there is sth out there that can address those needs.

Interested to see and example including deployment.

