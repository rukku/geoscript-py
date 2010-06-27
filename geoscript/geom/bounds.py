from org.geotools.geometry.jts import ReferencedEnvelope
from geoscript.util import deprecated
from geoscript import proj

class Bounds(ReferencedEnvelope):
  """
  A two dimensional bounding box.
  """
  def __init__(self, west=None, south=None, east=None, north=None, prj=None, env=None):
    if prj:
      prj = proj.Projection(prj)

    if env:
      if prj:
        ReferencedEnvelope.__init__(self, env, prj._crs)
      else:
        ReferencedEnvelope.__init__(self, env)
    else:
      if west:
        ReferencedEnvelope.__init__(self, west, east, south, north, 
           prj._crs if prj else None)
      elif prj:
        ReferencedEnvelope.__init__(self, prj._crs) 
      else:
        ReferencedEnvelope.__init__(self)

  def getwest(self):
    return self.minX()
  west = property(getwest)
  """
  The leftmost/westmost oordinate of the bounds.
  """

  @deprecated
  def get_l(self):
    return self.west
  l = property(get_l, None, None, "Use west.")

  def getsouth(self):
    return self.minY()
  south = property(getsouth)
  """
  The bottomtmost/southmost oordinate of the bounds.
  """

  @deprecated
  def get_b(self):
    return self.south
  b = property(get_b, None, None, "Use south.")

  def geteast(self):
    return self.maxX()
  east = property(geteast)
  """
  The rightmost/eastmost oordinate of the bounds.
  """

  @deprecated
  def get_r(self):
    return self.east
  r = property(get_r, None, None, 'Use east.')

  def getnorth(self):
    return self.maxY()
  north = property(getnorth)
  """
  The topmost/northmost oordinate of the bounds.
  """

  @deprecated
  def get_t(self):
    return self.north
  t = property(get_t, None, None, 'Use north.')

  def getproj(self):
    crs = self.coordinateReferenceSystem
    if crs:
      return proj.Projection(crs)
  proj = property(getproj)
  """
  The :class:`Projection <geoscript.proj.Projection>` of the bounds. ``None`` if the projection is unknown.
  """

  def reproject(self, prj):
    """
    Reprojects the bounding box.
    
    *prj* is the destination :class:`Projection <geoscript.proj.Projection>` 

    """
    if not self.proj:
      raise Exception('No projection set on bounds, unable to reproject')

    prj = proj.Projection(prj)
    return Bounds(env=self.transform(prj._crs, True))

  def scale(self, factor):
    """
    Scales the bounds by a specified factor.

    *factor* is the scale factor. The scale factor must be greather than 0. A 
    value greater than 1 will grow the bounds whereas a value of less than 1 
    will shrink the bounds.
   
    This method returns a new :class:`Bounds <geoscript.geom.bounds.Bounds>` 
    object.

    >>> b = Bounds(0, 0, 1, 1)
    >>> b1 = b.scale(1.5)
    (-0.25, -0.25, 1.25, 1.25)
    """
    w = self.width * (factor - 1) / 2
    h = self.height * (factor - 1) / 2

    return Bounds(self.west - w, self.south - h, self.east + w, self.north + h)
   
  def __repr__(self):
    s = '(%s, %s, %s, %s' % (self.west, self.south, self.east, self.north)
    if self.proj:
      s = '%s, %s' % (s, self.proj.id)

    return '%s)' % s

