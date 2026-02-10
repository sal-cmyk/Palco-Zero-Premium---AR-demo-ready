# PALCO ZERO - TESTING CHECKLIST
## Checklist de Testes iOS + Android (Web)

---

## PRÉ-REQUISITOS

### Ambiente de Teste
- [ ] Servidor HTTPS configurado (AR requer HTTPS)
- [ ] Certificado SSL válido
- [ ] Arquivos GLB e USDZ no mesmo domínio (CORS)
- [ ] model-viewer CDN carregando corretamente

### Dispositivos Necessários
- [ ] iPhone (iOS 12+ recomendado)
- [ ] iPad (para testes em telas maiores)
- [ ] Android com ARCore (Android 7.0+)
- [ ] Diferentes resoluções testadas

---

## TESTES iOS (Safari)

### 1. Carregamento Inicial
- [ ] Página carrega sem erros no console
- [ ] Estado "idle" → "loading" acontece imediatamente
- [ ] Loading skeleton aparece com animação suave
- [ ] Texto "Preparando experiência..." está visível

### 2. Modelo 3D
- [ ] Arquivo GLB carrega corretamente
- [ ] Progress bar avança de 0% → 100%
- [ ] Modelo renderiza sem artefatos visuais
- [ ] Rotação automática funciona após 3 segundos
- [ ] Gestos touch funcionam:
  - [ ] Pinch para zoom
  - [ ] Swipe para rotacionar
  - [ ] Dois dedos para pan
- [ ] Sombra do modelo está presente
- [ ] Iluminação está adequada

### 3. Validação USDZ
- [ ] Console mostra "✓ USDZ file validated"
- [ ] Request HEAD retorna status 200
- [ ] Path do USDZ está correto
- [ ] Arquivo USDZ não está corrompido

### 4. Botão AR (Quick Look)
- [ ] Botão AR aparece APENAS após modelo carregar
- [ ] Botão aparece APENAS se USDZ for válido
- [ ] Ícone de cubo 3D está visível
- [ ] Texto "Ver em AR" está legível
- [ ] Efeito glassmorphism está aplicado
- [ ] Animação de slide-up acontece suavemente
- [ ] Botão responde ao toque (não está hidden)

### 5. Sessão AR (Quick Look)
- [ ] Toque no botão abre Quick Look
- [ ] USDZ carrega no Quick Look
- [ ] Nome do produto aparece no Quick Look
- [ ] Modelo pode ser posicionado no ambiente
- [ ] Escala do modelo é apropriada
- [ ] Lighting Estimation funciona
- [ ] Oclusão de pessoas funciona (iOS 13+)
- [ ] Compartilhamento funciona (botão de share)

### 6. Tracking de Eventos AR
- [ ] Console mostra "AR Status: session-started"
- [ ] Estado muda para "ar"
- [ ] Indicador de status AR aparece (canto superior direito)
- [ ] Bolinha verde pisca
- [ ] Texto "Sessão AR ativa" está visível
- [ ] Ao sair do AR:
  - [ ] Status muda para "not-presenting"
  - [ ] Estado volta para "ready"
  - [ ] Indicador de status desaparece

### 7. UI Premium
- [ ] Glassmorphism tem blur de 40px
- [ ] Cards têm opacidade correta (~0.06)
- [ ] Tipografia está limpa (SF Pro Display)
- [ ] Hierarquia visual está clara
- [ ] Espaçamento é generoso
- [ ] Micro-animações são suaves (120-180ms)
- [ ] Fade-in dos cards tem delay escalonado

### 8. Responsividade iOS
- [ ] iPhone SE (small screen) funciona
- [ ] iPhone 14/15 (standard) funciona
- [ ] iPhone 14/15 Pro Max (large) funciona
- [ ] iPad Mini (tablet) funciona
- [ ] iPad Pro (large tablet) funciona
- [ ] Landscape mode funciona
- [ ] Safe area insets respeitados (notch)

### 9. Performance iOS
- [ ] Loading completo em < 5 segundos (Wi-Fi)
- [ ] Frame rate estável (60fps) na rotação
- [ ] Sem lag ao pinch zoom
- [ ] Transições state são instantâneas
- [ ] AR abre em < 2 segundos

---

## TESTES ANDROID (Chrome)

### 1. Carregamento Inicial
- [ ] Página carrega sem erros no console
- [ ] Estado "idle" → "loading" acontece
- [ ] Loading skeleton aparece
- [ ] Texto "Preparando experiência..." está visível

### 2. Modelo 3D
- [ ] Arquivo GLB carrega corretamente
- [ ] Progress bar funciona
- [ ] Modelo renderiza sem problemas
- [ ] Rotação automática funciona
- [ ] Gestos touch funcionam:
  - [ ] Pinch para zoom
  - [ ] Swipe para rotacionar
  - [ ] Dois dedos para pan
- [ ] Sombra do modelo está presente

### 3. Validação USDZ (Android usa GLB para AR)
- [ ] Console mostra validação
- [ ] Mesmo GLB será usado para AR
- [ ] Path está correto

### 4. Botão AR (Scene Viewer)
- [ ] Botão AR aparece após modelo carregar
- [ ] Botão aparece se device suporta ARCore
- [ ] Ícone está visível
- [ ] Texto "Ver em AR" está legível
- [ ] Glassmorphism aplicado
- [ ] Animação slide-up funciona

### 5. Sessão AR (Scene Viewer)
- [ ] Toque no botão abre Scene Viewer
- [ ] Modelo GLB carrega no Scene Viewer
- [ ] Scanning de superfície funciona
- [ ] Modelo pode ser posicionado
- [ ] Escala é apropriada
- [ ] Iluminação ambiente detectada
- [ ] Sombra projetada no chão
- [ ] Rotate, scale, move funcionam

### 6. Tracking de Eventos AR
- [ ] Console mostra "AR Status: session-started"
- [ ] Estado muda para "ar"
- [ ] Indicador de status aparece
- [ ] Ao sair (botão voltar):
  - [ ] Status "not-presenting"
  - [ ] Estado volta "ready"
  - [ ] Indicador desaparece

### 7. UI Premium
- [ ] Glassmorphism renderiza corretamente
- [ ] Blur funciona no Chrome
- [ ] Cards têm opacidade correta
- [ ] Tipografia Roboto está carregada
- [ ] Hierarquia visual clara
- [ ] Espaçamento adequado
- [ ] Micro-animações suaves

### 8. Responsividade Android
- [ ] Pixel 5/6/7 (standard) funciona
- [ ] Galaxy S20/S21/S22 funciona
- [ ] Tablets Android funcionam
- [ ] Landscape mode funciona
- [ ] Different screen densities OK

### 9. Performance Android
- [ ] Loading < 5 segundos (Wi-Fi)
- [ ] Frame rate OK na rotação
- [ ] Sem lag ao interagir
- [ ] Transições rápidas
- [ ] AR abre em < 3 segundos

---

## TESTES CROSS-PLATFORM

### 1. Fallback para Desktop
- [ ] Desktop sem AR não mostra botão AR
- [ ] Desktop ainda carrega modelo 3D
- [ ] Controles de mouse funcionam
- [ ] Experience degrada graciosamente

### 2. Modo Photo (Opcional)
Se implementado:
- [ ] Card "Modo Foto" aparece se suportado
- [ ] Botão "Ativar Modo Foto" funciona
- [ ] Permissão de câmera é solicitada
- [ ] Stream de vídeo aparece
- [ ] Botão "Capturar" funciona
- [ ] Foto é usada como background
- [ ] Glass UI fica sobre foto
- [ ] Botão "Cancelar" limpa tudo
- [ ] Estado "photo" é gerenciado corretamente

### 3. Edge Cases
- [ ] Conexão lenta: loading não trava
- [ ] Arquivo GLB inválido: erro tratado
- [ ] Arquivo USDZ inválido: botão AR não aparece
- [ ] CORS error: mensagem clara
- [ ] Offline: mensagem de conexão
- [ ] Tab background: modelo pausa
- [ ] Tab foreground: modelo resume
- [ ] Orientation change: layout se adapta

### 4. Acessibilidade
- [ ] alt text no model-viewer
- [ ] Labels em botões
- [ ] Contraste adequado
- [ ] Touch targets > 44px
- [ ] VoiceOver/TalkBack funcionam (básico)

### 5. Analytics (se implementado)
- [ ] Event "ar_click" dispara
- [ ] Event "ar_status" trackeado
- [ ] State changes logadas
- [ ] Device type identificado
- [ ] Timestamps corretos

---

## CHECKLIST DE DEPLOY

### Antes de Demo (3 de Março)
- [ ] Certificado SSL renovado
- [ ] DNS configurado
- [ ] CDN configurado (se aplicável)
- [ ] Arquivos GLB/USDZ otimizados
- [ ] Compressão gzip/brotli ativada
- [ ] Cache headers configurados
- [ ] Error tracking ativo (Sentry, etc)
- [ ] Analytics configurado
- [ ] Backup de arquivos feito
- [ ] Domínio custom (se aplicável)

### Otimizações Finais
- [ ] GLB < 5MB (ideal < 2MB)
- [ ] USDZ < 10MB
- [ ] Texturas otimizadas
- [ ] Geometria simplificada
- [ ] CSS minificado
- [ ] JS minificado
- [ ] Images webp (se houver)
- [ ] Fonts otimizadas

### Teste Final Pré-Demo
- [ ] Teste completo iOS em 3 devices
- [ ] Teste completo Android em 3 devices
- [ ] Teste em rede 3G/4G (não só Wi-Fi)
- [ ] Teste com pessoas reais (não só devs)
- [ ] Tempo de loading aceitável
- [ ] AR funciona first try
- [ ] Sem bugs visuais
- [ ] Performance fluida

---

## TROUBLESHOOTING COMUM

### "Botão AR não aparece"
- [ ] Verificar console: USDZ validou?
- [ ] Verificar device tem ARCore/ARKit
- [ ] Verificar HTTPS está ativo
- [ ] Verificar path do arquivo USDZ
- [ ] Verificar CORS headers

### "AR abre mas modelo não carrega"
- [ ] Verificar tamanho do arquivo
- [ ] Verificar formato (GLB para Android)
- [ ] Verificar USDZ válido (iOS)
- [ ] Verificar conexão Internet
- [ ] Verificar console errors

### "Performance ruim"
- [ ] Reduzir poly count do modelo
- [ ] Otimizar texturas
- [ ] Desabilitar features desnecessárias
- [ ] Testar em device mais potente

### "Glassmorphism não funciona"
- [ ] Verificar backdrop-filter support
- [ ] Verificar prefixos -webkit-
- [ ] Fallback para solid background

---

## NOTAS IMPORTANTES

1. **Sempre testar em HTTPS** - AR não funciona em HTTP
2. **Validar USDZ antes do botão** - Evita frustração do usuário
3. **Tracking é essencial** - Dados para melhorar experiência
4. **Performance matters** - Modelo deve ser otimizado
5. **Graceful degradation** - Funcionar sem AR também

---

**Data da última atualização:** Preparado para demo 3 de Março 2026
**Versão:** 1.0
**Responsável:** Sal Zammataro / hackthepack team
