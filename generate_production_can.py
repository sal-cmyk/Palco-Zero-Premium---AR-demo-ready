#!/usr/bin/env python3
"""
PALCO ZERO - PRODUCTION CAN MODEL GENERATOR
Generates professional low-poly can with PBR materials and optimized textures
Target: GLB < 2MB, USDZ-ready, iOS + Android compatible
"""

import trimesh
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pygltflib
from pathlib import Path
import json

# Configuration
OUTPUT_DIR = Path("assets/can")
TEXTURE_SIZE = 512  # 512x512 texture (optimized for < 2MB target)
CAN_HEIGHT = 0.15  # 15cm (standard 330ml can)
CAN_RADIUS = 0.03  # 3cm radius
SEGMENTS = 32  # Low-poly but smooth enough

def create_can_geometry():
    """Create low-poly cylindrical can with proper UV mapping"""
    print("Creating can geometry...")
    
    # Create cylinder body
    cylinder = trimesh.creation.cylinder(
        radius=CAN_RADIUS,
        height=CAN_HEIGHT,
        sections=SEGMENTS
    )
    
    # Ensure proper normals
    cylinder.fix_normals()
    
    # Generate cylindrical UV mapping
    vertices = cylinder.vertices
    uvs = np.zeros((len(vertices), 2))
    
    for i, vertex in enumerate(vertices):
        x, y, z = vertex
        
        # Cylindrical unwrap
        angle = np.arctan2(x, z)
        u = (angle + np.pi) / (2 * np.pi)  # 0-1 range
        
        # Vertical coordinate (normalized height)
        v = (y + CAN_HEIGHT/2) / CAN_HEIGHT  # 0-1 range
        
        uvs[i] = [u, v]
    
    # Store UVs in visual
    cylinder.visual = trimesh.visual.TextureVisuals(uv=uvs)
    
    print(f"✓ Geometry created: {len(cylinder.vertices)} vertices, {len(cylinder.faces)} faces")
    return cylinder

def create_neon_flow_texture():
    """Create NEON FLOW label texture with gradient and typography"""
    print("Creating NEON FLOW texture...")
    
    # Create base image
    img = Image.new('RGBA', (TEXTURE_SIZE, TEXTURE_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create neon gradient background (blue to pink)
    for y in range(TEXTURE_SIZE):
        # Gradient from electric blue to neon pink
        ratio = y / TEXTURE_SIZE
        r = int(0 + (255 - 0) * ratio)  # 0 -> 255
        g = int(100 + (50 - 100) * ratio)  # 100 -> 50
        b = int(255 + (150 - 255) * ratio)  # 255 -> 150
        
        draw.rectangle([(0, y), (TEXTURE_SIZE, y+1)], fill=(r, g, b, 255))
    
    # Add subtle noise/texture
    pixels = np.array(img)
    noise = np.random.randint(-10, 10, pixels.shape, dtype=np.int16)
    pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(pixels)
    
    # Add text overlay (NEON FLOW)
    draw = ImageDraw.Draw(img)
    
    # Try to use a bold font, fallback to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw "NEON" text (centered, upper)
    text1 = "NEON"
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    text1_width = bbox1[2] - bbox1[0]
    text1_height = bbox1[3] - bbox1[1]
    x1 = (TEXTURE_SIZE - text1_width) // 2
    y1 = TEXTURE_SIZE // 3 - text1_height // 2
    
    # Draw with outline for visibility
    outline_color = (0, 0, 0, 255)
    text_color = (255, 255, 255, 255)
    
    for offset_x in [-2, 0, 2]:
        for offset_y in [-2, 0, 2]:
            draw.text((x1 + offset_x, y1 + offset_y), text1, font=font_large, fill=outline_color)
    draw.text((x1, y1), text1, font=font_large, fill=text_color)
    
    # Draw "FLOW" text (centered, lower)
    text2 = "FLOW"
    bbox2 = draw.textbbox((0, 0), text2, font=font_large)
    text2_width = bbox2[2] - bbox2[0]
    text2_height = bbox2[3] - bbox2[1]
    x2 = (TEXTURE_SIZE - text2_width) // 2
    y2 = 2 * TEXTURE_SIZE // 3 - text2_height // 2
    
    for offset_x in [-2, 0, 2]:
        for offset_y in [-2, 0, 2]:
            draw.text((x2 + offset_x, y2 + offset_y), text2, font=font_large, fill=outline_color)
    draw.text((x2, y2), text2, font=font_large, fill=text_color)
    
    # Apply subtle blur for premium feel
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    print(f"✓ Texture created: {TEXTURE_SIZE}x{TEXTURE_SIZE}px")
    return img

def create_metallic_roughness_map():
    """Create metallic-roughness map for PBR material"""
    print("Creating metallic-roughness map...")
    
    # Create image (B=metallic, G=roughness)
    img = Image.new('RGB', (TEXTURE_SIZE, TEXTURE_SIZE), (0, 0, 0))
    pixels = np.array(img)
    
    # Blue channel = metallic (high for aluminum can)
    pixels[:, :, 2] = 230  # 0.9 metallic (230/255)
    
    # Green channel = roughness (low for shiny can)
    pixels[:, :, 1] = 64  # 0.25 roughness (64/255)
    
    # Add subtle variation
    noise = np.random.randint(-5, 5, pixels.shape, dtype=np.int16)
    pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    img = Image.fromarray(pixels)
    print(f"✓ Metallic-roughness map created")
    return img

def create_emissive_map():
    """Create emissive map for subtle neon glow"""
    print("Creating emissive map...")
    
    # Create base image
    img = Image.new('RGB', (TEXTURE_SIZE, TEXTURE_SIZE), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Subtle gradient glow (very low intensity)
    for y in range(TEXTURE_SIZE):
        ratio = y / TEXTURE_SIZE
        # Very subtle blue to pink glow
        r = int(0 + (30 - 0) * ratio)  # Max 30 (subtle)
        g = int(10 + (5 - 10) * ratio)
        b = int(30 + (20 - 30) * ratio)
        
        draw.rectangle([(0, y), (TEXTURE_SIZE, y+1)], fill=(r, g, b))
    
    print(f"✓ Emissive map created (subtle glow)")
    return img

def export_glb(mesh, base_color_tex, metallic_roughness_tex, emissive_tex):
    """Export mesh as GLB with PBR materials and textures"""
    print("Exporting GLB...")
    
    # Create material with PIL Image objects directly
    material = trimesh.visual.material.PBRMaterial(
        baseColorTexture=base_color_tex,
        metallicRoughnessTexture=metallic_roughness_tex,
        emissiveTexture=emissive_tex,
        emissiveFactor=[1.0, 1.0, 1.0],  # Full emissive strength
        metallicFactor=0.9,
        roughnessFactor=0.25,
        doubleSided=False
    )
    
    # Apply material to mesh
    mesh.visual = trimesh.visual.TextureVisuals(
        uv=mesh.visual.uv,
        material=material
    )
    
    # Export as GLB
    glb_path = OUTPUT_DIR / "product.glb"
    mesh.export(str(glb_path), file_type='glb')
    
    # Check file size
    size_mb = glb_path.stat().st_size / (1024 * 1024)
    print(f"✓ GLB exported: {glb_path} ({size_mb:.2f} MB)")
    
    return glb_path, size_mb

def optimize_glb(glb_path):
    """Optimize GLB file size by compressing textures if needed"""
    print("Optimizing GLB...")
    
    # Load GLB
    gltf = pygltflib.GLTF2().load(str(glb_path))
    
    # Check if optimization needed
    size_mb = glb_path.stat().st_size / (1024 * 1024)
    
    if size_mb > 2.0:
        print(f"⚠ GLB too large ({size_mb:.2f} MB), compressing textures...")
        
        # Reduce texture size to 512x512
        # This would require re-generating textures at lower resolution
        # For now, we'll just warn
        print("⚠ Manual texture reduction may be needed")
    else:
        print(f"✓ GLB size OK ({size_mb:.2f} MB < 2 MB)")
    
    return size_mb

def generate_usdz_placeholder(glb_path):
    """Generate USDZ placeholder (requires external conversion)"""
    print("Generating USDZ placeholder...")
    
    usdz_path = OUTPUT_DIR / "product.usdz"
    
    # Create empty placeholder
    usdz_path.touch()
    
    print(f"⚠ USDZ placeholder created: {usdz_path}")
    print(f"  Convert GLB → USDZ using:")
    print(f"  - Reality Converter (macOS)")
    print(f"  - Blender 3.0+ (File → Export → USD)")
    print(f"  - Online tool: https://www.vectary.com/")
    
    return usdz_path

def create_poster_render():
    """Create poster image from 3D model (simplified version)"""
    print("Creating poster render...")
    
    # For now, reuse the texture as poster
    # In production, this would be a proper 3D render
    poster_path = OUTPUT_DIR / "poster.webp"
    
    # Create a simple poster with the texture
    texture = create_neon_flow_texture()
    
    # Resize to poster dimensions (1536x2752)
    poster = Image.new('RGBA', (1536, 2752), (20, 20, 30, 255))
    
    # Place texture in center (simulating can view)
    can_width = 800
    can_height = 1600
    texture_resized = texture.resize((can_width, can_height), Image.Resampling.LANCZOS)
    
    x = (1536 - can_width) // 2
    y = (2752 - can_height) // 2
    
    poster.paste(texture_resized, (x, y), texture_resized)
    
    # Save as WebP
    poster.save(poster_path, 'WEBP', quality=85)
    
    size_mb = poster_path.stat().st_size / (1024 * 1024)
    print(f"✓ Poster created: {poster_path} ({size_mb:.2f} MB)")
    
    return poster_path

def main():
    """Main execution"""
    print("=" * 60)
    print("PALCO ZERO - PRODUCTION CAN MODEL GENERATOR")
    print("=" * 60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Create geometry
    can_mesh = create_can_geometry()
    
    # Step 2: Create textures
    base_color_tex = create_neon_flow_texture()
    metallic_roughness_tex = create_metallic_roughness_map()
    emissive_tex = create_emissive_map()
    
    # Step 3: Export GLB
    glb_path, size_mb = export_glb(
        can_mesh,
        base_color_tex,
        metallic_roughness_tex,
        emissive_tex
    )
    
    # Step 4: Optimize if needed
    optimize_glb(glb_path)
    
    # Step 5: Generate USDZ placeholder
    usdz_path = generate_usdz_placeholder(glb_path)
    
    # Step 6: Create poster
    poster_path = create_poster_render()
    
    # Summary
    print("=" * 60)
    print("✓ PRODUCTION CAN MODEL GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"GLB:    {glb_path} ({size_mb:.2f} MB)")
    print(f"USDZ:   {usdz_path} (placeholder - convert manually)")
    print(f"Poster: {poster_path}")
    print()
    print("Next steps:")
    print("1. Convert GLB → USDZ using Reality Converter or Blender")
    print("2. Test in Safari iOS (Quick Look)")
    print("3. Test in Chrome Android (Scene Viewer)")
    print("4. Integrate with model-viewer in HTML")
    print("=" * 60)

if __name__ == "__main__":
    main()
