import math

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    abs_steering = abs(params['steering_angle'])
    speed = params["speed"]
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    
    # Give a very low reward by default
    reward = 1e-3
        
    # Get extra reward for having more speed
    # Steering penality threshold, change the number based on MAX speed
    MAX_SPEED = 3 
    speed_reward = speed/MAX_SPEED * 0.3
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 0.7
    elif distance_from_center <= marker_2:
        reward += 0.4
    elif distance_from_center <= marker_3:
        reward += 0.15
    else:
        reward += 1e-3  # likely crashed/ close to off track
        
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car and combine it with the speed_reward
    heading = 0.0001 if heading == 0 else heading
    direction_diff = abs(track_direction/heading) if (track_direction < 0 and heading < 0) or (track_direction > 0 and heading > 0) else track_direction/heading
    reward += speed_reward * direction_diff
    
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 20 
    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.7
    
    return float(reward)
