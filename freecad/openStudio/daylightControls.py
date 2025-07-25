# Adding Daylighting Controls, Schedules, Shading, and Postprocessing

# We'll cover each feature with sample code and where to plug it into your pipeline.

#1. 🌞 Daylighting Controls

# Purpose:
# Place sensors inside zones to simulate daylighting/autodimming.

# Add after space creation:

from openstudio import Point3d

# Place sensor at center of floor (adjust as needed)
sensor_point = Point3d(5.0, 1.5, 0.8)  # x, y, z in meters

daylight_control = openstudio.model.DaylightingControl(model)
daylight_control.setName("Daylight Sensor")
daylight_control.setPosition(sensor_point)
daylight_control.setIlluminanceSetpoint(500.0)  # lux
daylight_control.setSpace(space)

# Assign Custom Schedules from gbXML or Data

# If your gbXML parser provides occupancy schedules, you can match them to OpenStudio's ScheduleRuleset.

# Example:

schedule = openstudio.model.ScheduleRuleset(model)
rule = openstudio.model.ScheduleRule(schedule)

day_schedule = rule.daySchedule()
day_schedule.setName("Weekday Occupancy")
for hour in range(24):
    value = 1.0 if 8 <= hour < 18 else 0.0
    day_schedule.addValue(openstudio.Time(0, hour, 0, 0), value)

people.setNumberofPeopleSchedule(schedule)
# Repeat for lights, equipment, etc.

