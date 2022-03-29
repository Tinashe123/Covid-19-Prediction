RSA Covid 19 and Excess Fatality Exploratory Data Analysis
================
Graeme Lubbe
2022-03-29

## Set-up and reading data

Here the global environment is cleared, the necessary packages are
loaded and the working directory is set. Additionally, the data used in
this analysis is read.

``` r
rm(list = ls())

#required libraries
library(dplyr)
library(readr)
library(lubridate)
library(tidyr)
library(ggplot2)
library(broom)
library(purrr)

## Setting the working directory
setwd("C:/Users/User/Documents/University/Masters/2nd Year/MIT808/Project")

## Reading in excess dates data from obtained from https://www.samrc.ac.za/reports/report-weekly-deaths-south-africa
excess_deaths <- read.csv("./data/ExcessDeaths.csv", stringsAsFactors = F, sep = ";")

## reading cumulative deaths
cumtive_deaths <- read.csv("./data/covid19za_provincial_cumulative_timeline_deaths.csv", stringsAsFactors = F)
```

## Cleaning Fatality Data

Next the date variables are changed to date objects and column names for
the two fatality data sets are changed to match each other. The data
frame shape of the two are adjusted to match eachother to allow the
combination of the two frames. An indicator for the week and year is
created, as the excess mortality is only reported on a weekly basis, and
this will allow for direct comparison. Next an indicator is created to
distinguish excess mortality numbers from reported covid 19 fatalities.
Finaly the two data frame are combined

    ##         date year epi_week EC FS GP KZN LP MP NC NW WC RSA       indicator
    ## 1 2020-03-27 2020       13  0  0  0   0  0  0  0  0  1   1 Covid 19 Deaths
    ## 2 2020-03-28 2020       13  0  0  0   1  0  0  0  0  0   1 Covid 19 Deaths
    ## 3 2020-03-30 2020       14  0  1  0   0  0  0  0  0  0   1 Covid 19 Deaths
    ## 4 2020-03-31 2020       14  0  0  1   1  0  0  0  0  0   2 Covid 19 Deaths
    ## 5 2020-04-03 2020       14  0  0  0   4  0  0  0  0  0   4 Covid 19 Deaths
    ## 6 2020-04-05 2020       15  0  0  0   1  0  0  0  0  1   2 Covid 19 Deaths

## Analysis of Excess Mortality

First the weekly total covid related fatalities and excess mortalities
are plotted over time per province and for South Africa.

``` r
## Plot the excess mortality and actual deaths per week over time to compare trends
combined_df %>% 
  group_by(epi_week, year, indicator) %>% 
  summarise(date = min(date),
            across(.cols = EC:RSA, ~sum(., na.rm = T))) %>% 
  pivot_longer(cols = EC:RSA, names_to = "Province", values_to = "Deaths") %>% 
  ggplot(aes(x = date, y = Deaths, colour = indicator))+
  geom_line()+
  facet_wrap(.~Province, scales = "free_y")+ theme(axis.text.x = element_text(angle = 90))
```

![](ExcessDeathsEDA_files/figure-gfm/time%20plot-1.png)<!-- -->

And then the two are plotted against each other.

``` r
## Plot correlation between the two
combined_df %>% 
  group_by(epi_week, year, indicator) %>% 
  summarise(date = min(date),
            across(.cols = EC:RSA, ~sum(., na.rm = T))) %>% 
  pivot_longer(cols = EC:RSA, names_to = "Province", values_to = "Deaths") %>% 
  pivot_wider(names_from = indicator, values_from = Deaths) %>% 
  ggplot(aes(x = `Covid 19 Deaths`, y = `Excess Deaths`))+
  geom_point(shape = 1)+
  facet_wrap(.~Province, scales = "free")+
  geom_smooth(method = "lm", se = F, colour = "black")
```

![](ExcessDeathsEDA_files/figure-gfm/versus-1.png)<!-- -->

And finally, a nested regression is performed per province and for the
entire country to determine the strength of the correlation and the
degree of under reporting. A good correlation shows that the covid 19
fatalities corrlates well with excess fatalities, while a higher
estimate indicates either inaccurate death predictions, or under
reporting of covid 19 related fatalities.

``` r
lin_reg <- combined_df %>% 
  group_by(epi_week, year, indicator) %>% 
  summarise(date = min(date),
            across(.cols = EC:RSA, ~sum(., na.rm = T))) %>% 
  pivot_longer(cols = EC:RSA, names_to = "Province", values_to = "Deaths") %>% 
  pivot_wider(names_from = indicator, values_from = Deaths) %>% 
  ungroup() %>%
  select(-c(epi_week, year)) %>% 
  group_by(Province) %>% 
  drop_na() %>% 
  nest() %>% 
  mutate(
    fit = map(data, ~ lm(`Covid 19 Deaths` ~ `Excess Deaths` - 1, data = .x)),
    tidied = map(fit, tidy),
    glanced = map(fit, glance)
  ) 
```

``` r
lin_reg %>% 
  unnest(glanced) %>% 
  select(Province, r.squared)
```

    ## # A tibble: 10 x 2
    ## # Groups:   Province [10]
    ##    Province r.squared
    ##    <chr>        <dbl>
    ##  1 EC          0.806 
    ##  2 FS          0.641 
    ##  3 GP          0.835 
    ##  4 KZN         0.769 
    ##  5 LP          0.586 
    ##  6 MP          0.0415
    ##  7 NC          0.382 
    ##  8 NW          0.634 
    ##  9 WC          0.934 
    ## 10 RSA         0.888

``` r
lin_reg %>% 
  unnest(tidied) %>% 
  select(-c(data, fit, glanced, term))
```

    ## # A tibble: 10 x 5
    ## # Groups:   Province [10]
    ##    Province estimate std.error statistic  p.value
    ##    <chr>       <dbl>     <dbl>     <dbl>    <dbl>
    ##  1 EC         0.303    0.0152      20.0  5.48e-36
    ##  2 FS         0.362    0.0276      13.1  4.41e-23
    ##  3 GP         0.275    0.0124      22.1  2.17e-39
    ##  4 KZN        0.220    0.0123      17.9  2.53e-32
    ##  5 LP         0.104    0.00891     11.7  4.23e-20
    ##  6 MP         0.0818   0.0401       2.04 4.43e- 2
    ##  7 NC         0.303    0.0393       7.71 1.18e-11
    ##  8 NW         0.212    0.0165      12.9  1.20e-22
    ##  9 WC         0.653    0.0177      36.8  2.13e-58
    ## 10 RSA        0.288    0.0105      27.5  2.40e-47
