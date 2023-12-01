# Data Dicionary: bike_accidents.csv

| column name | type | description | 
|-------------|------|-------------|
|accident_id|||
|between_street_name_1| string | Accident occurs between two streets: name of one street |
|between_street_name_2| string | Accident occurs between two streets: name of second street |
|between_street_number_1| string | Accident occurs between two streets: number of first street |
|between_street_number_2|string| Accident occurs between two streets: number of second street|
|building_number| number | Building number of accident site |
|date| pandas.Timestamp | Date and time of accident|
|day| number | Day of month for date of accident |
|day_of_week| string | Name of weekday for time of accident |
|directional_analysis| ||
|fatality_indicator| boolean | Did the accident result in a fatality? |
|hit_and_run_indicator| boolean | Was the accident a hit and run? |
|hour| number | Hour component of time of accident |
|injury_indicator| boolean | Did the accident cause an injury? |
|intersection_roadway_name| string | Accident occurs in intersection: name of road intersecting with main road |
|intersection_roadway_number|string | Accident occurs in intersection: number of road intersection with main road |
|investigating_agency|string| Police agency responding to the accident |
|latitude| float | Latitude coordinate for accident site |
|light_condition| string | Light condition during the accident. |
|lighted_signal_indicator| boolean| If accident happened in an intersection, did the intersection have a traffic light? |
|longitude| float| Longitude coordinate for accident site |
|manner_of_collision| string | |
|milepoint| number | Milepoint along roadway where accident happened |
|minute| number | Minute component for time of accident|
|month| number | Month component for time of accident |
|motor_vehicles_involved| number | Count of motor vehicles involved in accident |
|roadway_character|||
|roadway_condition|||
|roadway_direction|||
|roadway_name|||
|roadway_number|||
|roadway_suffix|||
|roadway_type|||
|secondary_collision_indicator|||
|units_involved| number | Total vehicles involved in accident, including motor vehicles and bicycles |
|weather| string | Weather condition during accident |
|year| number | Year component for date of accident |
