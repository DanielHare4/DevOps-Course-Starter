terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 4.19.0"
    }
  }
  backend "azurerm" {
        resource_group_name  = "cohort32-33_DanHar_ProjectExercise"
        storage_account_name = "danharstorageaccount"
        container_name       = "danharcontainer"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name     = "cohort32-33_DanHar_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-terraformed-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name     = "danielharedevops/todo-app:latest"
      docker_registry_url   = "https://index.docker.io"
    }
  }

  app_settings = {
    FLASK_APP = "todo_app/app"
    FLASK_DEBUG = "false"
    MONGODB_COLLECTION_NAME = "todo_app_items"
    MONGODB_CONNECTION_STRING = azurerm_cosmosdb_account.main.primary_mongodb_connection_string
    MONGODB_DB_NAME = "todo_app_db"
    SECRET_KEY = "secret-key"
    WEBSITES_PORT = "5000"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                  = "${var.prefix}-terraformed-cosmos-db"
  location              = data.azurerm_resource_group.main.location
  resource_group_name   = data.azurerm_resource_group.main.name
  offer_type            = "Standard"
  kind                  = "MongoDB"
  mongo_server_version  = "6.0"

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level = "Eventual"
  }

  geo_location {
    location = "uksouth"
    failover_priority = 0
  }

  # lifecycle {
  #   prevent_destroy = true
  # }
}