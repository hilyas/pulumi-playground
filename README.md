# GCP Infrastructure Deployment with Pulumi

This project deploys a Google Cloud Platform (GCP) infrastructure using Pulumi. Current infrastructure includes: storage buckets, compute instances, and a Kubernetes cluster.

## Prerequisites

- Python: Make sure you have Python 3.6 or higher installed on your machine.
- Pulumi: Install Pulumi by following the instructions on the Pulumi website.
- Google Cloud SDK: Install the Google Cloud SDK by following the instructions here.
- GCP Account: Make sure you have a GCP account and have created a project. Note the project_id as you will need it later.
- Service Account: Create a service account in GCP and download the JSON key file. This service account should have sufficient permissions to create resources in your GCP project.

## Configuration

Set up the Google Cloud SDK: Authenticate your account and set the project by running:

```bash
gcloud auth login
gcloud config set project <your-project-id>
```

Configure Pulumi to use GCP: Run `pulumi config set gcp:project <your-project-id>` to set your GCP project ID.

Set Environment Variable: Export the `GOOGLE_PROJECT_ID` and `GOOGLE_APPLICATION_CREDENTIALS` environment variables by adding the following lines to your `.bashrc` or `.bash_profile` (or any other relevant shell configuration file):

```bash
export GOOGLE_PROJECT_ID="<your-project-id>"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```

Source your shell configuration file to update the environment variables:

```bash
source ~/.bashrc
```

Install Required Python Packages: Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

## Deployment

Initialize a New Stack: Initialize a new Pulumi stack (ex. dev) by running:

```bash
pulumi stack init dev
```

Deploy the Infrastructure: Deploy the infrastructure by running:

```bash
pulumi up
```

Review the changes and select yes to create the resources. The state is saved to the Pulumi cloud by default. The prompt will link to the process.

## Cleanup

To delete the resources created by Pulumi, run:

```bash
pulumi destroy
```

Review the changes and select yes to delete the resources.
