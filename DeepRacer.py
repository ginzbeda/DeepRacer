import math

def reward_function(params):
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    progress = params['progress']
    is_offtrack = params['is_offtrack']
    
    reward = 25
    
    #set speed threshold
    SPEED_THRESHOLD = 2.5
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.25 * track_width
    marker_2 = 0.5 * track_width
    marker_3 = 0.75 * track_width

     # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 10
    elif distance_from_center <= marker_2:
           reward += 5
    elif distance_from_center <= marker_3:
           reward -= 5
    #lower reward if car goes off track
    elif not all_wheels_on_track:
           reward *= 0.5


     #Direction of the center line to closest waypoint and future waypoints
    #Account for coming to finish
    if closest_waypoints[1]+1 < len(waypoints):
           third_waypoint = waypoints[closest_waypoints[1]+1]
           if closest_waypoints[1]+2 < len(waypoints):
               fourth_waypoint = waypoints[closest_waypoints[1]+2]
           else:
               fourth_waypoint = waypoints[0]
    else:
        third_waypoint = waypoints[0]
        fourth_waypoint = waypoints[1]
    next_waypoint = waypoints[closest_waypoints[1]]
    last_waypoint = waypoints[closest_waypoints[0]]


      # Calculate the direction using arctan
    next_direction = math.atan2(next_waypoint[1] - last_waypoint[1], next_waypoint[0] - last_waypoint[0])
    third_direction = math.atan2(third_waypoint[1] - last_waypoint[1], third_waypoint[0] - last_waypoint[0])
    future_direction = math.atan2(third_waypoint[1] - next_waypoint[1], third_waypoint[0] - next_waypoint[0])

     # Calculate degree needed
    next_direction = math.degrees(next_direction)
    third_direction = math.degrees(third_direction)
    future_direction = math.degrees(future_direction)


    #Average degree 
    track_direction = (next_direction + third_direction + future_direction)/3

    #Calculate future next to check if necessary to slow down
    future_next_direction = math.atan2(fourth_waypoint[1] - third_waypoint[1], fourth_waypoint[0] - third_waypoint[0])
    future_next_direction = math.degrees(future_next_direction)
    future_direction_diff = abs(future_next_direction - heading)

    # Account of other direction of track
    if future_direction_diff > 180:
        future_direction_diff = 360 - future_direction_diff        

    #Set lower speed threshold if future turn is big
    if future_direction_diff > 15 :
        SPEED_THRESHOLD *= 0.75

    # Calculate the difference between degree needed and degree of car direction
    direction_diff = abs(track_direction - heading)

     # Account of other direction of track
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    # increase reward for going faster
    if speed > SPEED_THRESHOLD:
        reward *= 1.2

    if is_offtrack:
        reward *= 0.5

     #Account for not making progress
    reward += progress

    return float(reward)