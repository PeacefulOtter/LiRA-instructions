# PostGIS functions instructions

## 1. wayDists

### 1.1 Description
`f(way_id) = [way_dist1, way_dist2, ...]`

Get the node's 'distance from the start of the way' (`way_dist`) for a way with id `way_id` .

### 1.2 Prototype
```sql
wayDists(way_id character varying(255)) 
returns table (way_dist double)
```

### 1.3 Implementation
```sql
return query 
    select ST_LineLocatePoint(geom, (ST_DumpPoints(geom)).geom
    from way where id=way_id;
```

## 2. wayCoords

### 2.1 Description
`f(way_id) = [(lat1, lng1), (lat2, lng2), ...]`

Get the node's coordinates (latitude, longitude) for a way with id `way_id` 

### 2.1 Prototype
```sql
wayCoords(way_id character varying(255)) 
returns table (coordinates json)
```

### 2.3 Implementation
```sql
return query 
    select ST_AsGeoJSON((ST_DumpPoints(geom)).geom)::json->'coordinates' 
    from way where id=way_id;
```

## 3. getCoord

### 3.1 Description
`f(way_id, way_dist) = (lat, lng)`

Get the coordinates (latitude, longitude) of a point located on the way with id `way_id` at a distance from the start of the way `way_dist`

### 3.2 Examples
#### 1. Getting the coordinates of all the rows stored in the altitude table.
```sql
select lat, lng from altitude, getCoord(way_id, way_dist);
```
#### 2. Getting the coordinates of a point.
```sql
select lat, lng from getCoord('420540', 0.25);
```

### 3.3 Prototype
```sql
getCoord(way_id character varying(255), way_dist double precision) 
returns table (lat double, lng double)
```

### 3.4 Implementation

```sql
select ST_Y(point) as lat, ST_X(point) as lng 
from way, ST_LineInterpolatePoint(geom, way_dist) as point 
where id = way_id;
```

## 4. wayDist

precision

```sql
wayDist(way_id character varying(255), point Point) 
returns table (way_dist double)
```

### 4.3 Implementation
```sql
return query 
    select ST_LineLocatePoint(geom, point::geometry) as way_dist 
    from way where id=way_id;
```

## 5. getCoords

### 5.1 Description

`f(way_id, padding) = [(way_dist1, lat1, lng1), (way_dist2, lat2, lng2), ...]`

Get the 'distance from the start of the way' (`way_dist`) and coordinates (latitude, longitude) of all the points located at an interval of `padding` (meters) on a way with id `way_id`.

Example: A `padding` of 5 will return the points located every 5 meters on a way
```
           0m                              23m
     way:  |_______________________________|
returned:  |------|------|------|------|---
           p1     p2     p3     p4     p5
           0m     5m     10m    15m    20m
```

### 5.2 Prototype

```sql
getCoords(way_id character varying(255), padding integer) 
returns table (way_dist double, lat double, lng double)
```

### 4.3 Implementation
```sql
return query 
    select point, ST_X(ST_LineInterpolatePoint(geom, point)), ST_Y(ST_LineInterpolatePoint(geom, point))
    from (
        select geom, generate_series(0, cast(ST_Length(geom::geography) as integer), padding) / ST_Length(geom::geography) as point
        from way where id=way_id
    ) as subquery;
```