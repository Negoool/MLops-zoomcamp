# Experiment tracking:
## WHY:
 1. Imagine in a meeting, you have reported some metrics for a project to your team. After sometime, you want to train your model again. Only you noticed that you are not able to  reproduce the results. what has changed? was it another set of parameters? has any of your teammates changed the code? well **reporducibility** matters a lot. I guess anyone in an iterative project (which happens in ML) without any experiment tracking way has faced with reproducibility issue.

 2. If you are in  a team, it is nice to have a **centralized** place for runs and others can  see the results of runs. It boosts **collaboration**

 3. It is nice to be able to compare diferrent runs together, expecially in hyperparameter search, where you can see the effect of each parameter. 

 Naive way: 
    Spreadsheet. and its problems are  ...

Better way:
    Mlflow. 
    

### what should be tracked for an experiment (minimum)?
    - source code  (version of the code)
    - data 
    - hyperparameter
    - enviroment
    - metrics
    - model

you can use mlflow to log parameters, metrics, artifacts, models, tags and mlflow itself will save commit id, source script and some more. 
A little bit of mlflow concepts, _experiment_ is an experminet for example hyper-parameter-taxi-newyork and you can have different _runs_ (e.g.  trying different HP) under one experiment.


 # Model managements:
 ## WHY?
The model is named as "classifier_final" which is obviously never a final one. The next model is named as "really_final", which of course, it never is. It is nice to have versions.
well! naming folders can work to some extend, model_v1, model_v2. BTW what is different between model_v1 and model_v2? ( no model lineage for this approach)


You can use model registery. when you are happy with the models, you can promote them and register them. You can put them in different stages. (stage, production or archive) and move from one stage to another. As you register more model, the version automaticallly gets incremented (versioning). For each registered model the run id is there, which shows you all the information saved during expriment tracking (lineage). 

You can register models through UI or using the mlflow client. For example as in the homework, you can run a hyperparameter tunning, get the n top model (based on your performance metric) and register them through mlflow client. Later you can compare these models more, for example based on run time, change its stage to production.


### Mlflow configuration
- Backend store: For saving metric, parameters and metadata fo runs.
    - local filesystem
    -  SQLAlchemy compatible database (eg SQLit)
- Artifact store
    - local filesystem
    - remote (eg S3)
You can using no tracking server, a local tracking server, or a remote one.

which to choose? depends on the scenario. For example 
- If you are competing in a kaggle competition and you just want to track experminets, Backend store: local filesystem, Artifact store: local filesystem and no tracking server would be enough.
- If you are a team of data scientists and sw, Backend store: postgres, Artifact store: google cloud server, tracking server: a gcp.


###  !
Tool is not the answer. **Needs** for a spacific project matters most. So first identify those needs in a project and then looks whether there is sth out there that can address those needs.

### What is there in the code folder?
- `preprocess.py` data
- `train.py` with autologging, In a general setting you have to call mlflow.log... . But for some of the libraries, like sklearn, mlflow offer autologging. 
- `hpo.py` Huperparameter tunning using hyperopt while traking runs using mlflow.
- `register_model.py` use mlflowclient to search runs in an experiment that fit the specified criteria and sort them. here get the top 5 models based on validation metric and register the best one.


cool to search trough runs programatically, makes it automatic.
runs can get clutter, It can be beneficial to add tags for runs, later you can filter the results based on that.
you can also add text descrioption to your registered model, through ui or programatically.
one bad thing about mlflow, it can not track uncommited changes. so remember to commit before running experiments. otherwise the commit id does not match the code you used for running experiments.