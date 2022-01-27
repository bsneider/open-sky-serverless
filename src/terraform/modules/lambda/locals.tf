#--- lambda_module/locals --- 

locals {

  source_files = [
    "${path.module}/external/scrape.py",
    "${path.module}/external/load.py",
    "${path.module}/external/report.py",
    "${path.module}/external/create_table.sql",
  ]
}
