
# Postprocess EnergyPlus Simulation Results

# After generating and simulating your IDF (via OpenStudio or EnergyPlus CLI), you can extract results from the .sql output.

sql_path = openstudio.path("run/eplusout.sql")
sql_file = openstudio.SqlFile(sql_path)

model.setSqlFile(sql_file)

# Example: Get annual heating load for a thermal zone
zone = model.getThermalZones()[0]
result = zone.annualHeatingLoad()
print(f"{zone.nameString()} annual heating: {result.get} GJ")

