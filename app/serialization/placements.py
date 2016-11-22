list_placements_schema = {
    'id': ('id', int),
    'order_id': ('order_id', int),
    'placer_id': ('placer_id', int),
    'placed_at': ('placed_at', str)
}

# for now they are equal, but perhaps one day they will be the same
detail_placement_schema = {
    'id': ('id', int),
    'order_id': ('order_id', int),
    'placer_id': ('placer_id', int),
    'placed_at': ('placed_at', str)
}
