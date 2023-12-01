# Data Dicionary: bike_accidents.csv

| column name | type | description | 
|-------------|------|-------------|
|accident_id| number | Unique numeric index for each row. |
|between_street_name_1| string | Accident occurs between two streets: name of one street |
|between_street_name_2| string | Accident occurs between two streets: name of second street |
|between_street_number_1| string | Accident occurs between two streets: number of first street |
|between_street_number_2|string| Accident occurs between two streets: number of second street|
|building_number| number | Building number of accident site |
|date| pandas.Timestamp | Date and time of accident|
|day| number | Day of month for date of accident |
|day_of_week| string | Name of weekday for time of accident |
|directional_analysis| string | Description of the accident in terms of the direction one vehicle hit another. |
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
|roadway_character| string | Description of the roadway shape |
|roadway_condition| string | Description of the road surface conditions |
|roadway_direction| string | Cardinal directions for roadways that use them in their names |
|roadway_name| string | Name of roadway |
|roadway_number| string | Alphanumeric designator for roadway |
|roadway_suffix| string | Suffix for roadway type: St, Ln, Rd, etc. |
|roadway_type| string | Type of road or roadway owner: Local, State, Federal, etc. |
|secondary_collision_indicator| boolean | Was the collision the indirect consequence of another collision? |
|units_involved| number | Total vehicles involved in accident, including motor vehicles and bicycles |
|weather| string | Weather condition during accident |
|year| number | Year component for date of accident |
