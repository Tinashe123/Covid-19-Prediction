rm(list = ls())

library(ggplot2)
library(deSolve)
library(reshape2)
library(tidyr)
library(pso)
library(dplyr)
library(lubridate)
library(readr)

setwd("G:/My Drive/University/Meesters/Year 2/Capstone/modelling")

##############################################################################
## Covid 19 data
## reading cumulative deaths
cumtive_cases <- read.csv("./data/covid19za_provincial_cumulative_timeline_confirmed.csv", stringsAsFactors = F)

## Back calculating deaths per day and adding epi week for correlation anlysis with excess deaths
cases <- cumtive_cases %>% 
  mutate(across(.cols = EC:total, ~ifelse(YYYYMMDD == 20200305, .,  (.) - dplyr::lag(.))),
         date = dmy(date),
         day = (as.numeric(date - min(date)))/365)%>% 
  select(day, cases = total)

###############################################################################
## Create function to calculate SIR model that includes mortality and birth rate
sir <- function(beta, gamma, sigma, mu, b, S0, I0, R0, times) {
  require(deSolve) # for the "ode" function
  
  # the differential equations:
  sir_equations <- function(time, variables, parameters) {
    with(as.list(c(variables, parameters)), {
      N=S+I+R
      lambda=beta*(I/N)
      dS=-lambda*S-mu*S+b*N+sigma*R
      dI=lambda*S-gamma*I-mu*I
      dR=gamma*I-mu*R-sigma*R
      return(list(c(dS, dI, dR)))
    })
  }
  
  # the parameters values:
  parameters_values <- c(beta  = beta, gamma = gamma, sigma = sigma, b = b, mu = mu)
  
  # the initial values of variables:
  initial_values <- c(S = S0, I = I0, R = R0)
  
  # solving
  out <- ode(initial_values, times, sir_equations, parameters_values)
  
  # returning the output:
  as.data.frame(out)
}

### First prediction 
pred <- sir(beta = 0.4*365, 
              gamma = 0.2*365, 
              sigma = 2, 
              b = 19.328/1000, ## Current national average birth rate
              mu = 9.415/1000, ## Current national average death rate
              S0 = 59.31*10^6, 
              I0 = 1, 
              R0 = 0, 
              times = seq(0, 749/365, by = 1/365)
              )

## Plot od S, I &R over time
pred %>% 
  pivot_longer(cols = S:R) %>% 
  ggplot(aes(x = time, y = value, colour = name))+
  geom_line()

## Sum of squares function to minimize and fit the equation to the actual data
sum_s <- function(pars0, data = cases, N = 59.31*10^6) {
  I0 <- data$cases[1]
  times <- data$day
  predictions <- sir(beta = pars0[1], # parameters
                     gamma = pars0[2],   
                     sigma = pars0[3],
                     b = 19.328/1000,
                     mu = 9.415/1000,
                     S0 = N - I0, I0 = I0, R0 = 0, # variables' intial values
                     times = times)                # time points
  sum((predictions$I[-1] - data$cases[-1])^2)
}

## Choose initial parameters to optimize from
pars0 <- c(1*365, 0.2*365, 2)

## Optimize these three parameters using "L-BFGS-B" and optimizing sum of square error
fit <- optim(pars0, sum_s,  method = "L-BFGS-B", lower = 0)

## Store the optimal parameters
opt_par <- fit$par

## Use these parameters to calculate the SIR model
pred_opt <- sir(beta = opt_par[1], 
                gamma = opt_par[2], 
                sigma = opt_par[3], 
                b = 19.328/1000, ## Current national average birth rate
                mu = 9.415/1000, ## Current national average death rate
                S0 = 59.31*10^6, 
                I0 = 1, 
                R0 = 0, 
                times = seq(0, 749/365, by = 1/365)
)


df <- cases %>% 
  rename(time = day) %>% 
  inner_join(pred_opt, by = "time")

df %>% 
  pivot_longer(cols = c(I, cases)) %>% 
  ggplot(aes(x = time, y = value, colour = name))+
  geom_line()
