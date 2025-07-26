library(europepmc)
# install.packages("devtools")
devtools::install_github("cran/crminer")
library(crminer)
devtools::install_github("serghiou/metareadr")
library(metareadr)
library(dplyr)



tte_epmc_search = epmc_search(query = '"target trial emulation"',
                              verbose = F,
                              limit = 10000)

write.csv(tte_epmc_search, "~/Documents/Github/TTEdb/dataset/tte_epmc_search.csv", row.names = F)

tte_epmc_search$pmcid_ = gsub("PMC", "", as.character(tte_epmc_search$pmcid))

tte_epmc_search_oa = tte_epmc_search %>%
  filter(isOpenAccess == "Y")

sapply(tte_epmc_search_oa$pmcid_, metareadr::mt_read_pmcoa)

metareadr::mt_read_pmcoa(pmcid = tte_epmc_search_oa$pmcid_,
                         file_name = "~/Documents/Github/TTEdb/dataset/tte_xmls/")








