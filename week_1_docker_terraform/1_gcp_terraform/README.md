# Terraform and GCP

## Terraform

[Video source](https://www.youtube.com/watch?v=Hajwnmj0xfQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=6)

Terraform is an infrastructure as code tool that allows us to provision infrastructure resources as code, thus making it possible to handle infrastructure as an additional software component and take advantage of tools such as version control. 
It also allows us to bypass the cloud vendor GUIs.

You can browse your provider's (eg: GCP in our case) registry:
https://registry.terraform.io/providers/hashicorp/google/latest

### Key Commands

```commandline
init          Prepare your working directory for other commands
validate      Check whether the configuration is valid
plan          Show changes required by the current configuration
apply         Create or update infrastructure
destroy       Destroy previously-created infrastructure
```

```terraform fmt``` is a neat way to format your .tf files

Registry resources config

- [Storage Bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket)

- [BQ Dataset](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset)

## GCP

https://registry.terraform.io/providers/hashicorp/google/latest/docs
