# Week 2: Orchestration

## Mage

[Mage Zoomcamp repo](https://github.com/mage-ai/mage-zoomcamp)

To connect the docker-spun postgres DB in the tutorial (DEV env):
```sehll
pgcli -h localhost -p 5432 -u postgres -d postgres
```

To verify that the data has been loaded, connect to the database and then run:
```shell
SELECT * FROM ny_taxi.yellow_cab_data LIMIT 10;
```

### Adding the GCP SA Key:
Add the .json file containg the JSON SA key


## Deployment

The repo below contains all terraform code to deploy Mage to various cloud providers
[Templates for TF](https://github.com/mage-ai/mage-ai-terraform-templates)

In our case for GCP, please follow instructions [here](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)







