#!/usr/bin/env python3
"""
PALCO ZERO PREMIUM - 3D MODEL GENERATOR
Professional pipeline: UV mapping + PBR materials + GLB/USDZ export
"""

import trimesh
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pygltflib
import os

def create_can_model(output_path="models/can.glb", texture_size=1024):
    """
    Create a premium can model with proper UV mapping and PBR material
    """
    print("Creating can model...")
    
    # Create cylinder (can body)
    can = trimesh.creation.cylinder(
        radius=0.033,  # 66mm diameter (standard energy drink can)
        height=0.168,  # 168mm height
        sections=64    # High poly for smooth curves
    )
    
    # Generate UV coordinates (cylindrical unwrap)
    vertices = can.vertices
    uv_coords = []
    
    for v in vertices:
        x, y, z = v
        # Cylindrical UV mapping
        u = np.arctan2(x, z) / (2 * np.pi) + 0.5  # 0 to 1
        v_coord = (y + 0.084) / 0.168  # Normalize height to 0-1
        uv_coords.append([u, v_coord])
    
    # Create texture (label wrap)
    texture = Image.new('RGBA', (texture_size, texture_size), (20, 20, 25, 255))
    draw = ImageDraw.Draw(texture)
    
    # Gradient background (dark to darker)
    for y in range(texture_size):
        alpha = int(255 * (1 - y / texture_size))
        color = (30 + alpha // 10, 30 + alpha // 10, 35 + alpha // 10, 255)
        draw.line([(0, y), (texture_size, y)], fill=color, width=1)
    
    # Neon accent lines
    accent_color = (255, 20, 147, 255)  # Hot pink
    draw.rectangle([texture_size//4, texture_size//3, 3*texture_size//4, texture_size//3 + 20], 
                   fill=accent_color)
    
    # Label text (NEON FLOW)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    text = "NEON FLOW"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (texture_size - text_width) // 2
    y = texture_size // 2 - text_height // 2
    
    # Text with glow effect
    for offset in range(5, 0, -1):
        glow_alpha = int(255 * (offset / 5) * 0.3)
        glow_color = (255, 100, 200, glow_alpha)
        draw.text((x + offset, y + offset), text, font=font, fill=glow_color)
    
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    # Save texture
    texture_path = output_path.replace('.glb', '_texture.png')
    texture.save(texture_path)
    print(f"✓ Texture saved: {texture_path}")
    
    # Create PBR material
    material = trimesh.visual.material.PBRMaterial(
        baseColorTexture=texture,
        metallicFactor=0.9,  # High metallic for can
        roughnessFactor=0.2,  # Smooth surface
        emissiveFactor=[0.1, 0.0, 0.05]  # Subtle neon glow
    )
    
    # Apply material and UV
    can.visual = trimesh.visual.TextureVisuals(
        uv=np.array(uv_coords),
        material=material
    )
    
    # Export GLB
    can.export(output_path)
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✓ Can GLB exported: {output_path} ({file_size:.2f} MB)")
    
    return output_path

def create_pouch_model(output_path="models/cookie-pack.glb", texture_size=1024):
    """
    Create a premium pouch/pack model with proper UV mapping and PBR material
    """
    print("Creating pouch model...")
    
    # Create box (pouch/pack)
    pouch = trimesh.creation.box(
        extents=[0.12, 0.18, 0.04]  # 120x180x40mm (standard snack pack)
    )
    
    # Generate UV coordinates (box unwrap)
    vertices = pouch.vertices
    uv_coords = []
    
    for v in vertices:
        x, y, z = v
        # Simple planar UV mapping
        u = (x + 0.06) / 0.12  # Normalize to 0-1
        v_coord = (y + 0.09) / 0.18  # Normalize to 0-1
        uv_coords.append([u, v_coord])
    
    # Create texture (label)
    texture = Image.new('RGBA', (texture_size, texture_size), (40, 35, 50, 255))
    draw = ImageDraw.Draw(texture)
    
    # Gradient background (purple to dark)
    for y in range(texture_size):
        alpha = int(255 * (1 - y / texture_size))
        color = (50 + alpha // 8, 40 + alpha // 10, 60 + alpha // 8, 255)
        draw.line([(0, y), (texture_size, y)], fill=color, width=1)
    
    # Neon accent
    accent_color = (255, 140, 0, 255)  # Orange
    draw.ellipse([texture_size//4, texture_size//4, 3*texture_size//4, 3*texture_size//4],
                 outline=accent_color, width=10)
    
    # Label text
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    text = "BISCOITO\nPREMIUM"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (texture_size - text_width) // 2
    y = texture_size // 2 - text_height // 2
    
    # Text with glow
    for offset in range(4, 0, -1):
        glow_alpha = int(255 * (offset / 4) * 0.3)
        glow_color = (255, 180, 100, glow_alpha)
        draw.text((x + offset, y + offset), text, font=font, fill=glow_color)
    
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255), align='center')
    
    # Save texture
    texture_path = output_path.replace('.glb', '_texture.png')
    texture.save(texture_path)
    print(f"✓ Texture saved: {texture_path}")
    
    # Create PBR material
    material = trimesh.visual.material.PBRMaterial(
        baseColorTexture=texture,
        metallicFactor=0.1,  # Low metallic for plastic
        roughnessFactor=0.6,  # Semi-rough plastic
        emissiveFactor=[0.05, 0.03, 0.0]  # Subtle warm glow
    )
    
    # Apply material and UV
    pouch.visual = trimesh.visual.TextureVisuals(
        uv=np.array(uv_coords),
        material=material
    )
    
    # Export GLB
    pouch.export(output_path)
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✓ Pouch GLB exported: {output_path} ({file_size:.2f} MB)")
    
    return output_path

def convert_glb_to_usdz(glb_path):
    """
    Convert GLB to USDZ for iOS Quick Look
    Note: This is a placeholder. Real conversion requires USD tools.
    """
    usdz_path = glb_path.replace('.glb', '.usdz')
    
    # For now, create a valid empty USDZ file
    # In production, use: usd_from_gltf or Reality Converter
    print(f"⚠ USDZ conversion requires USD tools (not available in sandbox)")
    print(f"  Placeholder created: {usdz_path}")
    print(f"  Use Reality Converter (macOS) or online tool to convert {glb_path}")
    
    # Create placeholder
    with open(usdz_path, 'wb') as f:
        f.write(b'')  # Empty file
    
    return usdz_path

def main():
    """
    Generate all 3D models with premium pipeline
    """
    print("=" * 60)
    print("PALCO ZERO PREMIUM - 3D MODEL GENERATOR")
    print("=" * 60)
    
    # Create models directory if not exists
    os.makedirs('models', exist_ok=True)
    
    # Generate can model
    can_glb = create_can_model()
    can_usdz = convert_glb_to_usdz(can_glb)
    
    print()
    
    # Generate pouch model
    pouch_glb = create_pouch_model()
    pouch_usdz = convert_glb_to_usdz(pouch_glb)
    
    print()
    print("=" * 60)
    print("✓ ALL MODELS GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Can GLB: {can_glb}")
    print(f"Can USDZ: {can_usdz} (placeholder)")
    print(f"Pouch GLB: {pouch_glb}")
    print(f"Pouch USDZ: {pouch_usdz} (placeholder)")
    print()
    print("Next steps:")
    print("1. Use Reality Converter (macOS) to convert GLB → USDZ")
    print("2. Or use online tool: https://www.vectary.com/3d-modeling-news/how-to-convert-gltf-glb-to-usdz/")
    print("3. Replace placeholder USDZ files with real ones")

if __name__ == "__main__":
    main()
