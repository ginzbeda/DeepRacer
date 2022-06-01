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
    steering_angle = params['steering_angle']
    track_width = params['track_width']

    center_reward = 0

    # Weight of Rewards

    speed_weight = 150
    steering_weight = 50
    heading_weight = 100
    centered_weight = 75
    speed_threshold = 2.0

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        center_reward = (1 - (distance_from_center / (track_width / 2))) * centered_weight

    # lower reward if car goes off track
    if not all_wheels_on_track or is_offtrack:
        return 1e-3

    # Direction of the center line to closest waypoint and future waypoints
    # Account for coming to finish
    if closest_waypoints[1] + 1 < len(waypoints):
        third_waypoint = waypoints[closest_waypoints[1] + 1]
        # if closest_waypoints[1] + 2 < len(waypoints):
        # fourth_waypoint = waypoints[closest_waypoints[1] + 2]
        # else:
        # fourth_waypoint = waypoints[0]
    else:
        third_waypoint = waypoints[0]
        # fourth_waypoint = waypoints[1]
    next_waypoint = waypoints[closest_waypoints[1]]
    last_waypoint = waypoints[closest_waypoints[0]]

    # Calculate the direction using arctan
    next_direction = math.atan2(next_waypoint[1] - last_waypoint[1], next_waypoint[0] - last_waypoint[0])
    third_direction = math.atan2(third_waypoint[1] - last_waypoint[1], third_waypoint[0] - last_waypoint[0])
    # future_direction = math.atan2(third_waypoint[1] - next_waypoint[1], third_waypoint[0] - next_waypoint[0])

    # Calculate degree needed
    next_direction = math.degrees(next_direction)
    third_direction = math.degrees(third_direction)
    # future_direction = math.degrees(future_direction)

    # Average degree
    track_direction = (next_direction + third_direction) / 2

    # Calculate the difference between degree needed and degree of car direction
    direction_diff = abs(track_direction - heading)

    # Account of other direction of track
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    direction_reward = (1 - (direction_diff / 180)) * heading_weight

    # Steering Angle Reward
    steering_reward = (1 - ((abs(steering_angle - direction_diff)) / 180)) * steering_weight

    # Calculate future next to check if necessary to slow down
    # future_next_direction = math.atan2(fourth_waypoint[1] - last_waypoint[1], fourth_waypoint[0] - last_waypoint[0])
    # future_next_direction = math.degrees(future_next_direction)
    # future_direction_diff = abs(future_next_direction - direction_diff)

    # Account of other direction of track
    # if future_direction_diff > 180:
    #     future_direction_diff = 360 - future_direction_diff

    # Set lower speed threshold if future turn is big
    # if future_direction_diff > 5:
    #     speed_threshold *= 0.56

    # Speed reward
    # Account for speed below threshold and lowering speed to prepare for a turn
    min_speed = 0.75
    max_speed = 4
    throttle = (speed - min_speed) / (max_speed - min_speed)
    if throttle > speed_threshold:
        speed_weight = speed_weight + 50

    speed_reward = (1 - (max_speed - (speed - min_speed))) * speed_weight
    # if speed < speed_threshold:
    #     speed_weight = (max_speed - (speed_threshold - speed)) / (max_speed - min_speed) * 50
    # else:
    #     speed_weight = (speed_weight + (speed - speed_threshold )) / (max_speed - min_speed) * 50
    # speed_reward = ((speed / max_speed) ** 3) \
    # max_speed * (speed *10) + weight_speed
    #     #(math.pow(speed, 2) - min_speed) / (max_speed - min_speed) * speed_weight

    return center_reward + speed_reward + steering_reward + direction_reward + progress
