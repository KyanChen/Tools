from osgeo import gdal
from osgeo import osr
import numpy as np

def getSRSPair(dataset):
    '''
    获得给定数据的投影参考系和地理参考系
    :param dataset: GDAL地理数据
    :return: 投影参考系和地理参考系
    '''
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(dataset.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs

def geo2lonlat(dataset, x, y):
    '''
    将投影坐标转为经纬度坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param x: 投影坐标x
    :param y: 投影坐标y
    :return: 投影坐标(x, y)对应的经纬度坐标(lon, lat)
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(prosrs, geosrs)
    coords = ct.TransformPoint(x, y)
    return coords[:2]


def lonlat2geo(dataset, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 经纬度坐标(lon, lat)对应的投影坐标
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    coords = ct.TransformPoint(lon, lat)
    return coords[:2]

def imagexy2geo(dataset, row, col):
    '''
    根据GDAL的六参数模型将影像图上坐标（行列号）转为投影坐标或地理坐标（根据具体数据的坐标系统转换）
    :param dataset: GDAL地理数据
    :param row: 像素的行号
    :param col: 像素的列号
    :return: 行列号(row, col)对应的投影坐标或地理坐标(x, y)
    '''
    trans = dataset.GetGeoTransform()
    px = trans[0] + col * trans[1] + row * trans[2]
    py = trans[3] + col * trans[4] + row * trans[5]
    return px, py


def geo2imagexy(dataset, x, y):
    '''
    根据GDAL的六 参数模型将给定的投影或地理坐标转为影像图上坐标（行列号）
    :param dataset: GDAL地理数据
    :param x: 投影或地理坐标x
    :param y: 投影或地理坐标y
    :return: 影坐标或地理坐标(x, y)对应的影像图上行列号(row, col)
    '''
    trans = dataset.GetGeoTransform()
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([x - trans[0], y - trans[3]])
    return np.linalg.solve(a, b)  # 使用numpy的linalg.solve进行二元一次方程的求解

def convert(infile,outfile):

  dataset = gdal.Open(infile, gdal.GA_ReadOnly)
  sr = osr.SpatialReference()
  sr.SetWellKnownGeogCS('WGS84')
  dst_ds = gdal.Warp(outfile, dataset, format='GTiff',
                    resampleAlg=gdal.GRIORA_Bilinear, outputType=gdal.GDT_Int16,rpc=True)
  del dataset, sr

if __name__ == '__main__':
    gdal.AllRegister()
    dataset = gdal.Open(r"F:\2016\Data\Great Khingan\DEM\Projection\strm_6102_UTM.tif")
    print('数据投影：')
    print(dataset.GetProjection())
    print('数据的大小（行，列）：')
    print('(%s %s)' % (dataset.RasterYSize, dataset.RasterXSize))

    x = 464201
    y = 5818760
    lon = 122.47242
    lat = 52.51778
    row = 2399
    col = 3751

    print('投影坐标 -> 经纬度：')
    coords = geo2lonlat(dataset, x, y)
    print('(%s, %s)->(%s, %s)' % (x, y, coords[0], coords[1]))
    print('经纬度 -> 投影坐标：')
    coords = lonlat2geo(dataset, lon, lat)
    print('(%s, %s)->(%s, %s)' % (lon, lat, coords[0], coords[1]))

    print('图上坐标 -> 投影坐标：')
    coords = imagexy2geo(dataset, row, col)
    print('(%s, %s)->(%s, %s)' % (row, col, coords[0], coords[1]))
    print('投影坐标 -> 图上坐标：')
    coords = geo2imagexy(dataset, x, y)
    print('(%s, %s)->(%s, %s)' % (x, y, coords[0], coords[1]))


    #               栅格数据重投影
    # 栅格数据也可以重投影，但比矢量数据投影更复杂。
    # 栅格数据需要处理栅格数据中像元会弯曲和移动的事实，一对一的映射并不存在
    # 通常用最近邻域插值法、双线性插值和三次卷积插值法进行插值
    # 方法：1.gdalwarp 2.AutoCreateWarpedVRT
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS('WGS84')  # UTM转无投影，即地理坐标系
    old_ds = gdal.Open('nat_color.tif')
    vrt_ds = gdal.AutoCreateWarpedVRT(old_ds, None, srs.ExportToWkt(),
                                      gdal.GRA_Bilinear)  # 第一个默认值None，使用源栅格数据的srs；第二个如果None，表示不发生重投影
    gdal.GetDriverByName('gtiff').CreateCopy('nat_color_wgs84.tif', vrt_ds)  # 该函数返回一个数据集对象，用CreateCopy函数保存为gtiff


    #         GetGeoTransform，在真实坐标和栅格数据坐标具有相同srs情况下，计算坐标偏移。
    # 作用：图像坐标（行列号）和现实世界坐标（投影坐标或地理坐标）之间的转换。是仿射变换，不是投影转换，和上面不同。
    # 0、3 x\y坐标 起始点现实世界坐标  1、5 像素宽度和高度  2、4 x\y方向旋转角
    gt = ds.GetGeoTransform()  # 正变换：图像坐标到现实世界坐标。正变换时输入行列号，输出的现实世界坐标是栅格图像srs下的坐标
    inv_gt = gdal.InvGeoTransform(gt)  # 逆变换：现实世界坐标到图像坐标
    offsets = gdal.ApplyGeoTransform(inv_gt, 465200, 5296000)  # 逆变换：输入的投影坐标具有和栅格图像的相同的srs
    xoff, yoff = map(int, offsets)  # 取整

    #        gdal.Transformer，可计算相同srs下的坐标偏移；不能用于不同srs投影转换
    # 作用：现实世界坐标（投影坐标或地理坐标）与图像坐标（行列号）之间的转换、两个栅格图像之间像素坐标偏移（行列号），如镶嵌#原理就是在相同srs情况下，计算图1的像素坐标到现实世界坐标的偏移，再从现实世界坐标偏移到图2的像素坐标。其实就是两次仿射变换（正、逆），从而把图1的像素坐标偏移到图2的像素坐标。#所以不能用于不同srs情况，因为该函数没有内置不同srs的投影转换公式。只能用于相同srs下，两个栅格数据集坐标的偏移。
    # 这里in_ds和out_ds具有相同srs。转换目的是为了把不同栅格数据的图像坐标（行列号）进行偏移，方便镶嵌
    trans = gdal.Transformer(in_ds, out_ds, [])  # 空白用于设置转换器选项
    success, xyz = trans.TransformPoint(False, 0, 0)  # False基于源数据计算目标栅格，反之为True。起始坐标为左上角 0，0
    x, y, z = map(int, xyz)

    # 图像坐标和现实世界坐标之间转换
    trans = gdal.Transformer(out_ds, None, [])
    success, xyz = trans.TransformPoint(0, 1078, 648)

    #                PROJ（矢量数据投影）
    #作用：投影坐标之间转换、地理坐标和投影坐标之间转换
    import pyproj
    utm_proj = pyproj.Proj('+proj=utm +zone=31 +ellps=WGS84')
    x, y = utm_proj(2.294, 48.858)  #地理坐标转化为投影坐标
    x1, y1 = utm_proj(x, y, inverse=True)  #逆变换
    wgs84 = pyproj.Proj('')
    nad27 = pyproj.Proj('')
    x, y = pyproj.transform(wgs84, nad27, 580744, 4504695) #投影坐标之间转换

    #               OSR（矢量数据投影）
    # 作用：投影坐标系之间转换、地理坐标和投影坐标之间转换
    # 可用于几何对象和点（点属于几何对象）
    from osgeo import gdal
    import osr

    peters_sr = osr.SpatialReference()
    peters_sr.ImportFromProj4('...')
    ct = osr.CoordinateTransformation(web_mercator_sr, peters_sr)
    # world对象为web_mercator_sr投影，但没有分配srs
    world.Transform(ct)
    # 对几何对象的转换
    ct.TransformPoint(x, y)
    # 对点的转换

    # 如果几何对象分配有srs，转换方法如下
    world.TransformTo(web_mercator_sr)

    # 读取投影的地理基准，用于和地理坐标进行转换
    geosrs = peters_sr.CloneGeogCS()


