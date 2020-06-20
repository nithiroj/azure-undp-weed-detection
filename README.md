# Azure UNDP Weed Detection

## Datasets

Data being used in this project is [V2: Nonsegmented single plants (1.7GB)](https://vision.eng.au.dk/?download=/data/WeedData/NonsegmentedV2.zip) from [PAPER: A Public Image Database for Benchmark of Plant Seedling Classification Algorithms](http://arxiv.org/abs/1711.05458).

It contains about 960 unique plants of 12 classes:

```
└── NonsegmentedV2
    ├── Black-grass
    ├── Charlock
    ├── Cleavers
    ├── Common Chickweed
    ├── Common wheat
    ├── Fat Hen
    ├── Loose Silky-bent
    ├── Maize
    ├── Scentless Mayweed
    ├── Shepherd’s Purse
    ├── Small-flowered Cranesbill
    └── Sugar beet
```
More information can be found from [Plant Seedlings Dataset](https://vision.eng.au.dk/plant-seedlings-dataset/).

## Training Weed Detection Model
The details can be found in `notebooks/UNDP.ipynb` and can be run with Colab.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nithiroj/azure-undp-weed-detection/blob/master/notebooks/UNDP.ipynb)


## Azure Architectures

### Azure Functions


### Azure Notification Hubs


Requirements:
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Docker](https://www.docker.com/)
- [Microsoft Azure Account](https://azure.microsoft.com/en-us/)
- [Docker Hub Account](https://hub.docker.com/)
### Azure Notification Hub Setup
1. Configure Azure Notification Hub and connect app to the notification hub. (See [Tutorial: Send push notifications to Android devices using Firebase SDK version 0.6](https://docs.microsoft.com/en-us/azure/notification-hubs/notification-hubs-android-push-notification-google-fcm-get-started)).
2. Replace `<ConnectionString>` and `<HubName>` in `undp/classify/__init__.py` with `DefaultFullSharedAccessSignature` and name of the hub you have configured.
### Docker Setup
cr. [fastai](https://course.fast.ai/deployment_azure_functions.html#2---docker-setup)
1. Open your terminal and change directory to `undp`
2. Build Docker image 
    > docker build --tag <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG> .
3. Test Docker image
    > docker run -p 8080:80 -it <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG>
4. Open browser:
    > localhost:8080/api/classify?name=https://raw.githubusercontent.com/nithiroj/azure-undp-weed-detection/master/assets/maize-251.png
5. Push the image to Docker Hub
    > docker login
    >
    >docker push <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG>

### Azure Functions Setup
cr. [fastai](https://course.fast.ai/deployment_azure_functions.html#3---azure-setup)
1. Login to Microsoft Azure with Azure CLI
    > az login
2. Run following command to see list of available location for `<LOCATION_ID>`, e.g. `centralus`.
3. Create resource group
    > az group create \\\
--name <RESOURCE_GROUP> \\\
--location <LOCATION_ID>
4. Create storage account
    > az storage account create \\\
--name <STORAGE_ACCOUNT> \\\
--location <LOCATION_ID> \\\
--resource-group <RESOURCE_GROUP> \\\
--sku Standard_LRS
5. Create a Linux App Service Plan
    > az appservice plan create \\\
--name <APP_PLAN_NAME> \\\
--resource-group <RESOURCE_GROUP> \\\
--sku B1 \\\
--is-linux
6. Create the App & Deploy the Docker image from Docker Hub
    > az functionapp create \\\
--resource-group <RESOURCE_GROUP> \\\
--name <FUNCTION_APP> \\\
--storage-account  <STORAGE_ACCOUNT> \\\
--plan <APP_PLAN_NAME> \\\
--deployment-container-image-name <DOCKER_HUB_ID>/<DOCKER_IMAGE_NAME>:<TAG>
7. Configure the function app
    > storageConnectionString=$(az storage account show-connection-string \\\
--resource-group <RESOURCE_GROUP> \\\
--name <STORAGE_ACCOUNT> \\\
--query connectionString --output tsv)
    > az functionapp config appsettings set --name <FUNCTION_APP> \\\
--resource-group <RESOURCE_GROUP> \\\
--settings AzureWebJobsDashboard=$storageConnectionString \\\
AzureWebJobsStorage=$storageConnectionString
8. Run your Azure Function
    > https://<FUNCTION_APP>.azurewebsites.net/api/classify?name=<IMAGE_URL>

### Delete Resource Group
When you are done, delete the resource group

> az group delete \\\
--name <RESOURCE_GROUP> \\\
--yes

## Demo
The demo can be tested by replacing `<IMAGE_URL>` with your image url.

```
https://undpinferenceapp.azurewebsites.net/api/classify?name=<IMAGE_URL>
```

For example:

https://undpinferenceapp.azurewebsites.net/api/classify?name=https://raw.githubusercontent.com/nithiroj/azure-undp-weed-detection/master/assets/maize-251.png

Note:
- More samples of images are avilable in `assets/`
- The demo will be available until the end of June 2020.



