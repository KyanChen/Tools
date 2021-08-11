from osgeo import gdal

img_file = r'G:\Coding\ShipDetection_hzj\ShipDetection\read.tiff'
data_set = gdal.Open(img_file)
im_width = data_set.RasterXSize
im_height = data_set.RasterYSize
im_bands = data_set.RasterCount
transform = data_set.GetGeoTransform()
projection = data_set.GetProjection()
im_data = data_set.GetRasterBand(1).ReadAsArray(0, 0, im_width, im_height)
driver = gdal.GetDriverByName("GTiff")
dataset = driver.Create(img_file.replace('read', 'read_single'), im_width, im_height, 1, gdal.GDT_UInt16)
dataset.SetGeoTransform(transform)
dataset.SetProjection(projection)
dataset.GetRasterBand(1).WriteArray(im_data)
