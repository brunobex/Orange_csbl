library(ggplot2)
library("devtools")
library("data.table")

# library("glue")


pdf(NULL)

args <- commandArgs(TRUE)

name <- args[1]
token <- args[2]
expressed <- args[3]
variant <- args[4]
location <- args[5]

name 
token 
expressed 
variant
location

token_paste <- paste0(token, ".Rmd")
token_paste_out <- paste0(token, ".html")
local_name <- paste0(location, name)

folder_rmd <- paste0("",location, token_paste)
folder_html_save <- paste0("/opt/lampp/htdocs/www/", token, ".html")
folder_pdf_save <- paste0("/opt/lampp/htdocs/www/", token, ".pdf")

folder_html <- paste0("",location, "results.html")

raiz_html <- paste0("/opt/lampp/htdocs/www/", token_paste_out )



loexpres <- args[2]





df2 <- fread(name, data.table = FALSE)
rownames(df2) <- df2[,1]
df2[,1] <- NULL



# df2 <- read.delim(file = name, header=TRUE,quote = "", row.names = 1)

variance_df2 <- apply(df2,1,var)
mean_df2 <- apply(df2, 1, mean)
df <- head(df2[,1:4])

x <- mean_df2
y <- variance_df2

mean_t <- mean(x)
mean_var <- mean(y)

comb <- data.frame(express_mean = x, variance_mean = y)
comb_ori <- comb

# percent_var = 100
# toorder <- order(comb$express_mean)
# comb <- comb[toorder[percent_var:nrow(comb)],]
# 
# maxx <- length(rownames(comb))
# toorder.y <- order(comb$variance_mean)
# comb <- comb[toorder.y,]
# 
#  min_ex <- comb[1,1]
#  max_ex <- comb[nrow(name),1]
#  outlier_var <- 2
# 
# comb$varY <- ifelse(comb$variance_mean > outlier_var, NA, comb$variance_mean)
# 
# outlier_exp_min <- 7
# outlier_exp_max <- 12
# 
# comb$varX <- ifelse(comb$express_mean > outlier_exp_max | comb$express_mean < outlier_exp_min, NA, comb$express_mean)
# 
# comb_out<<- comb


library(DT)
teste <- datatable(comb_ori)
name
head(comb_ori)


rmarkdown::render("results.Rmd",output_file = folder_html_save , params = list(
  name_saved = name))

# my.file.rename <- function(from, to) {
#   todir <- dirname(to)
#   if (!isTRUE(file.info(todir)$isdir)) dir.create(todir, recursive=TRUE)
#   file.rename(from = from,  to = to)
# }
# 
# my.file.rename(from = raiz_html, to = folder_html)


# Rscript -e "rmarkdown::render('test.Rmd',output_file='test.html')" --args --title=my.title --author=me




