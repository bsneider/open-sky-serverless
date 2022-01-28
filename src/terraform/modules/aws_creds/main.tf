terraform {
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "2.21.0"
    }
  }
}

provider "vault" {
  # Configuration options
  address   = var.vault_addr
  namespace = var.vault_namespace
  auth_login {
    path      = "auth/approle/login"
    namespace = var.vault_namespace
    parameters = {
      role_id   = "${var.login_approle_role_id}"
      secret_id = "${var.login_approle_secret_id}"
    }
  }
}

data "vault_aws_access_credentials" "creds" {
  type    = "sts"
  backend = "aws"
  role    = "OrganizationAccountAccessRole"
}