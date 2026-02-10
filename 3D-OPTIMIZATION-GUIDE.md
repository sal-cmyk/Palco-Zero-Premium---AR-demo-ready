# GUIA DE OTIMIZAÇÃO DE MODELOS 3D
## GLB + USDZ para AR Cross-Platform

---

## 📦 REQUISITOS DE ARQUIVO

### GLB (Android + Web)
- **Tamanho máximo:** 5MB (ideal < 2MB)
- **Formato:** GLB (não GLTF separado)
- **Compressão:** Draco recomendado
- **Poly count:** < 100,000 faces
- **Texturas:** Power-of-two, < 2048px

### USDZ (iOS Quick Look)
- **Tamanho máximo:** 10MB (Quick Look limit)
- **Formato:** USDZ (não USD separado)
- **Compressão:** Automática no Reality Converter
- **Poly count:** < 100,000 faces
- **Texturas:** < 2048px, embedded

---

## 🛠 WORKFLOW DE OTIMIZAÇÃO

### 1. Preparação no Blender

```
1. Abrir modelo 3D no Blender
2. Aplicar modificadores (se houver)
3. Triangular geometria (Mesh → Faces → Triangulate)
4. Remover duplicatas (Mesh → Clean Up → Merge by Distance)
5. Remover faces internas não visíveis
6. Aplicar escala/rotação (Ctrl+A → All Transforms)
```

**Reduzir Poly Count:**
```
1. Selecionar objeto
2. Adicionar Modifier: Decimate
3. Ratio: 0.5 (reduz 50%)
4. Testar visualmente
5. Aplicar modifier
```

**Otimizar Texturas:**
```
1. UV Unwrap apropriado
2. Bake texturas se necessário
3. Redimensionar para power-of-two:
   - 2048x2048 (alta qualidade)
   - 1024x1024 (padrão)
   - 512x512 (low-poly)
4. Exportar como PNG ou JPG (JPG menor)
```

### 2. Exportar GLB

**Configurações Blender Export:**
```
File → Export → glTF 2.0 (.glb/.gltf)

Format: glTF Binary (.glb)  ✓
Include:
  - Selected Objects (ou visíveis)
  - Cameras ✗
  - Punctual Lights ✗
Transform:
  - +Y Up ✓
Geometry:
  - Apply Modifiers ✓
  - UVs ✓
  - Normals ✓
  - Tangents ✓
  - Vertex Colors ✗ (se não usar)
Compression:
  - Draco Mesh Compression ✓ (importante!)
Materials:
  - Materials ✓
  - Export ✓
Animation:
  - Use Current Frame ✓
  - Animations ✗ (AR não precisa)
```

**Resultado esperado:**
- Arquivo `.glb` único
- Texturas embedded
- < 5MB (ideal < 2MB)

### 3. Converter para USDZ (iOS)

**Opção A: Reality Converter (Mac)**
```
1. Baixar Reality Converter (grátis)
   https://developer.apple.com/augmented-reality/tools/

2. Arrastar GLB para Reality Converter

3. Ajustar settings:
   - Name: product
   - Scale: Auto (ou ajustar)
   - Placement: Horizontal (piso)
   
4. Export USDZ

5. Testar no Quick Look Preview
```

**Opção B: usdz_converter.py (Command Line)**
```bash
# Download da Apple Developer
curl -O https://docs-assets.developer.apple.com/ml-research/datasets/usdz/usdz_converter.py

# Converter
python usdz_converter.py input.glb output.usdz

# Com opções
python usdz_converter.py \
  input.glb \
  output.usdz \
  -v  # verbose
```

**Opção C: Blender USD Export (Experimental)**
```
File → Export → Universal Scene Description (.usd/.usdc/.usda)

Format: USDC (Binary)
Selected Objects Only: ✓
Visible Objects Only: ✓
```
Depois comprimir para USDZ no Reality Converter.

### 4. Validar Arquivos

**Testar GLB:**
```
1. Abrir em https://gltf-viewer.donmccurdy.com/
2. Verificar:
   - Modelo carrega sem erros
   - Texturas aparecem
   - Escala está correta
   - File size aceitável
```

**Testar USDZ:**
```
1. Enviar arquivo para iPhone via AirDrop
2. Tap para abrir no Quick Look
3. Verificar:
   - Modelo carrega
   - Escala apropriada
   - Iluminação OK
   - Posicionamento funciona
```

**Validar Tecnicamente:**
```bash
# GLB info
npm install -g gltf-pipeline
gltf-pipeline -i model.glb --stats

# USDZ info (Mac)
usdchecker model.usdz
```

---

## ⚡ OTIMIZAÇÕES AVANÇADAS

### Draco Compression

**Instalar ferramentas:**
```bash
npm install -g gltf-pipeline
```

**Comprimir GLB:**
```bash
gltf-pipeline -i input.glb -o output.glb -d
# -d = Draco compression
# Reduz ~80% do tamanho
```

**Resultado:**
- 5MB → 1MB typical
- Mantém qualidade visual
- Requer decoder (model-viewer já tem)

### Texture Optimization

**Ferramentas recomendadas:**
```bash
# Squoosh (web)
https://squoosh.app/

# ImageMagick (CLI)
convert input.png -resize 1024x1024 -quality 85 output.jpg

# WebP (ainda não suportado em USDZ)
cwebp input.png -q 80 -o output.webp
```

**Configurações:**
- Redimensionar para power-of-two
- JPG quality 80-90% (bom balance)
- PNG só se necessário transparência

### Level of Detail (LOD)

Para modelos complexos:
```
1. Criar 3 versões:
   - LOD0: Alta qualidade (close-up)
   - LOD1: Média qualidade (normal)
   - LOD2: Baixa qualidade (distante)

2. Exportar como GLB separados

3. Usar LOD0 para web/AR close
4. Usar LOD2 para thumbnails
```

---

## 🎨 BOAS PRÁTICAS DE MODELAGEM

### Geometria

```
✅ DO:
- Usar quads no workflow
- Triangular antes de export
- Edge loops limpos
- Topology regular
- Faces convexas

❌ DON'T:
- N-gons (5+ lados)
- Faces concavos
- Faces duplicadas
- Vértices soltos
- Geometria interna
```

### Materiais

```
✅ DO:
- PBR materials (Principled BSDF)
- Texturas power-of-two
- Base Color + Normal + Roughness
- Metallic onde apropriado

❌ DON'T:
- Múltiplos materiais desnecessários
- Texturas gigantes (> 2048px)
- Transparência complexa
- Emission (não funciona bem em AR)
```

### UV Mapping

```
✅ DO:
- UV unwrap limpo
- Minimizar seams
- Utilizar espaço 0-1 eficientemente
- Testar no UV Editor

❌ DON'T:
- UV overlapping
- Stretching excessivo
- Seams em áreas visíveis
- Múltiplos UV maps
```

---

## 📏 ESCALA E POSICIONAMENTO

### Escala Correta

```
Blender Units = Metros

Exemplos de escala real:
- Lata de refrigerante: 0.12m altura
- Garrafa PET 2L: 0.30m altura
- Caixa de sapato: 0.30 x 0.20 x 0.10m
- Smartphone: 0.15m altura

Aplicar escala:
1. Selecionar objeto
2. S (scale) → Digite valor → Enter
3. Ctrl+A → Apply → Scale
```

### Pivot Point

```
Definir pivot na base do objeto:
1. Tab (edit mode)
2. Selecionar vértices da base
3. Shift+S → Cursor to Selected
4. Tab (object mode)
5. Object → Set Origin → Origin to 3D Cursor
```

### Orientação

```
Padrão para AR:
- +Y = Up (vertical)
- +X = Right
- +Z = Forward (frente do objeto)

Rotacionar se necessário:
R X 90 (rodar 90° em X)
Ctrl+A → Apply → Rotation
```

---

## 🧪 TESTING WORKFLOW

### 1. Test Localmente

```bash
# Servir arquivos HTTPS local
# Opção 1: Python
python3 -m http.server 8000

# Opção 2: Node.js
npx http-server -p 8000

# Opção 3: Vercel Dev
vercel dev
```

**Testar em:**
- Chrome desktop (model-viewer)
- Safari desktop (preview)
- iPhone Safari (AR)
- Android Chrome (AR)

### 2. Checklist Visual

```
✅ Modelo carrega < 5s
✅ Textures corretas
✅ Escala apropriada
✅ Sombra projetada
✅ Iluminação OK
✅ Sem artefatos
✅ Rotação suave
✅ AR posicionamento fácil
```

### 3. Performance Metrics

```
Target metrics:
- File size: < 2MB GLB, < 10MB USDZ
- Poly count: < 100k faces
- Texture size: < 2048px
- Load time: < 3s (Wi-Fi)
- Frame rate: 60fps web, 30fps AR
```

---

## 🔧 FERRAMENTAS ÚTEIS

### Online
- [glTF Viewer](https://gltf-viewer.donmccurdy.com/) - Preview GLB
- [Squoosh](https://squoosh.app/) - Otimizar texturas
- [Reality Composer](https://developer.apple.com/augmented-reality/tools/) - USDZ editor

### Desktop
- [Blender](https://www.blender.org/) - Modelagem + export
- [Reality Converter](https://developer.apple.com/augmented-reality/tools/) - GLB → USDZ (Mac)
- [Meshlab](https://www.meshlab.net/) - Mesh processing

### Command Line
```bash
# glTF pipeline
npm install -g gltf-pipeline

# USD tools (Mac)
brew install usd

# ImageMagick
brew install imagemagick
```

---

## 📚 RECURSOS

### Documentação
- [glTF 2.0 Spec](https://www.khronos.org/gltf/)
- [USDZ File Format](https://graphics.pixar.com/usd/docs/Usdz-File-Format-Specification.html)
- [model-viewer Docs](https://modelviewer.dev/)
- [ARKit Guidelines](https://developer.apple.com/augmented-reality/)

### Tutoriais
- [Blender to AR](https://www.youtube.com/results?search_query=blender+to+ar)
- [GLB Optimization](https://www.donmccurdy.com/2021/08/02/dont-trust-default-gltf-export-options/)
- [USDZ Best Practices](https://developer.apple.com/documentation/arkit/arkit_in_ios/content_anchors/creating_3d_content_with_reality_composer)

---

## 🎯 CHECKLIST FINAL

Antes de deploy:

### GLB
- [ ] Tamanho < 5MB (ideal < 2MB)
- [ ] Draco compressed
- [ ] Texturas power-of-two
- [ ] Poly count < 100k
- [ ] Testa em gltf-viewer
- [ ] Escala correta
- [ ] Pivot na base
- [ ] Orientação +Y up

### USDZ
- [ ] Tamanho < 10MB
- [ ] Converte de GLB otimizado
- [ ] Testa no Quick Look (iPhone)
- [ ] Escala apropriada
- [ ] Placement horizontal funciona
- [ ] Lighting estimation OK

### Validação
- [ ] HEAD request retorna 200
- [ ] CORS configurado
- [ ] HTTPS ativo
- [ ] Paths corretos em app.js
- [ ] Botão AR aparece em devices suportados

---

**Última atualização:** 10 Fevereiro 2026
**Para:** hackthepack - Palco Zero
