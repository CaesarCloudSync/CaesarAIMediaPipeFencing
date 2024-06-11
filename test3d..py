import numpy as np
import open3d as o3d

def main():
    pts = np.random.randint(0, 100, (100, 3))

    # whether to write in binary or text format
    write_text = True

    # use open3d
    use_o3d(pts, write_text)


def use_o3d(pts, write_text):
    pcd = o3d.geometry.PointCloud()

    # the method Vector3dVector() will convert numpy array of shape (n, 3) to Open3D format.
    # see http://www.open3d.org/docs/release/python_api/open3d.utility.Vector3dVector.html#open3d.utility.Vector3dVector
    pcd.points = o3d.utility.Vector3dVector(pts)

    # http://www.open3d.org/docs/release/python_api/open3d.io.write_point_cloud.html#open3d.io.write_point_cloud
    o3d.io.write_point_cloud("my_pts.ply", pcd, write_ascii=write_text)

    # read ply file
    pcd = o3d.io.read_point_cloud('my_pts.ply')

    # visualize
    # o3d.visualization.draw_geometries([pcd])
