#!/usr/bin/env python3
"""
Generate NEON FLOW 3D can model with real label texture
"""

import trimesh
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import pygltflib
from pathlib import Path

# Paths
REFERENCE_IMAGE = Path("/home/ubuntu/palco-zero-premium/neon_flow_reference.webp")
OUTPUT_DIR = Path("/home/ubuntu/palco-zero-premium/public/assets/can")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Can dimensions (realistic energy drink can)
CAN_RADIUS = 0.031  # 31mm radius (62mm diameter)
CAN_HEIGHT = 0.168  # 168mm height (standard 500ml can)
SEGMENTS = 64  # Smooth cylinder

print("🎨 Generating NEON FLOW 3D Can Model...")

# 1. Load and process reference image
print("📸 Loading reference image...")
ref_img = Image.open(REFERENCE_IMAGE).convert("RGBA")
print(f"   Reference image size: {ref_img.size}")

# 2. Extract label from reference (crop to can body, remove top/bottom)
# The reference shows a full can, we need to extract just the label wrap
img_width, img_height = ref_img.size

# Estimate can body region (exclude top and bottom caps)
# Typical can: top 10%, body 80%, bottom 10%
label_top = int(img_height * 0.12)
label_bottom = int(img_height * 0.88)
label_crop = ref_img.crop((0, label_top, img_width, label_bottom))

print(f"   Extracted label region: {label_crop.size}")

# 3. Create cylindrical UV texture map (1024x512 for performance)
TEXTURE_WIDTH = 1024
TEXTURE_HEIGHT = 512

# Resize label to fit texture
label_resized = label_crop.resize((TEXTURE_WIDTH, TEXTURE_HEIGHT), Image.Resampling.LANCZOS)

# Create base texture with metallic background
base_texture = Image.new("RGBA", (TEXTURE_WIDTH, TEXTURE_HEIGHT), (40, 40, 60, 255))

# Composite label onto base
base_texture.paste(label_resized, (0, 0), label_resized)

# Save base color texture
texture_path = OUTPUT_DIR / "texture_base.png"
base_texture.save(texture_path, "PNG", optimize=True)
print(f"✅ Base texture saved: {texture_path} ({texture_path.stat().st_size // 1024} KB)")

# 4. Create metallic-roughness texture
metallic_roughness = Image.new("RGB", (TEXTURE_WIDTH, TEXTURE_HEIGHT), (255, 100, 0))  # Full metallic, low roughness
mr_path = OUTPUT_DIR / "texture_metallic_roughness.png"
metallic_roughness.save(mr_path, "PNG", optimize=True)
print(f"✅ Metallic-Roughness texture saved: {mr_path}")

# 5. Create emissive texture (neon glow from label)
# Extract bright areas from label for emissive
emissive = label_resized.copy()
emissive_data = np.array(emissive)

# Boost bright cyan/magenta areas
emissive_data[:, :, 0] = np.clip(emissive_data[:, :, 0] * 0.3, 0, 255)  # Reduce red
emissive_data[:, :, 1] = np.clip(emissive_data[:, :, 1] * 1.2, 0, 255)  # Boost green (cyan)
emissive_data[:, :, 2] = np.clip(emissive_data[:, :, 2] * 1.5, 0, 255)  # Boost blue (neon)

emissive_img = Image.fromarray(emissive_data.astype(np.uint8))
emissive_img = emissive_img.filter(ImageFilter.GaussianBlur(radius=3))  # Soft glow

emissive_path = OUTPUT_DIR / "texture_emissive.png"
emissive_img.save(emissive_path, "PNG", optimize=True)
print(f"✅ Emissive texture saved: {emissive_path}")

# 6. Create cylinder geometry with proper UV mapping
print("🔨 Creating cylinder geometry...")

# Create cylinder using trimesh
cylinder = trimesh.creation.cylinder(
    radius=CAN_RADIUS,
    height=CAN_HEIGHT,
    sections=SEGMENTS
)

# Rotate to stand upright (trimesh creates horizontal cylinder)
rotation_matrix = trimesh.transformations.rotation_matrix(
    angle=np.pi / 2,
    direction=[1, 0, 0],
    point=[0, 0, 0]
)
cylinder.apply_transform(rotation_matrix)

# Center at origin
cylinder.vertices[:, 2] -= CAN_HEIGHT / 2

print(f"   Vertices: {len(cylinder.vertices)}, Faces: {len(cylinder.faces)}")

# 7. Generate cylindrical UV coordinates
vertices = cylinder.vertices
uvs = np.zeros((len(vertices), 2), dtype=np.float32)

for i, vertex in enumerate(vertices):
    x, y, z = vertex
    
    # Cylindrical UV mapping
    # U: angle around cylinder (0 to 1)
    angle = np.arctan2(y, x)
    u = (angle + np.pi) / (2 * np.pi)
    
    # V: height (0 at bottom, 1 at top)
    v = (z + CAN_HEIGHT / 2) / CAN_HEIGHT
    
    uvs[i] = [u, v]

print(f"✅ UV coordinates generated: {uvs.shape}")

# 8. Create trimesh with UVs
mesh = trimesh.Trimesh(
    vertices=cylinder.vertices,
    faces=cylinder.faces,
    visual=trimesh.visual.TextureVisuals(
        uv=uvs,
        image=base_texture
    )
)

# 9. Export to GLB with PBR materials
print("💾 Exporting GLB...")

# Create material
material = trimesh.visual.material.PBRMaterial(
    baseColorTexture=base_texture,
    metallicRoughnessTexture=metallic_roughness,
    emissiveTexture=emissive_img,
    emissiveFactor=[0.3, 0.3, 0.4],  # Subtle neon glow
    metallicFactor=0.9,
    roughnessFactor=0.2
)

mesh.visual = trimesh.visual.TextureVisuals(
    uv=uvs,
    material=material
)

# Export GLB
glb_path = OUTPUT_DIR / "product.glb"
mesh.export(str(glb_path), file_type='glb')

glb_size = glb_path.stat().st_size
print(f"✅ GLB exported: {glb_path} ({glb_size / 1024:.2f} KB)")

if glb_size > 2 * 1024 * 1024:
    print(f"⚠️  Warning: GLB size ({glb_size / 1024 / 1024:.2f} MB) exceeds 2MB target!")

# 10. Update poster
print("🖼️  Copying poster...")
poster_path = OUTPUT_DIR / "poster.webp"
ref_img.save(poster_path, "WEBP", quality=85)
print(f"✅ Poster saved: {poster_path}")

print("\n🎉 NEON FLOW 3D Can Model Generated Successfully!")
print(f"   GLB: {glb_path}")
print(f"   Poster: {poster_path}")
print(f"   Textures: {OUTPUT_DIR}")
