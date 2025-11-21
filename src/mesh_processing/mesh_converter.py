"""
Mesh processing utilities for converting point clouds to watertight meshes
"""
import numpy as np
import open3d as o3d
import trimesh
import os
from pathlib import Path
from typing import Optional, Tuple


class MeshConverter:
    """Converts point clouds to watertight meshes"""

    def __init__(self):
        """Initialize mesh converter"""
        self.default_depth = 9  # Poisson reconstruction depth
        self.default_scale = 1.1  # Scale factor for reconstruction

    def load_point_cloud(self, ply_path: str) -> o3d.geometry.PointCloud:
        """
        Load point cloud from PLY file

        Args:
            ply_path: Path to .ply file

        Returns:
            Open3D PointCloud object
        """
        pcd = o3d.io.read_point_cloud(ply_path)
        print(f"Loaded point cloud with {len(pcd.points)} points")
        return pcd

    def estimate_normals(self, pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Estimate normals for point cloud

        Args:
            pcd: Input point cloud

        Returns:
            Point cloud with estimated normals
        """
        print("Estimating normals...")

        # Estimate radius for normal computation
        distances = pcd.compute_nearest_neighbor_distance()
        avg_dist = np.mean(distances)
        radius = avg_dist * 2

        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=radius,
                max_nn=30
            )
        )

        # Orient normals consistently
        pcd.orient_normals_consistent_tangent_plane(k=15)

        return pcd

    def poisson_reconstruction(
        self,
        pcd: o3d.geometry.PointCloud,
        depth: int = 9,
        width: int = 0,
        scale: float = 1.1,
        linear_fit: bool = False
    ) -> Tuple[o3d.geometry.TriangleMesh, np.ndarray]:
        """
        Perform Poisson surface reconstruction

        Args:
            pcd: Input point cloud with normals
            depth: Maximum depth of the octree (higher = more detail)
            width: Target width of the finest level octree cells
            scale: Ratio between the diameter of the cube used for
                   reconstruction and the diameter of the samples
            linear_fit: Use linear interpolation

        Returns:
            Tuple of (reconstructed mesh, vertex densities)
        """
        print(f"Running Poisson reconstruction (depth={depth})...")

        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd,
            depth=depth,
            width=width,
            scale=scale,
            linear_fit=linear_fit
        )

        print(f"Reconstructed mesh with {len(mesh.vertices)} vertices "
              f"and {len(mesh.triangles)} triangles")

        return mesh, densities

    def clean_mesh(
        self,
        mesh: o3d.geometry.TriangleMesh,
        densities: Optional[np.ndarray] = None,
        density_threshold: float = 0.01
    ) -> o3d.geometry.TriangleMesh:
        """
        Clean and filter mesh

        Args:
            mesh: Input mesh
            densities: Vertex densities from Poisson reconstruction
            density_threshold: Threshold for removing low-density vertices

        Returns:
            Cleaned mesh
        """
        print("Cleaning mesh...")

        # Remove low-density vertices if densities are provided
        if densities is not None:
            vertices_to_remove = densities < np.quantile(densities, density_threshold)
            mesh.remove_vertices_by_mask(vertices_to_remove)

        # Remove degenerate triangles
        mesh.remove_degenerate_triangles()
        mesh.remove_duplicated_triangles()
        mesh.remove_duplicated_vertices()
        mesh.remove_non_manifold_edges()

        print(f"Cleaned mesh: {len(mesh.vertices)} vertices, "
              f"{len(mesh.triangles)} triangles")

        return mesh

    def make_watertight(
        self,
        mesh: o3d.geometry.TriangleMesh,
        resolution: int = 20000
    ) -> trimesh.Trimesh:
        """
        Convert mesh to watertight using voxelization

        Args:
            mesh: Input mesh
            resolution: Voxel resolution for watertightness

        Returns:
            Watertight trimesh
        """
        print("Making mesh watertight...")

        # Convert Open3D mesh to trimesh
        vertices = np.asarray(mesh.vertices)
        triangles = np.asarray(mesh.triangles)
        tri_mesh = trimesh.Trimesh(vertices=vertices, faces=triangles)

        # Method 1: Try to fill holes
        if not tri_mesh.is_watertight:
            print("Mesh is not watertight, attempting to fix...")
            trimesh.repair.fill_holes(tri_mesh)

        # Method 2: If still not watertight, use voxelization
        if not tri_mesh.is_watertight:
            print("Using voxelization to ensure watertightness...")

            # Create voxelized version
            pitch = tri_mesh.bounding_box.extents.max() / resolution
            voxelized = tri_mesh.voxelized(pitch=pitch)

            # Convert back to mesh
            tri_mesh = voxelized.as_boxes().to_mesh()

            # Smooth the voxelized mesh
            tri_mesh = trimesh.smoothing.filter_laplacian(tri_mesh)

        if tri_mesh.is_watertight:
            print("Mesh is now watertight!")
        else:
            print("Warning: Mesh may not be fully watertight")

        return tri_mesh

    def save_mesh(
        self,
        mesh: trimesh.Trimesh,
        output_path: str,
        file_format: str = "obj"
    ) -> str:
        """
        Save mesh to file

        Args:
            mesh: Input mesh
            output_path: Output file path
            file_format: Output format (obj, ply, stl, etc.)

        Returns:
            Path to saved mesh file
        """
        # Ensure correct extension
        output_path = str(Path(output_path).with_suffix(f".{file_format}"))

        mesh.export(output_path)
        print(f"Mesh saved to: {output_path}")

        return output_path

    def convert_to_watertight_mesh(
        self,
        ply_path: str,
        output_dir: str = "data/output",
        depth: int = 9,
        clean: bool = True,
        output_format: str = "obj"
    ) -> str:
        """
        Complete pipeline: Convert point cloud to watertight mesh

        Args:
            ply_path: Path to input .ply point cloud file
            output_dir: Output directory
            depth: Poisson reconstruction depth
            clean: Whether to clean the mesh
            output_format: Output file format

        Returns:
            Path to output watertight mesh file
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Step 1: Load point cloud
        pcd = self.load_point_cloud(ply_path)

        # Step 2: Estimate normals if not present
        if not pcd.has_normals():
            pcd = self.estimate_normals(pcd)

        # Step 3: Poisson reconstruction
        mesh, densities = self.poisson_reconstruction(pcd, depth=depth)

        # Step 4: Clean mesh
        if clean:
            mesh = self.clean_mesh(mesh, densities)

        # Step 5: Make watertight
        tri_mesh = self.make_watertight(mesh)

        # Step 6: Save mesh
        base_name = Path(ply_path).stem
        output_path = os.path.join(output_dir, f"{base_name}_watertight.{output_format}")
        output_path = self.save_mesh(tri_mesh, output_path, output_format)

        # Print mesh statistics
        print(f"\nFinal mesh statistics:")
        print(f"  - Vertices: {len(tri_mesh.vertices)}")
        print(f"  - Faces: {len(tri_mesh.faces)}")
        print(f"  - Watertight: {tri_mesh.is_watertight}")
        print(f"  - Volume: {tri_mesh.volume:.4f}")
        print(f"  - Surface area: {tri_mesh.area:.4f}")

        return output_path

    def visualize_mesh(self, mesh_path: str):
        """
        Visualize mesh using Open3D viewer

        Args:
            mesh_path: Path to mesh file
        """
        mesh = trimesh.load(mesh_path)

        # Convert to Open3D for visualization
        o3d_mesh = o3d.geometry.TriangleMesh()
        o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
        o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)
        o3d_mesh.compute_vertex_normals()

        o3d.visualization.draw_geometries([o3d_mesh])
