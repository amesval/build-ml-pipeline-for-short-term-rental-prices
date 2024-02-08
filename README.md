# Build an ML Pipeline for Short-Term Rental Prices in NYC
Imagine that you are working for a property management company renting rooms and properties for short periods of time on various rental platforms. You need to estimate the typical price for a given property based on the price of similar properties. Your company receives new data in bulk every week. The model needs to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

In this project we will build such a pipeline.

## Setup

1. Clone repository:
```
git clone https://github.com/amesval/build-ml-pipeline-for-short-term-rental-prices.git
```

2. Move to root folder of the project.

3. Create conda environment:
```
conda env create -f environment.yml
```

4. Change to conda environment:
```
conda activate nyc_airbnb_dev
```

5. Get your API key from W&B (https://docs.wandb.ai/quickstart).

6. Run next instruction in the command line:
```
wandb login <API_KEY>
```

7. You should see a message similar to:
```
wandb: Appending key for api.wandb.ai to your netrc file: /home/[your username]/.netrc
```

Note: Your experiments and artifacts are going to be registered in your W&B account.

## ML Pipeline
The current pipeline consists of the following steps:

1) Download data
2) Data cleaning
3) Data testing
4) Data splitting
5) Train Random Forest model
6) Test model

## Config
The config.yaml file contains the parameters to run the entire pipeline. Take a look to get familiar with the hyperparameter configuration.

## Run specific steps

To run specific steps, you could use the *steps* argument. The command to enter for each step are as follow:

| Pipeline step | command |
| ------- | ----------- |
| Download data | download |
| Data cleaning | basic_cleaning |
| Data testing | data_check |
| Data splitting | data_split |
| Train Random Forest model | train_random_forest |
| Test model | test_regression_model |

For example, to train a new model, you can just run:
```
mlflow run . -P steps="train_random_forest" -P hydra_options="modeling.max_tfidf_features=10"
```

If you want to run two steps, you can simply separate each step by a comma:
```
mlflow run . -P steps="download, basic_cleaning"
```

To run with multiple parameters, you can add *-m* at the end of *hydra_options*:
```
mlflow run . -P steps="train_random_forest" -P hydra_options="modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1.0 -m"
```

Previous instruction is useful to perform hyperparameter optimization.

If you want to run the pipeline for the first time, follow the instructions in the next section.

## 1st run of the pipeline

Run download, and data cleaning steps:
```
mlflow run . -P steps="download, basic_cleaning"
```

Go to the artifacts section in your W&B project, and add the *reference* alias to the *clean_data.csv* artifact. This promotes your data as a reference. Next, perform a unit testing step for our data:
```
mlflow run . -P steps="data_check"
```

After verifying that the data pass all the examples, we can split the data and train our model:
```
mlflow run . -P steps="data_split, train_random_forest"
```

Once we trained model, we need to promote the best model into production. Add a *prod* alias to the *model_export* artifact.

## Test model

After running hyperparameter configuration, you need to deploy the best model. This can be done from the W&B interface: just add a *prod* alias to the best model. The *prod* model is called by our pipeline to test with new data.

For testing, just write:
```
mlflow run . -P steps="test_regression_model"
```





## Run entire pipeline

After running the pipeline for the first time, you can run the entire cycle at once from the command line:

```
mlflow run .
```

To run the pipeline with a different configuration you can manually modify the config.yaml file. Another alternative is to overwrite your current configuration by using  *hydra_options* argument. For example, let's run the pipeline and
train a model with a different value of *tfidf_features*:

```
mlflow run . -P hydra_options="modeling.max_tfidf_features=10"
```


## Project artifacts

Artifacts can be access from the W&B project. You can review an example for this project here: https://wandb.ai/amesval-91/nyc_airbnb/. The artifacts are generated from this GitHub repository: https://github.com/amesval/build-ml-pipeline-for-short-term-rental-prices

## License

[License](LICENSE.txt)