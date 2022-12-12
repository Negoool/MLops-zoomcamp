# Deployment

There are diffrenet ways to deploy a model, based on problem.
1. **batch**: run prediction periodically, like churn prediction or netflix movie recommendation. (predict if user is likely to leave the service, send the result to marketing to offer them incentives or predict the movie that the users like, save the result and when the user loggs in, fetch the results.)
2. **Online**: like google translate or ride price predicion.
    a. **web services** (the client waits for the server to get the response from)
    b. **streaming** (client does not wait for the answer, there is no explicit connection between client and server, example is content moderation, a user upload a vedio and we want to see if it satisfies the copy right, unti violence, ... ). the app backend (aka producer) will create events stream and there are multiple consumer (services) that use that event stream to make prediction. and they sent their prediction somewhere.

**My confusion**: 
somewhere else I read there are 3 ways to deploy, 1.batch prediction which uses batch featuers, 2.online prediction which uses batch features and 3.online prediction that uses batch and stream featuers. and the same place mentioned for stream features, if we have lot of microservecies that want to share the data, we do not want to wirte and read to/from databases and the flow of the data should be in memory through a broker (pubsub). this way the flow of data is event-based rather than request base. it is going to be asynchronus. like message queue and I am wondering if the communication of data is asynchronous can it be an online (realtime) system?

anyway, it seems both of these definitions are leading to pubsub and kinesis.

Motivation of pubsub is not obviouse, is it for:
- processing of stream features?
- share of data between services?
- move to asynchronouse option? if can not process on time?

## Notes
**4.2 web service (deploying with Flask and docker)**
- Create enviroment using **pipenv**
- Create a Flask app, the endpoint will wrap the predict function. you can test it with _requests_ library.
- will get a warning about this is development enviroment, do not use for prod. to solve the warning , instead ofrunning `python <script>`, run `gunicorn --bind=0.0.0.0:port <script>:<flask_app name>`
- package the app in Docker. Again he used pipenv in the docker and used the pipfile and pipfile.lock for installing the requirements.
>- Now you can deploy on kubernetese or serverless. [here](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/05-deployment) module 5, 9, 10

**4.3 web service, getting the model from model registery**
We want to use the model in MLflow model registery, by stage or by run_id.
as mentioned in model part, mlflow.pyfunc.load_model or if it an artifact mlflowclient.download_artifact. Either case you have to set the mlflow_tracking_uri. 
problem? if server is down, we can not load the models. solution ... Download directly from S3 bucket.
The above part was not done in docker. ( when later they want to use model in dockermlflow.pyfunc.load_model load the model directly without downloading)
Another point is the model version or run_id can be set as an enviroment variabe.

**4.4 streaming with Kinesis and Lambda**
for deployig the model they use Lambda (serverless) and connect it to input and output Kinesis for stream of data.
- The code for deployment, start with script and later a docker image with was pushed to Elastic container registeru (ECR)
- Configurations for _roles_ and _policies_.
- Lambda support Test stage or using aws Commandline you can put an example in the input pipeline.

**4.5 and 4.6 Batch deployment and scheduling the job with prefec**
- create a unique id, using uuid, the same if not more necessary for stream prediction.
- modular and parametrize
- create a flow with paramterse, you can pass patameters in creating deployment. datetime is the one that if is not provided, it will use the context date.
- Now, if we want to backfill (run the flow for previous months), we can create a flow which in a loop calls previouse flow (now it is subflow)
- The subflow will run and you can see in the prefect ui
- Something intresting the min flow, is also appear in the ui. but I do not know how prefect knows about it?!!! 
