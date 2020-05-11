#imortant libarary to import
import pandas as pd 
import geopandas as gpd # handele the gedata shape file
import rtree  #frist install rtree -> sudo apt install rtree then import
from pathlib import Path # to know the current working directory

print(Path.cwd())

#file path of shape file which you want to join 
point_fp='/home/navneet/Documents/companyTask/spatial join/vs_spatial/data/Point_sample/point_sample.shp'
poly_fp='/home/navneet/Documents/companyTask/spatial join/vs_spatial/data/Polygon_sample/all.shp'

#read both the shape file using geopandas 
point_df=gpd.read_file(point_fp)
poly_df=gpd.read_file(poly_fp)


#perform the spatial join point with polygon
def spjoinWithin(point_df, poly_df):
    point_with_poly_within=gpd.sjoin(point_df, poly_df, how="inner", op='within')
    return point_with_poly_within

#spatial join with intersects operation
def spjoinIntersect(point_df, poly_df):
    point_with_poly_intersect=gpd.sjoin(point_df, poly_df, how="inner", op='intersects')
    return point_with_poly_intersect

#spatial join with contain operation
def spjointContain(point_df, poly_df):
    point_with_poly_contain=gpd.sjoin(poly_df, point_df,how="inner", op='contains')
    return point_with_poly_contain



#no. of point intersect the polygon city
def numOfPointIntersect():
    n = spjoinIntersect(poly_df, point_df)
    print("no. of point intersect the polygon city")
    no_of_point=n.Name.value_counts()
    print(no_of_point)

#how many point 'rajnandgaon' in the polygon cities
def howManypointInPoly():
    n = spjoinIntersect(poly_df, point_df)
    print("no. of point 'rajnandgaon' in the polygon cities")
    specific_point_in_city=n[n.Addr_Cur_3 == 'RAJNANDGAON'].City.value_counts()
    print(specific_point_in_city)


#calling function according to your requirment
#we want no. of point intersect in polygon
numOfPointIntersect()
