1. Setting up a virtial machine and an enviroment with python (condo), docker, docker-compose.


2. Playground example. Estimate the taxi ride time. 
There is a similar Kaggle competetion  [https://www.kaggle.com/competitions/nyc-taxi-trip-duration/overview](New York City Taxi Trip Duration) based on latitude and longitude
    - How to handle **categorical features**. Specifically for:
        - If we are going to have unseen values during production.
        - If onehot encoding leads to a very sparce feature vector.
        - If there is a relationship between features and we might want to use that.

    - Will feature crossing help the model?
    - If there is a realtionship between zones and there closeness, is it beneficial to make the features integer instead of string?
    - For the time of the hour, we can use descritization (or leave it alone.)
