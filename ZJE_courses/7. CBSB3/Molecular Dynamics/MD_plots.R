# Plots to evaluate the GROMACS pipeline
library(ggplot2)
setwd("~/Documents/ZJE/Teaching/CBSB3_2022/Modeling/Practical2")

# Energy minimization
# Receives potential.xvg
potential <- read.table("potential.xvg", sep = "" , header = FALSE , skip = 24, na.strings = "",
                        stringsAsFactors = FALSE)
ggplot(data = potential, aes(x = V1, y = V2)) +
  geom_line() +
  geom_point() +
  ylim(min(potential$V2), 0) +
  labs(x = "Energy Minimization Step", y = bquote("Potential Energy (kJ "*~mol^-1*')')) +
  ggtitle("Energy Minimization, Steepest Descent") +
  theme_bw() +
  theme(plot.title = element_text(size = rel(1.5), face = "bold"))

# Temperature equilibration
# Receives temperature.xvg
temperature <- read.table("temperature.xvg", sep = "" , header = FALSE , skip = 24, na.strings = "",
                          stringsAsFactors = FALSE)
temperature$average10ps <- NA
temperature$average10ps[10:nrow(temperature)] <- sapply(10:nrow(temperature), function(x){mean(temperature$V2[(x-9):x])})
ggplot(data = temperature, aes(x = V1, y = V2)) +
  geom_line() +
  geom_point() +
  geom_line(aes(y = average10ps, col = "Running average 10 ps")) +
  labs(x = "Time (ps)", y = "Temperature (K)") +
  ggtitle("Temperature, NVT equilibration") +
  theme_bw() +
  theme(legend.position = c(0.80, 0.9),
        legend.title = element_blank(),
        plot.title = element_text(size = rel(1.5), face = "bold"))

# Pressure equilibration
# Receives pressure.xvg
pressure <- read.table("pressure.xvg", sep = "" , header = FALSE , skip = 24, na.strings = "",
                          stringsAsFactors = FALSE)
pressure$average10ps <- NA
pressure$average10ps[10:nrow(pressure)] <- sapply(10:nrow(pressure), function(x){mean(pressure$V2[(x-9):x])})
ggplot(data = pressure, aes(x = V1, y = V2)) +
  geom_line() +
  geom_point() +
  geom_line(aes(y = average10ps, col = "Running average 10 ps")) +
  labs(x = "Time (ps)", y = "Pressure (bar)") +
  ggtitle("Pressure, NPT equilibration") +
  theme_bw() +
  theme(legend.position = c(0.80, 0.9),
        legend.title = element_blank(),
        plot.title = element_text(size = rel(1.5), face = "bold"))

# Density equilibration
# Receives density.xvg
density <- read.table("density.xvg", sep = "" , header = FALSE , skip = 24, na.strings = "",
                       stringsAsFactors = FALSE)
density$average10ps <- NA
density$average10ps[10:nrow(density)] <- sapply(10:nrow(density), function(x){mean(density$V2[(x-9):x])})
ggplot(data = density, aes(x = V1, y = V2)) +
  geom_line() +
  geom_point() +
  geom_line(aes(y = average10ps, col = "Running average 10 ps")) +
  labs(x = "Time (ps)", y = bquote("Density (kg "*~m^-3*')')) +
  ggtitle("Density, NPT equilibration") +
  theme_bw() +
  theme(legend.position = c(0.80, 0.2),
        legend.title = element_blank(),
        plot.title = element_text(size = rel(1.5), face = "bold"))

# RMSD, backbone
# Receives rmsd.xvg and rmsd_xtal.xvg
rmsd_equilibrated <- read.table("rmsd.xvg", sep = "" , header = FALSE , skip = 18, na.strings = "",
                      stringsAsFactors = FALSE)
rmsd_xtal <- read.table("rmsd_xtal.xvg", sep = "" , header = FALSE , skip = 18, na.strings = "",
                                stringsAsFactors = FALSE)
rmsd <- rmsd_equilibrated
names(rmsd) <- c("time", "equilibrated")
rmsd$xtal <- rmsd_xtal$V2
ggplot(data = rmsd, aes(x = time)) +
  geom_line(aes(y = equilibrated, col = "Ref: Equilibrated")) +
  geom_line(aes(y = xtal, col = "Ref: Original") ) +
  labs(x = "Time (ns)", y = "RMSD (nm)") +
  ggtitle("RMSD, backbone") +
  theme_bw() +
  theme(legend.position = c(0.80, 0.2),
        legend.title = element_blank(),
        plot.title = element_text(size = rel(1.5), face = "bold"))

# Radius of gyration
# Receives gyrate.xvg
gyration <- read.table("gyrate.xvg", sep = "" , header = FALSE , skip = 27, na.strings = "",
                        stringsAsFactors = FALSE)
ggplot(data = gyration, aes(x = V1/1000, y = V2)) +
  geom_line() +
  geom_point() +
#  ylim(1.3, 1.50) +
  labs(x = "Time (ns)", y = bquote(~R[g]*" (nm)")) +
  ggtitle("Radius of gyration, Unrestrained MD") +
  theme_bw() +
  theme(plot.title = element_text(size = rel(1.5), face = "bold"))
