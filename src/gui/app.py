"""
GUI Application for 2D to 3D conversion using SAM 3D Objects
"""
import gradio as gr
import numpy as np
from PIL import Image
import os
import sys
from pathlib import Path
import cv2

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sam_integration.sam_processor import SAMProcessor
from mesh_processing.mesh_converter import MeshConverter


class App:
    def __init__(self):
        self.sam_processor = SAMProcessor()
        self.mesh_converter = MeshConverter()
        self.current_image = None
        self.selected_points = []

    def process_image_click(self, image, evt: gr.SelectData):
        """Handle image click events to collect coordinates"""
        if image is None:
            return None, "Please upload an image first"

        # Store the image
        self.current_image = image

        # Get clicked coordinates
        x, y = evt.index[0], evt.index[1]
        self.selected_points.append((x, y))

        # Draw points on image
        img_array = np.array(image)
        for point in self.selected_points:
            px, py = point
            # Draw a circle at the clicked point
            cv2.circle(img_array, (px, py), 5, (255, 0, 0), -1)

        status = f"Selected {len(self.selected_points)} point(s). Last point: ({x}, {y})"
        return Image.fromarray(img_array), status

    def clear_points(self):
        """Clear all selected points"""
        self.selected_points = []
        if self.current_image is not None:
            return self.current_image, "Points cleared"
        return None, "Points cleared"

    def generate_3d(self, image, progress=gr.Progress()):
        """Generate 3D model from image and selected points"""
        if image is None:
            return None, None, "Please upload an image first"

        if len(self.selected_points) == 0:
            return None, None, "Please select at least one point on the image"

        try:
            progress(0.1, desc="Generating mask from points...")

            # Generate mask from selected points
            mask = self.sam_processor.generate_mask(image, self.selected_points)

            progress(0.3, desc="Running SAM 3D Objects inference...")

            # Generate point cloud using SAM 3D Objects
            ply_path = self.sam_processor.generate_point_cloud(
                image,
                mask,
                output_dir="data/output"
            )

            progress(0.7, desc="Converting to watertight mesh...")

            # Convert point cloud to watertight mesh
            mesh_path = self.mesh_converter.convert_to_watertight_mesh(
                ply_path,
                output_dir="data/output"
            )

            progress(1.0, desc="Complete!")

            return ply_path, mesh_path, f"Success! Generated:\n- Point cloud: {ply_path}\n- Mesh: {mesh_path}"

        except Exception as e:
            return None, None, f"Error: {str(e)}"

    def launch(self):
        """Launch the Gradio interface"""
        with gr.Blocks(title="2D to 3D Converter") as demo:
            gr.Markdown("# 2D to 3D Converter using SAM 3D Objects")
            gr.Markdown("""
            Upload an image and click on the object you want to convert to 3D.
            The application will:
            1. Generate a mask from your selected points
            2. Use SAM 3D Objects to create a point cloud (.ply)
            3. Convert the point cloud to a watertight mesh
            """)

            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(
                        label="Upload Image",
                        type="pil",
                        interactive=True
                    )

                    with gr.Row():
                        clear_btn = gr.Button("Clear Points")
                        generate_btn = gr.Button("Generate 3D Model", variant="primary")

                    status_text = gr.Textbox(
                        label="Status",
                        value="Upload an image and click to select points",
                        interactive=False
                    )

                with gr.Column():
                    annotated_image = gr.Image(
                        label="Image with Selected Points",
                        type="pil",
                        interactive=False
                    )

            with gr.Row():
                ply_output = gr.File(label="Point Cloud (.ply)")
                mesh_output = gr.File(label="Watertight Mesh")

            # Event handlers
            input_image.select(
                self.process_image_click,
                inputs=[input_image],
                outputs=[annotated_image, status_text]
            )

            clear_btn.click(
                self.clear_points,
                outputs=[annotated_image, status_text]
            )

            generate_btn.click(
                self.generate_3d,
                inputs=[input_image],
                outputs=[ply_output, mesh_output, status_text]
            )

        demo.launch(share=False)


if __name__ == "__main__":
    app = App()
    app.launch()
