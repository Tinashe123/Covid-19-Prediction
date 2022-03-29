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

## Back calculating deaths per day and adding epi week for correlation anlysis with excess deaths
deaths <- cumtive_deaths %>% 
  mutate(across(.cols = EC:total, ~ifelse(YYYYMMDD == 20200327, .,  (.) - dplyr::lag(.))),
         date = dmy(date),
         epi_week = epiweek(date),
         indicator = "Covid 19 Deaths") %>% 
  select(date, epi_week, EC:WC, RSA = total, indicator)
  

## Changing compatibility between two death data frames
excess_deaths_clean <- excess_deaths %>%
  rename(date = X) %>% 
  mutate(date = dmy(date),
         epi_week = epiweek(date),
         indicator = "Excess Deaths") %>% 
  select(date, epi_week, EC, FS, GP = GT, KZN, LP = LM, MP:WC, RSA, indicator)

combined_df <- rbind(deaths, excess_deaths_clean) %>% 
  mutate(year = year(date))

## Plot the excess mortality and actual deaths per week over time to compare trends
combined_df %>% 
  group_by(epi_week, year, indicator) %>% 
  summarise(date = min(date),
            across(.cols = EC:RSA, ~sum(., na.rm = T))) %>% 
  pivot_longer(cols = EC:RSA, names_to = "Province", values_to = "Deaths") %>% 
  ggplot(aes(x = date, y = Deaths, colour = indicator))+
  geom_line()+
  facet_wrap(.~Province, scales = "free_y")

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

## Nest by geography to perform linear rgression per province and for the country 
## between excess deaths and rported covid 19 fatalities
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

lin_reg %>% 
  unnest(glanced) %>% 
  select(-c(data:tidied))

lin_reg %>% 
  unnest(tidied) %>% 
  select(-c(data, fit, glanced, term))


