# GUIA RÁPIDO: CONVERSÃO GLB → USDZ

**Tempo estimado:** 5 minutos  
**Requisito:** macOS com Reality Converter OU acesso à internet

---

## 🍎 OPÇÃO A: REALITY CONVERTER (RECOMENDADO)

### 1. Instalar Reality Converter
- Abrir App Store no Mac
- Buscar "Reality Converter"
- Clicar "Obter" (app gratuito da Apple)
- Aguardar instalação

### 2. Baixar Modelos GLB do GitHub
- Ir para: https://github.com/sal-cmyk/Palco-Zero-Premium---AR-demo-ready
- Navegar para pasta `models/`
- Baixar arquivos:
  - `can.glb`
  - `cookie-pack.glb`

### 3. Converter Lata (can.glb)
- Abrir Reality Converter
- Arrastar `can.glb` para a janela do app
- Aguardar preview carregar
- Clicar "Export" (canto inferior direito)
- Salvar como `can.usdz`

### 4. Converter Cookie-Pack (cookie-pack.glb)
- Repetir processo anterior
- Arrastar `cookie-pack.glb`
- Export → Salvar como `cookie-pack.usdz`

### 5. Substituir Arquivos no Repositório
```bash
# Clonar repo (se ainda não tiver)
git clone https://github.com/sal-cmyk/Palco-Zero-Premium---AR-demo-ready.git
cd Palco-Zero-Premium---AR-demo-ready

# Substituir arquivos USDZ
cp ~/Downloads/can.usdz models/can.usdz
cp ~/Downloads/cookie-pack.usdz models/cookie-pack.usdz

# Commit e push
git add models/*.usdz
git commit -m "✨ Add valid USDZ files for iOS Quick Look"
git push origin main
```

### 6. Aguardar Deploy
- Vercel detecta push automaticamente
- Deploy leva ~30-60 segundos
- Site atualizado: https://palco-0-hackthepack.vercel.app/

---

## 🌐 OPÇÃO B: FERRAMENTA ONLINE

### 1. Acessar Conversor Online
- Ir para: https://products.aspose.app/3d/conversion/glb-to-usdz
- OU: https://www.vectary.com/ (criar conta gratuita)

### 2. Upload GLB
- Clicar "Upload" ou arrastar arquivo
- Selecionar `can.glb` primeiro
- Aguardar upload completar

### 3. Converter
- Selecionar formato de saída: USDZ
- Clicar "Convert"
- Aguardar processamento (10-30s)

### 4. Download USDZ
- Clicar "Download"
- Salvar como `can.usdz`
- Repetir para `cookie-pack.glb` → `cookie-pack.usdz`

### 5. Substituir Arquivos
- Seguir passo 5 da Opção A (comandos Git)

---

## 📱 TESTAR NO IPHONE

### 1. Abrir Safari
- Ir para: https://palco-0-hackthepack.vercel.app/?sku=can
- Aguardar modelo 3D carregar

### 2. Verificar Botão AR
- Botão "Ver em AR" deve aparecer (canto inferior direito)
- Se não aparecer: USDZ inválido ou não carregou

### 3. Clicar "Ver em AR"
- Quick Look deve abrir
- Produto aparece em AR no ambiente real
- Testar movimentação (arrastar, pinça para zoom)

### 4. Testar Cookie-Pack
- Repetir para: https://palco-0-hackthepack.vercel.app/?sku=cookie-pack

---

## 🚨 TROUBLESHOOTING

### Botão AR não aparece
**Causa:** USDZ inválido ou não carregado  
**Solução:**
1. Abrir DevTools no Safari (Cmd+Opt+I)
2. Ir para Console
3. Procurar erros relacionados a USDZ
4. Verificar se arquivo existe: https://palco-0-hackthepack.vercel.app/models/can.usdz
5. Se 404: arquivo não foi commitado corretamente
6. Se 200 mas não funciona: USDZ inválido, reconverter

### Reality Converter não abre GLB
**Causa:** GLB pode ter formato não suportado  
**Solução:**
1. Usar Opção B (online tool)
2. OU: Abrir GLB no Blender → Export USDZ
3. OU: Usar comando `usdz_converter` (se tiver Xcode instalado)

### Quick Look abre mas modelo não aparece
**Causa:** USDZ sem materiais ou geometria corrompida  
**Solução:**
1. Verificar tamanho do arquivo USDZ (deve ser > 1KB)
2. Se muito pequeno: conversão falhou
3. Reconverter usando Reality Converter (mais confiável)

### Deploy não atualiza
**Causa:** Vercel não detectou push  
**Solução:**
1. Ir para: https://vercel.com/sal-cmyk/palco-0-hackthepack
2. Verificar último deploy
3. Se não apareceu: fazer push manual
4. OU: Trigger redeploy no dashboard Vercel

---

## ✅ CHECKLIST FINAL

- [ ] Reality Converter instalado (ou acesso a online tool)
- [ ] `can.glb` baixado do GitHub
- [ ] `cookie-pack.glb` baixado do GitHub
- [ ] `can.usdz` convertido
- [ ] `cookie-pack.usdz` convertido
- [ ] Arquivos USDZ substituídos no repo local
- [ ] Commit + push realizado
- [ ] Deploy Vercel concluído (~60s)
- [ ] Testado no iPhone: `?sku=can`
- [ ] Testado no iPhone: `?sku=cookie-pack`
- [ ] Botão "Ver em AR" aparece
- [ ] Quick Look funciona
- [ ] Produto aparece em AR no ambiente real

---

## 📞 SUPORTE

**GitHub Issues:** https://github.com/sal-cmyk/Palco-Zero-Premium---AR-demo-ready/issues  
**Reality Converter Docs:** https://developer.apple.com/augmented-reality/tools/  
**USDZ Spec:** https://graphics.pixar.com/usd/release/spec_usdz.html

---

**Última atualização:** 10 de fevereiro de 2026  
**Autor:** HACKTHEPACK Operational Executor
