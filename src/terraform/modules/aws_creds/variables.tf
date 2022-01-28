variable "login_approle_role_id" {
  description = "role id for vault approle to generate aws creds"
  type        = string
  sensitive   = true
}
variable "login_approle_secret_id" {
  description = "secret id for vault approle to generate aws creds"
  type        = string
  sensitive   = true
}
variable "vault_addr" {
  description = "address of vault instance"
  type        = string
  sensitive   = true
}
variable "vault_namespace" {
  description = "vault namespace"
  default     = "admin"
  type        = string
}
variable "environment" {
  description = "the name of your environment, e.g. \"dev\""
  default     = "dev"
  type        = string
}
