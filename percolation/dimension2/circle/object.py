class Circle:
    def __init__(self, x, y, r) -> None:
        self.x = x
        self.y = y
        self.r = r
        
        
    def intersect(self, other) -> bool:
        self_xy = [self.x, self.y]
        other_xy = [other.x, other.y]
        return dist(self_xy, other_xy) <= self.r + other.r