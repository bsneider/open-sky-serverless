#--- lambda_module/locals --- 

locals {

  source_files = [
    "${path.module}/external/scraper.py",
    "${path.module}/external/load.py",
    "${path.module}/external/report.py",
  ]
}
