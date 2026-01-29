import math

def main():

    can_names = [
        '#1 Picnic', '#1 Tall', '#2 Tall', '#2', '#3 Cyclinder',
        '#5', '#6Z', '#8Z short', '#10', '#211', '#300', '#303'
    ]

    can_heights = [
        10.16, 11.91, 11.59, 11.91, 17.78, 14.29,
        8.89, 7.62, 17.78, 12.38, 11.27, 11.11
    ]

    can_radiuses = [
        6.83, 7.78, 8.73, 10.32, 10.79, 13.02,
        5.40, 6.83, 15.72, 6.83, 7.62, 8.10
    ]

    can_costs = [
        0.28, 0.43, 0.45, 0.61, 0.86, 0.83,
        0.22, 0.26, 1.53, 0.34, 0.38, 0.42
    ]

    best_store = None
    best_cost = None
    max_store_eff = -1
    max_cost_eff = -1


    for i in range(len(can_names)):
        name = can_names[i]
        radius = can_radiuses[i]
        height = can_heights[i]
        cost = can_costs[i]
        storage_efficiency = compute_storage_efficiency(radius, height)
        cost_efficiency = compute_cost_efficiency(radius, height, cost)

        print(f'Name: {name} | Storage efficiency: {storage_efficiency:.2f} | Cost efficiency: {cost_efficiency:.0f}')
        
        if storage_efficiency > max_store_eff:
            best_store = name
            max_store_eff = storage_efficiency
        if cost_efficiency > max_cost_eff:
            best_cost = name
            max_cost_eff = cost_efficiency

    print()
    print(f'Best can size in storage efficiency: {best_store}')
    print(f'Best can size in cost efficiency: {best_cost}')

def compute_volume(radius, height):
    volume = math.pi * radius**2 * height
    return volume

def compute_surface_area(radius, height):
    surface_area = 2 * math.pi * radius * (radius + height)
    return surface_area

def compute_storage_efficiency(radius, height):
    volume = compute_volume(radius, height)
    surface_area = compute_surface_area(radius, height)
    efficiency = volume / surface_area
    return efficiency

def compute_cost_efficiency(radius, height, cost):
    volume = compute_volume(radius, height)
    efficiency = volume / cost
    return efficiency

main()