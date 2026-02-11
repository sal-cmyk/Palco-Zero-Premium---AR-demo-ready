#!/usr/bin/env python3
"""
Convert GLB to USDZ for iOS Quick Look
Uses OBJ as intermediate format
"""

import trimesh
from pathlib import Path
import zipfile
import shutil

# Paths
GLB_PATH = Path("/home/ubuntu/palco-zero-premium/public/assets/can/product.glb")
OUTPUT_DIR = Path("/home/ubuntu/palco-zero-premium/public/assets/can")
USDZ_PATH = OUTPUT_DIR / "product.usdz"
TEMP_DIR = Path("/tmp/usdz_conversion")

print("🔄 Converting GLB to USDZ...")

# Clean temp directory
if TEMP_DIR.exists():
    shutil.rmtree(TEMP_DIR)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load GLB
print(f"📂 Loading GLB: {GLB_PATH}")
mesh = trimesh.load(str(GLB_PATH))

# 2. Export to OBJ (with textures)
obj_path = TEMP_DIR / "model.obj"
print(f"📝 Exporting to OBJ: {obj_path}")

# Export mesh to OBJ
mesh.export(str(obj_path), file_type='obj', include_texture=True)

# 3. Copy textures to temp directory
print("🎨 Copying textures...")
texture_files = list(OUTPUT_DIR.glob("texture_*.png"))
for texture_file in texture_files:
    dest = TEMP_DIR / texture_file.name
    shutil.copy(texture_file, dest)
    print(f"   ✅ {texture_file.name}")

# 4. Create USDZ (ZIP archive with .usdz extension)
print(f"📦 Creating USDZ archive: {USDZ_PATH}")

with zipfile.ZipFile(USDZ_PATH, 'w', zipfile.ZIP_DEFLATED) as usdz:
    # Add OBJ file
    usdz.write(obj_path, "model.obj")
    
    # Add MTL file if exists
    mtl_path = TEMP_DIR / "model.mtl"
    if mtl_path.exists():
        usdz.write(mtl_path, "model.mtl")
    
    # Add textures
    for texture_file in TEMP_DIR.glob("*.png"):
        usdz.write(texture_file, texture_file.name)

usdz_size = USDZ_PATH.stat().st_size
print(f"✅ USDZ created: {USDZ_PATH} ({usdz_size / 1024:.2f} KB)")

# Clean up temp directory
shutil.rmtree(TEMP_DIR)

print("\n🎉 Conversion complete!")
print(f"   USDZ: {USDZ_PATH}")
print(f"   Size: {usdz_size / 1024:.2f} KB")
