class Vertex(object):
    # name_ should be a string identifier - only unique if the user is careful (or lucky) to make it so
    # genus_ should be a non-negative integer
    def __init__(self, name_, genus_):
        # Don't allow negative genus!
        if genus_ < 0:
            raise ValueError("Genus must be non-negative")
        self.name = name_
        self._genus = genus_

    @property
    def genus(self):
        return self._genus

    # Control how the genus property is set
    # genus_ should be a non-negative integer
    @genus.setter
    def genus(self, genus_):
        # Don't allow negative genus!
        if genus_ < 0:
            raise ValueError("Genus must be non-negative.")
        self._genus = genus_