#!/usr/bin/env python3
"""
Gera modelos 3D simples (lata e cookie-pack) com textura realista
GLB otimizado < 2MB para web AR
"""

import trimesh
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_can_model(output_path):
    """Cria modelo 3D de lata (cilindro metálico)"""
    print(f"[CAN] Criando modelo 3D de lata...")
    
    # Criar cilindro (lata)
    cylinder = trimesh.creation.cylinder(
        radius=0.03,  # 3cm raio
        height=0.12,  # 12cm altura (lata padrão)
        sections=32   # Resolução circular
    )
    
    # Criar tampa superior
    top_cap = trimesh.creation.cylinder(
        radius=0.031,
        height=0.002,
        sections=32
    )
    top_cap.apply_translation([0, 0, 0.061])
    
    # Criar tampa inferior
    bottom_cap = trimesh.creation.cylinder(
        radius=0.031,
        height=0.002,
        sections=32
    )
    bottom_cap.apply_translation([0, 0, -0.061])
    
    # Combinar geometrias
    can = trimesh.util.concatenate([cylinder, top_cap, bottom_cap])
    
    # Criar textura simples (label wrap)
    texture = Image.new('RGB', (512, 512), color=(220, 220, 220))  # Cinza metálico
    draw = ImageDraw.Draw(texture)
    
    # Adicionar gradiente metálico
    for y in range(512):
        brightness = int(200 + 55 * np.sin(y / 512 * np.pi))
        draw.line([(0, y), (512, y)], fill=(brightness, brightness, brightness))
    
    # Adicionar texto "NEON FLOW" (placeholder)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    draw.text((256, 200), "NEON", fill=(255, 45, 122), anchor="mm", font=font)
    draw.text((256, 260), "FLOW", fill=(255, 90, 42), anchor="mm", font=font)
    
    # Salvar textura
    texture_path = output_path.replace('.glb', '_texture.png')
    texture.save(texture_path)
    print(f"[CAN] Textura salva: {texture_path}")
    
    # Aplicar material PBR (metallic)
    material = trimesh.visual.material.PBRMaterial(
        baseColorFactor=[0.9, 0.9, 0.9, 1.0],
        metallicFactor=0.8,
        roughnessFactor=0.3
    )
    
    can.visual = trimesh.visual.TextureVisuals(
        material=material
    )
    
    # Exportar GLB
    can.export(output_path)
    file_size = os.path.getsize(output_path) / 1024 / 1024
    print(f"[CAN] Modelo GLB salvo: {output_path} ({file_size:.2f} MB)")
    
    return output_path

def create_cookie_pack_model(output_path):
    """Cria modelo 3D de cookie-pack (caixa plástica)"""
    print(f"[COOKIE] Criando modelo 3D de cookie-pack...")
    
    # Criar caixa retangular
    box = trimesh.creation.box(
        extents=[0.08, 0.12, 0.04]  # 8cm x 12cm x 4cm
    )
    
    # Arredondar cantos
    box = box.subdivide()
    
    # Criar textura simples (plástico transparente com label)
    texture = Image.new('RGB', (512, 512), color=(245, 245, 250))  # Branco levemente azulado
    draw = ImageDraw.Draw(texture)
    
    # Adicionar borda
    draw.rectangle([(20, 20), (492, 492)], outline=(200, 200, 200), width=3)
    
    # Adicionar texto "BISCOITO PREMIUM"
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    draw.text((256, 200), "BISCOITO", fill=(255, 90, 42), anchor="mm", font=font)
    draw.text((256, 260), "PREMIUM", fill=(255, 45, 122), anchor="mm", font=font)
    
    # Salvar textura
    texture_path = output_path.replace('.glb', '_texture.png')
    texture.save(texture_path)
    print(f"[COOKIE] Textura salva: {texture_path}")
    
    # Aplicar material PBR (plástico)
    material = trimesh.visual.material.PBRMaterial(
        baseColorFactor=[0.96, 0.96, 0.98, 1.0],
        metallicFactor=0.1,
        roughnessFactor=0.5
    )
    
    box.visual = trimesh.visual.TextureVisuals(
        material=material
    )
    
    # Exportar GLB
    box.export(output_path)
    file_size = os.path.getsize(output_path) / 1024 / 1024
    print(f"[COOKIE] Modelo GLB salvo: {output_path} ({file_size:.2f} MB)")
    
    return output_path

if __name__ == "__main__":
    # Criar pasta models se não existir
    os.makedirs("models", exist_ok=True)
    
    # Gerar modelos
    print("\n=== Gerando Modelos 3D ===\n")
    
    can_path = "models/can.glb"
    cookie_path = "models/cookie-pack.glb"
    
    create_can_model(can_path)
    print()
    create_cookie_pack_model(cookie_path)
    
    print("\n=== Modelos 3D Criados com Sucesso ===\n")
    print(f"✅ Lata: {can_path}")
    print(f"✅ Cookie-pack: {cookie_path}")
    print("\nPróximo passo: Gerar posters.webp realistas")
