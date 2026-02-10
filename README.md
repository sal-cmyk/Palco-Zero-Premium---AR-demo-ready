# 🎭 PALCO ZERO - Premium AR Experience

> Transforme embalagens físicas em experiências digitais premium com AR cross-platform

![Version](https://img.shields.io/badge/version-1.0-blue)
![iOS](https://img.shields.io/badge/iOS-12%2B-black)
![Android](https://img.shields.io/badge/Android-7.0%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 Objetivo

Criar uma experiência web premium de AR que funciona perfeitamente em iOS (Quick Look) e Android (Scene Viewer) sem apps nativos. Design Apple-level com glassmorphism real e micro-animações suaves.

**Demo alvo:** 3 de Março 2026

---

## ✨ Features

### Core
- ✅ **AR Cross-Platform** - iOS Quick Look + Android Scene Viewer
- ✅ **USDZ Validation** - Botão AR só aparece se arquivo válido
- ✅ **AR Tracking** - Eventos rastreados (session-started, object-placed, etc)
- ✅ **State Machine** - Gerenciamento limpo de estados (idle → loading → ready → ar)
- ✅ **Premium UI** - Glassmorphism real, tipografia Apple, micro-animações 120-180ms

### Optional
- 🎨 **Photo Mode** - Capture ambiente e visualize produto em contexto real
- 📊 **Analytics Ready** - Sistema preparado para tracking
- 🌙 **Dark Mode** - Suporte automático baseado em preferência do sistema

---

## 🚀 Quick Start

### Pré-requisitos

1. **Servidor HTTPS** (AR requer HTTPS)
2. **Modelos 3D:**
   - `product.glb` - Para web + Android (< 5MB)
   - `product.usdz` - Para iOS AR (< 10MB)

### Setup Básico

```bash
# 1. Clone ou baixe os arquivos
palco-zero/
├── palco-zero-premium.html
├── styles-premium.css
├── state-machine.js
├── ar-manager.js
├── photo-mode.js
├── app.js
└── models/
    ├── product.glb
    └── product.usdz

# 2. Configure seu produto em app.js
const APP_CONFIG = {
    product: {
        name: 'Seu Produto',
        subtitle: 'Tagline premium',
        description: 'Descrição detalhada...',
        glbPath: './models/product.glb',
        usdzPath: './models/product.usdz'
    }
};

# 3. Deploy em servidor HTTPS
# Ex: Vercel, Netlify, GitHub Pages

# 4. Teste em iOS e Android
# Use checklist em TESTING-CHECKLIST.md
```

### Deploy Rápido (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Pronto! URL HTTPS gerado automaticamente
```

---

## 📁 Estrutura de Arquivos

```
palco-zero/
├── palco-zero-premium.html    # HTML principal com model-viewer
├── styles-premium.css         # Estilos Apple-level + glassmorphism
├── state-machine.js           # State management (idle/loading/ready/ar/photo)
├── ar-manager.js              # AR logic + USDZ validation + tracking
├── photo-mode.js              # Optional: Camera capture feature
├── app.js                     # Main orchestrator
├── ARCHITECTURE.md            # Documentação técnica detalhada
├── TESTING-CHECKLIST.md       # Checklist completo iOS + Android
└── models/
    ├── product.glb            # Modelo 3D otimizado
    └── product.usdz           # Modelo AR para iOS
```

---

## 🎨 Design System

### Cores
```css
--color-primary: #000000      /* Text primário */
--color-secondary: #1d1d1f    /* Text secundário */
--color-tertiary: #86868b     /* Text terciário */
--color-accent: #0071e3       /* Accent (botões, links) */
--color-background: #f5f5f7   /* Background */
```

### Glassmorphism
```css
--glass-blur: 40px            /* Blur real, não excessivo */
--glass-opacity: 0.06         /* Muito sutil */
--glass-border: rgba(255,255,255,0.18)
--glass-shadow: rgba(0,0,0,0.1)
```

### Tipografia
```css
--font-system: -apple-system, BlinkMacSystemFont, "SF Pro Display"
--font-weight-regular: 400
--font-weight-semibold: 600
--font-weight-bold: 700
```

### Timing
```css
--timing-fast: 120ms          /* Micro-interactions */
--timing-base: 180ms          /* Standard */
--timing-slow: 300ms          /* Transitions */
--easing: cubic-bezier(0.4, 0, 0.2, 1)
```

---

## 🔧 Configuração

### Trocar Produto

**Opção 1: Via Config (antes de carregar)**
```javascript
// Em app.js, edite APP_CONFIG
const APP_CONFIG = {
    product: {
        name: 'Guaraná Antarctica',
        subtitle: 'Sabor do Brasil',
        description: 'Explore em realidade aumentada...',
        glbPath: './models/guarana.glb',
        usdzPath: './models/guarana.usdz'
    }
};
```

**Opção 2: Via API (dinâmico)**
```javascript
// Após página carregar
window.PalcoZero.updateProduct({
    name: 'Novo Produto',
    subtitle: 'Nova experiência',
    description: '...',
    glbPath: './models/new.glb',
    usdzPath: './models/new.usdz'
});
```

### Habilitar Analytics

```javascript
const APP_CONFIG = {
    // ... product config
    analytics: {
        enabled: true,
        debugMode: false  // true = console logs
    }
};

// Implementar provider em app.js
window.analytics = {
    track: (event, props) => {
        // Ex: Google Analytics
        gtag('event', event, props);
    }
};
```

### Desabilitar Photo Mode

```javascript
// Em photo-mode.js, na linha 11:
this.isSupported = false;  // Força disable
```

Ou simplesmente remova o card do HTML:
```html
<!-- Remover este bloco -->
<div class="card glass fade-in" id="photoModeCard" ...>
    ...
</div>
```

---

## 📱 Suporte de Devices

### iOS (Quick Look)
- **Mínimo:** iOS 12
- **Recomendado:** iOS 13+ (oclusão de pessoas)
- **Browsers:** Safari (WebKit)
- **Formato AR:** USDZ

### Android (Scene Viewer)
- **Mínimo:** Android 7.0 (ARCore support)
- **Recomendado:** Android 9+
- **Browsers:** Chrome
- **Formato AR:** GLB

### Desktop (Fallback)
- Modelo 3D carrega
- Controles de mouse funcionam
- Botão AR não aparece

---

## 🧪 Testing

Use o checklist completo em `TESTING-CHECKLIST.md`

**Quick Test:**
```bash
# iOS
1. Abrir em Safari
2. Modelo deve carregar
3. Botão "Ver em AR" deve aparecer
4. Tap abre Quick Look
5. Objeto pode ser posicionado

# Android
1. Abrir em Chrome
2. Modelo deve carregar
3. Botão "Ver em AR" deve aparecer
4. Tap abre Scene Viewer
5. Scanning + posicionamento funcionam
```

---

## 🎯 State Machine

```
idle ──────► loading ──────► ready ──────► ar
                │                │          │
                │                ▼          │
                └─────────► photo ◄─────────┘
```

### Estados

- **idle** - Inicial, nada carregado
- **loading** - Modelo 3D carregando
- **ready** - Pronto, AR disponível
- **ar** - Sessão AR ativa
- **photo** - Modo foto ativo (opcional)

Ver documentação completa em `ARCHITECTURE.md`

---

## 🛠 API Pública

```javascript
// Acessível via window.PalcoZero

// Trocar produto
PalcoZero.updateProduct({
    name: 'Novo Produto',
    glbPath: './models/new.glb',
    usdzPath: './models/new.usdz'
});

// Estado atual
const state = PalcoZero.getState();  // 'idle', 'loading', 'ready', 'ar', 'photo'

// Reset AR
PalcoZero.resetAR();  // Volta câmera à posição inicial

// Limpar foto
PalcoZero.clearPhoto();  // Remove background de foto

// Config
console.log(PalcoZero.config);
```

---

## 📊 Eventos Rastreados

```javascript
// AR Events (via ar-manager.js)
'ar_click'         // Botão AR clicado
'ar_status'        // Status mudou (session-started, object-placed, etc)

// State Events (via state-machine.js)
'state_change'     // Estado mudou

// Photo Events (via photo-mode.js)
'photo_mode_entered'   // Modo foto ativado
'photo_captured'       // Foto capturada
```

---

## 🚨 Troubleshooting

### Botão AR não aparece

**Checklist:**
1. ✅ HTTPS ativo?
2. ✅ USDZ validou? (ver console)
3. ✅ Device suporta AR? (iOS 12+ ou Android ARCore)
4. ✅ Path do USDZ está correto?
5. ✅ CORS configurado?

**Debug:**
```javascript
// Verificar suporte
console.log(arManager.isARSupported);
console.log(arManager.isUsdzValid);
```

### Performance ruim

**Otimizações:**
1. Reduzir poly count (< 100k faces)
2. Comprimir texturas (power-of-two, < 2048px)
3. Usar Draco compression no GLB
4. Otimizar USDZ no Reality Converter

### Glassmorphism não funciona

**Verificar:**
```css
/* Adicionar fallback */
.glass {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);  /* ← Importante para Safari */
}

/* Se não suportar, fallback sólido */
@supports not (backdrop-filter: blur(40px)) {
    .glass {
        background: rgba(255, 255, 255, 0.9);
    }
}
```

---

## 📈 Roadmap

### v1.0 (Demo 3 Março)
- [x] AR cross-platform
- [x] USDZ validation
- [x] State machine
- [x] Premium UI
- [x] Photo mode (optional)

### v1.1 (Pós-demo)
- [ ] Múltiplos produtos
- [ ] Integração CMS
- [ ] Analytics avançado
- [ ] A/B testing UI
- [ ] Personalização por marca

### v2.0 (Q2 2026)
- [ ] Laboratório de Perguntas integrado
- [ ] Gamificação
- [ ] Social sharing
- [ ] Product recommendations

---

## 🤝 Contribuindo

**Antes de modificar:**
1. Ler `ARCHITECTURE.md` completo
2. Testar em iOS + Android
3. Seguir checklist em `TESTING-CHECKLIST.md`
4. Manter performance (Lighthouse > 90)

---

## 📝 License

MIT License - hackthepack © 2026

---

## 🙋 Suporte

**Problemas?**
1. Verificar console do browser
2. Consultar TROUBLESHOOTING acima
3. Revisar TESTING-CHECKLIST.md
4. Contatar equipe hackthepack

---

## 🎉 Créditos

**hackthepack Team:**
- Sal Zammataro - CEO, Founder, Chief Vision Officer
- Pedro - Co-founder
- Panarelli - Co-founder

**Powered by:**
- model-viewer (Google)
- Vercel (Hosting + AI SDK)
- Reality Converter (Apple)

---

**Built with ❤️ for the Second Layer OS**

*Versão 1.0 Premium - Preparado para demo 3 de Março 2026*
