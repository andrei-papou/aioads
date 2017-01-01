list_placements_schema = {
    'id': ('id', int),
    'order_id': ('order_id', int),
    'placer_id': ('placer_id', int),
    'placed_at': ('placed_at', str),
    'views': ('views', int),
    'clicks': ('clicks', int)
}

# for now they are equal, but perhaps one day they won't be the same
detail_placement_schema = {
    'id': ('id', int),
    'order_id': ('order_id', int),
    'placer_id': ('placer_id', int),
    'placed_at': ('placed_at', str)
}
